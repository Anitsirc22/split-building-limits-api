import pytest


# check expected status error code and message


@pytest.mark.integration
def test_overlapping_polygons_error():
    assert 1 == 1


@pytest.mark.integration
def test_plateaus_without_elevation_data_error():
    pass


@pytest.mark.integration
def test_3d_coordinates_error():
    pass


@pytest.mark.integration
def test_polygons_with_inner_holes_error():
    pass


@pytest.mark.integration
def test_input_schema_error():
    # parametrize for different errors
    pass
