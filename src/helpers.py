import logging

from typing import Optional

import geopandas as gpd


logger = logging.getLogger(__name__)


def validate_not_overlapping_polygons(gdf: gpd.GeoDataFrame, pcs: Optional[str] = None):
    """Validate that polygons do not overlap.

    Args:
        gdf (GeoDataFrame): GeoDataFrame with polygons.
        pcs (Optional[str]): The PCS (Projected Coordinate System) of the input data.
            For example: EPSG:3857. Defaults to None.

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
        raise ValueError("Input polygons overlap.")

    return
