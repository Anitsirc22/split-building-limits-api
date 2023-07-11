import geopandas as gpd
import pytest

from shapely.geometry import Polygon

from src.exceptions import InputGeometryError
from src.helpers import (
    validate_not_overlapping_polygons,
    validate_plateaus_fully_cover_building_limits,
)


@pytest.mark.unit
def test_validate_not_overlapping_polygons():
    polygon1 = Polygon([(0, 0), (2, 0), (2, 2), (0, 2)])
    polygon2 = Polygon([(2, 0), (4, 0), (4, 4), (2, 4)])

    data = {"Name": ["Polygon 1", "Polygon 2"], "Geometry": [polygon1, polygon2]}
    gdf = gpd.GeoDataFrame(data, geometry="Geometry")

    validate_not_overlapping_polygons(gdf)
    validate_plateaus_fully_cover_building_limits(gdf, gdf)


@pytest.mark.unit
def test_validate_not_overlapping_polygons_error():
    polygon1 = Polygon([(0, 0), (2, 0), (2, 2), (0, 2)])
    polygon2 = Polygon([(1, 1), (3, 1), (3, 3), (1, 3)])

    data = {"Name": ["Polygon 1", "Polygon 2"], "Geometry": [polygon1, polygon2]}
    gdf = gpd.GeoDataFrame(data, geometry="Geometry")

    with pytest.raises(InputGeometryError) as excinfo:
        validate_not_overlapping_polygons(gdf)

    assert "Please provide input polygons that do not overlap." == str(excinfo.value)


@pytest.mark.unit
def test_validate_plateaus_not_fully_cover_building_limits_error():
    polygon1 = Polygon([(0, 0), (5, 0), (5, 5), (0, 5)])
    polygon2 = Polygon([(1, 1), (3, 1), (3, 3), (1, 3)])

    data1 = {"Name": ["Polygon 1"], "Geometry": [polygon1]}
    data2 = {"Name": ["Polygon 2"], "Geometry": [polygon2]}
    gdf1 = gpd.GeoDataFrame(data1, geometry="Geometry")
    gdf2 = gpd.GeoDataFrame(data2, geometry="Geometry")

    with pytest.raises(InputGeometryError) as excinfo:
        validate_plateaus_fully_cover_building_limits(gdf2, gdf1)

    assert (
        "Please provide height plateaus that fully cover the building limits."
        == str(excinfo.value)
    )
