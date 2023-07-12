import logging

from typing import Optional

import geopandas as gpd

from src.exceptions import InputGeometryError


logger = logging.getLogger(__name__)


def validate_not_overlapping_polygons(gdf: gpd.GeoDataFrame, pcs: Optional[str] = None):
    """Validate that polygons do not overlap.

    Args:
        gdf (GeoDataFrame): GeoDataFrame with polygons.
        pcs (Optional[str]): The PCS (Projected Coordinate System) of the input data.
            For example: EPSG:3857. Defaults to None.

    Raises:
        InputGeometryError: If polygons overlap.

    """
    if pcs:
        gdf = gdf.to_crs(pcs)

    polygons_geoseries = gpd.GeoSeries(gdf.geometry)
    polygons_area = sum(polygons_geoseries.area)
    logger.info(polygons_area)

    polygons_union = polygons_geoseries.unary_union
    polygons_union_area = polygons_union.area
    logger.info(polygons_union_area)

    if abs(polygons_area - polygons_union_area) > 1e-6:
        logger.error("Input polygons overlap.")
        raise InputGeometryError("Please provide input polygons that do not overlap.")


def validate_plateaus_fully_cover_building_limits(
    gdf_plateaus: gpd.GeoDataFrame, gdf_building_limits: gpd.GeoDataFrame
):
    """Validate that height plateaus fully cover the building limits.

    Args:
        gdf_plateaus (gpd.GeoDataFrame): GeoDataFrame with height plateaus.
        gdf_building_limits (gpd.GeoDataFrame): GeoDataFrame with building limits.

    Raises:
        InputGeometryError: If height plateaus do not fully cover the building limits.
    """
    plateaus_fully_cover_building_limits = gdf_plateaus.unary_union.buffer(
        1e-6
    ).contains(gdf_building_limits.unary_union)
    if not plateaus_fully_cover_building_limits:
        raise InputGeometryError(
            "Please provide height plateaus that fully cover the building limits."
        )
