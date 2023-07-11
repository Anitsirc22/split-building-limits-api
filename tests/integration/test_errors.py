import pytest


@pytest.mark.parametrize(
    "input_data_overlapping",
    ["overlapping_building_limits", "overlapping_height_plateaus"],
)
@pytest.mark.integration
def test_overlapping_polygons_error(
    fast_api_test_client, request, input_data_overlapping
):
    input_data = request.getfixturevalue(input_data_overlapping)
    response = fast_api_test_client.post("/split", json=input_data)

    assert response.status_code == 400
    assert response.json() == {
        "message": "Please provide input polygons that do not overlap."
    }


@pytest.mark.integration
def test_plateaus_without_elevation_data_error(
    fast_api_test_client, plateaus_without_elevation_data
):
    response = fast_api_test_client.post("/split", json=plateaus_without_elevation_data)

    assert response.status_code == 400
    assert response.json() == {
        "message": "Height plateaus should contain elevation information."
    }


@pytest.mark.integration
def test_plateaus_not_fully_covering_building_limits_error(
    fast_api_test_client, plateaus_not_fully_covering_building_limits
):
    response = fast_api_test_client.post(
        "/split", json=plateaus_not_fully_covering_building_limits
    )

    assert response.status_code == 400
    assert response.json() == {
        "message": "Please provide height plateaus that fully cover the building limits."
    }


@pytest.mark.integration
def test_coordinates_error(
    fast_api_test_client, building_limit_plateaus_coordinates_format_error
):
    response = fast_api_test_client.post(
        "/split", json=building_limit_plateaus_coordinates_format_error
    )

    assert response.status_code == 400
    assert "Only 2d or 3d geometries supported." in response.json()["message"]


@pytest.mark.parametrize(
    "input_data_holes", ["building_limit_with_holes", "plateaus_with_holes"]
)
@pytest.mark.integration
def test_polygons_with_inner_holes_error(
    fast_api_test_client, request, input_data_holes
):
    input_data = request.getfixturevalue(input_data_holes)
    response = fast_api_test_client.post("/split", json=input_data)

    assert response.status_code == 400
    assert response.json() == {"message": "Polygons cannot contain inner holes."}


@pytest.mark.integration
def test_input_schema_error(fast_api_test_client, building_limit_plateaus_format_error):
    response = fast_api_test_client.post(
        "/split", json=building_limit_plateaus_format_error
    )

    assert response.status_code == 422
