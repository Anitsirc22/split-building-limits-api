import json
import logging
import time

from typing import Optional

import uvicorn

from fastapi import Body, FastAPI, Path, Query

from src.error_handlers import (
    input_geometry_error_handler,
    input_value_error_handler,
    split_building_limits_not_found_handler,
)
from src.exceptions import (
    InputGeometryError,
    InputValueError,
    SplitBuildingLimitsNotFoundError,
)
from src.handlers import split_and_persist_building_limits_unsafe
from src.models import ErrorMessageModel, InputModel, OutputModel
from src.persistence import delete_all_rows, delete_by_id, get_by_id


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


app.add_exception_handler(InputGeometryError, input_geometry_error_handler)
app.add_exception_handler(InputValueError, input_value_error_handler)
app.add_exception_handler(
    SplitBuildingLimitsNotFoundError, split_building_limits_not_found_handler
)


@app.post("/split", responses={400: {"model": ErrorMessageModel}})
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
) -> OutputModel:
    """
    Split building limits according to height plateaus.
    - building_limits: The areas (polygons) on your site where you are allowed to build. Expected format: GeoJSON with type FeatureCollection.
    - height_plateaus: Areas (polygons) on your site with different elevation. Expected format: GeoJSON with type FeatureCollection.

    """
    # add response model with the errors

    return await split_and_persist_building_limits_unsafe(input_data, gcs, pcs)


@app.get("/{id}", responses={404: {"model": ErrorMessageModel}})
async def get_building_limits_by_id(
    id: int = Path(..., description="The id of the building limits.")
) -> OutputModel:
    """Get building limits by id."""
    existing_split_building_limits = await get_by_id(id)
    return OutputModel(
        id=existing_split_building_limits[0],
        split_building_limits=json.loads(existing_split_building_limits[1]),
    )


@app.delete("/delete_all")
async def delete_all_building_limits():
    """Get building limits by id."""
    return await delete_all_rows()


@app.delete("/delete/{id}", responses={404: {"model": ErrorMessageModel}})
async def delete_building_limits_by_id(
    id: int = Path(..., description="The id of the building limits.")
):
    """Get building limits by id."""
    return await delete_by_id(id)


if __name__ == "__main__":
    uvicorn.run("app:app", port=8000, reload=True)
