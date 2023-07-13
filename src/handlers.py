import json
import logging

from src.helpers import (
    validate_not_overlapping_polygons,
    validate_plateaus_fully_cover_building_limits,
)
from src.models import OutputModel
from src.persistence import (
    get_connection,
    get_existing_split_building_limits,
    write_split_building_limits_to_database,
)

from src.models import InputModel


logger = logging.getLogger(__name__)


async def split_and_persist_building_limits_unsafe(
    input_data: InputModel, gcs: str, pcs: str
):
    """
    Split building limits and persist them to database.

    Args:
        input_data (InputModel): Input data containing building limits and height plateaus.
        gcs (str): The GCS (Geographic Coordinate System) of the input data.
            For example: EPSG:4326.
        pcs (str): The PCS (Projected Coordinate System) of the input data.
            For example: EPSG:3857.

    Returns:
        OutputModel: Output data containing the id of the split building limits and the split building limits geojson.

    """
    async_connection = await get_connection()

    async with async_connection:  # connection will be closed after exiting
        existing_split_building_limits = await get_existing_split_building_limits(
            async_connection,
            building_limits_str=input_data.building_limits.json(),
            height_plateaus_str=input_data.height_plateaus.json(),
        )

        if existing_split_building_limits:
            logging.info("Found existing split building limits in database.")
            return OutputModel(
                id=existing_split_building_limits[0],
                split_building_limits=json.loads(existing_split_building_limits[1]),
            )

        logging.info("Not found existing split building.")
        building_limits_gdf, height_plateaus_gdf = input_data.to_geodataframes(gcs=gcs)
        validate_not_overlapping_polygons(building_limits_gdf, pcs=pcs)
        validate_not_overlapping_polygons(height_plateaus_gdf, pcs=pcs)
        validate_plateaus_fully_cover_building_limits(
            height_plateaus_gdf, building_limits_gdf
        )

        building_limits_split_gdf = height_plateaus_gdf.overlay(
            building_limits_gdf, how="intersection"
        )
        building_limits_split_json = building_limits_split_gdf.to_json()

        building_limits_split_dict = json.loads(building_limits_split_json)

        row_id = await write_split_building_limits_to_database(
            async_connection,
            building_limits_str=input_data.building_limits.json(),
            height_plateaus_str=input_data.height_plateaus.json(),
            split_building_limits_str=building_limits_split_json,
        )
        logger.info(building_limits_split_dict)
        return OutputModel(id=row_id, split_building_limits=building_limits_split_dict)
