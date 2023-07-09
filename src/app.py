import json
import logging
import time

from typing import Optional

import uvicorn

from fastapi import Body, FastAPI, Query

from src.helpers import validate_not_overlapping_polygons
from src.models import FeatureCollectionModel, InputModel
from src.persistence import (
    delete_all_rows,
    get_connection,
    get_existing_split_building_limits,
    write_split_building_limits_to_database,
)


logging.basicConfig(level=logging.INFO)

description = """
The **Split Building Limits API** consumes building limits and height plateaus, splits up the building limits according to the height plateaus, and stores these three entities (building limits, height plateaus and split building limits) in a
in a Postgres database.

"""
input_data_description = """
building_limits: The areas (polygons) on your site where you are allowed to build. \nExpected format: GeoJSON with type FeatureCollection.
height_plateaus: Areas (polygons) on your site with different elevation. \nExpected format: GeoJSON with type FeatureCollection.
"""
app = FastAPI(title="Split building limits API", description=description)


@app.middleware("http")
async def add_process_time_header(request, call_next):
    """Add request process time in the response header.

    A middleware is a function that works with every request before it is processed by any specific
    path operation and also with every response before returning it.

    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(f"{process_time:0.4f} sec")
    return response


# todo add error handler, return 422 for InputGeomertyError and InputValueError


@app.post("/split")
async def split_building_limits(
    gcs: Optional[str] = Query(
        default=None,
        description="The GCS (Geographic Coordinate System) of the input data. For example: EPSG:4326.",
    ),
    pcs: Optional[str] = Query(
        default=None,
        description="The PCS (Projected Coordinate System) of the input data. For example: EPSG:3857.",
    ),
    input_data: InputModel = Body(),
) -> FeatureCollectionModel:
    """
    Split building limits according to height plateaus.
    - building_limits: The areas (polygons) on your site where you are allowed to build. Expected format: GeoJSON with type FeatureCollection.
    - height_plateaus: Areas (polygons) on your site with different elevation. Expected format: GeoJSON with type FeatureCollection.

    """
    # todo: refactor to compute_split_building_limits_safe
    # add response model with the errors
    await delete_all_rows()
    async_connection = await get_connection()
    async with async_connection:  # connection will be closed after exiting
        existing_split_building_limits = await get_existing_split_building_limits(
            async_connection,
            building_limits_str=input_data.building_limits.json(),
            height_plateaus_str=input_data.height_plateaus.json(),
        )

        if existing_split_building_limits:
            logging.info("Found existing split building limits in database.")
            return existing_split_building_limits

        logging.info("Not found existing split building.")
        building_limits_gdf, height_plateaus_gdf = input_data.to_geodataframes(gcs=gcs)

        validate_not_overlapping_polygons(building_limits_gdf, pcs=pcs)
        validate_not_overlapping_polygons(height_plateaus_gdf, pcs=pcs)

        building_limits_split_gdf = height_plateaus_gdf.overlay(
            building_limits_gdf, how="intersection"
        )
        building_limits_split_json = (
            building_limits_split_gdf.to_json()
        )  # to_json returns string, json.loads converts to dict

        await write_split_building_limits_to_database(
            async_connection,
            building_limits_str=input_data.building_limits.json(),
            height_plateaus_str=input_data.height_plateaus.json(),
            split_building_limits_str=building_limits_split_json,
        )

    logging.info(building_limits_split_json)
    return json.loads(building_limits_split_json)


# todo add /byid, /bygeometry, /delete

if __name__ == "__main__":
    uvicorn.run("app:app", port=8000, reload=True)
