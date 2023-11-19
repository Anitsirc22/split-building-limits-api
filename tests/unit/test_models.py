import pytest

from src.exceptions import InputGeometryError, InputValueError
from src.models import InputModel


# test outputmodel, patch the return object to not have the elevation and check error message


@pytest.mark.unit
def test_input_model(plateaus_covering_building_limit):
    input_model = InputModel(**plateaus_covering_building_limit)
    expected_dump = {
        "building_limits": {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[0, 0], [10, 0], [10, 10], [0, 10]]],
                    },
                    "properties": {},
                }
            ],
        },
        "height_plateaus": {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[0, 0], [5, 0], [5, 10], [0, 10]]],
                    },
                    "properties": {"elevation": 3.63},
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[5, 0], [10, 0], [10, 10], [5, 10]]],
                    },
                    "properties": {"elevation": 4.63},
                },
            ],
        },
    }
    assert input_model.dict() == expected_dump


@pytest.mark.unit
@pytest.mark.parametrize("input_data", ["plateaus_with_holes", "building_limit_with_holes"])
def test_input_model_contains_inner_holes_error(input_data, request):
    input_data_ = request.getfixturevalue(input_data)
    with pytest.raises(InputGeometryError) as excinfo:
        InputModel(**input_data_)

    assert "Polygons cannot contain inner holes." == str(excinfo.value)


@pytest.mark.unit
def test_input_model_plateaus_without_elevation_data_error(
    plateaus_without_elevation_data,
):
    with pytest.raises(InputValueError) as excinfo:
        InputModel(**plateaus_without_elevation_data)

    assert "Height plateaus should contain elevation information." == str(excinfo.value)


@pytest.mark.unit
def test_input_model_(building_limit_plateaus_coordinates_format_error):
    with pytest.raises(InputGeometryError) as excinfo:
        InputModel(**building_limit_plateaus_coordinates_format_error)

    assert "Only 2d or 3d geometries supported." in str(excinfo.value)


@pytest.mark.unit
def test_output_model():
    pass


@pytest.mark.unit
def test_output_model_without_elevation_error():
    pass
