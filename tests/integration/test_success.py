import pytest

from src.persistence import delete_by_id, get_number_of_rows


@pytest.mark.integration
@pytest.mark.asyncio
async def test_vaterlandsparken(fast_api_test_client, vaterlandsparken_input):
    response = fast_api_test_client.post(
        "/split",
        json=vaterlandsparken_input,
        params={"gcs": "EPSG:4326", "pcs": "EPSG:3857"},
    )

    assert response.status_code == 200

    response_json = response.json()

    assert len(response_json["split_building_limits"]["features"]) == 3
    assert (
        response_json["split_building_limits"]["features"][0]["properties"]["elevation"]
        == 3.63
    )
    assert (
        response_json["split_building_limits"]["features"][1]["properties"]["elevation"]
        == 4.63
    )
    assert (
        response_json["split_building_limits"]["features"][2]["properties"]["elevation"]
        == 2.63
    )

    assert response_json["split_building_limits"]["features"][0]["geometry"][
        "coordinates"
    ] == [
        [
            [10.75678086443506, 59.91291413160555],
            [10.757212163013266, 59.913509268463564],
            [10.757867266534337, 59.91339283457274],
            [10.757486364709461, 59.91285434826322],
            [10.75678086443506, 59.91291413160555],
        ]
    ]
    assert response_json["split_building_limits"]["features"][1]["geometry"][
        "coordinates"
    ] == [
        [
            [10.756996990155885, 59.91321236033006],
            [10.756312148602724, 59.91334421009501],
            [10.756398999995643, 59.91346700000333],
            [10.756516000002959, 59.913633000004204],
            [10.757212163013254, 59.91350926846357],
            [10.756996990155885, 59.91321236033006],
        ]
    ]
    assert response_json["split_building_limits"]["features"][2]["geometry"][
        "coordinates"
    ] == [
        [
            [10.75628300000438, 59.91330300000502],
            [10.756312148602724, 59.91334421009501],
            [10.756996990155885, 59.91321236033006],
            [10.75678086443506, 59.91291413160555],
            [10.756245682709302, 59.912959479672516],
            [10.756052815307351, 59.91297582153187],
            [10.75628300000438, 59.91330300000502],
        ]
    ]
    await delete_by_id(response_json["id"])


@pytest.mark.integration
@pytest.mark.asyncio
async def test_post_plateaus_covering_building_limit(
    fast_api_test_client, plateaus_covering_building_limit
):
    response = fast_api_test_client.post(
        "/split", json=plateaus_covering_building_limit
    )

    assert response.status_code == 200

    response_json = response.json()

    assert len(response_json["split_building_limits"]["features"]) == 2
    assert (
        response_json["split_building_limits"]["features"][0]["properties"]["elevation"]
        == 3.63
    )
    assert (
        response_json["split_building_limits"]["features"][1]["properties"]["elevation"]
        == 4.63
    )

    assert response_json["split_building_limits"]["features"][0]["geometry"][
        "coordinates"
    ] == [[[0.0, 0.0], [0.0, 10.0], [5.0, 10.0], [5.0, 0.0], [0.0, 0.0]]]
    assert response_json["split_building_limits"]["features"][1]["geometry"][
        "coordinates"
    ] == [[[5.0, 0.0], [5.0, 10.0], [10.0, 10.0], [10.0, 0.0], [5.0, 0.0]]]

    await delete_by_id(response_json["id"])


@pytest.mark.integration
@pytest.mark.asyncio
async def test_post_plateaus_covering_multiple_buildings_limits(
    fast_api_test_client, plateaus_covering_multiple_buildings_limits
):
    response = fast_api_test_client.post(
        "/split", json=plateaus_covering_multiple_buildings_limits
    )

    assert response.status_code == 200

    response_json = response.json()

    assert len(response_json["split_building_limits"]["features"]) == 4
    assert (
        response_json["split_building_limits"]["features"][0]["properties"]["elevation"]
        == 3.63
    )
    assert (
        response_json["split_building_limits"]["features"][1]["properties"]["elevation"]
        == 4.63
    )
    assert (
        response_json["split_building_limits"]["features"][2]["properties"]["elevation"]
        == 3.63
    )
    assert (
        response_json["split_building_limits"]["features"][3]["properties"]["elevation"]
        == 4.63
    )

    assert response_json["split_building_limits"]["features"][0]["geometry"][
        "coordinates"
    ] == [[[0.0, 0.0], [0.0, 4.0], [5.0, 4.0], [5.0, 0.0], [0.0, 0.0]]]
    assert response_json["split_building_limits"]["features"][1]["geometry"][
        "coordinates"
    ] == [[[5.0, 0.0], [5.0, 4.0], [10.0, 4.0], [10.0, 0.0], [5.0, 0.0]]]
    assert response_json["split_building_limits"]["features"][2]["geometry"][
        "coordinates"
    ] == [[[5.0, 6.0], [0.0, 6.0], [0.0, 10.0], [5.0, 10.0], [5.0, 6.0]]]
    assert response_json["split_building_limits"]["features"][2]["geometry"][
        "coordinates"
    ] == [[[5.0, 6.0], [0.0, 6.0], [0.0, 10.0], [5.0, 10.0], [5.0, 6.0]]]
    await delete_by_id(response_json["id"])


@pytest.mark.integration
@pytest.mark.asyncio
async def test_post_for_existing_result(
    fast_api_test_client, plateaus_covering_building_limit
):
    # make two post call to split
    # make sure in the last one we dont compute the result (number of rows still the same)
    num_rows = await get_number_of_rows()
    # make one delete call to delete the row
    response = fast_api_test_client.post(
        "/split", json=plateaus_covering_building_limit
    )
    assert response.status_code == 200
    assert await get_number_of_rows() == num_rows + 1

    response = fast_api_test_client.post(
        "/split", json=plateaus_covering_building_limit
    )
    response_json = response.json()

    assert response.status_code == 200
    assert await get_number_of_rows() == num_rows + 1
    await delete_by_id(response_json["id"])


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_by_id(fast_api_test_client, plateaus_covering_building_limit):
    response_post = fast_api_test_client.post(
        "/split", json=plateaus_covering_building_limit
    )
    response_post_json = response_post.json()
    assert response_post.status_code == 200

    row_id = response_post_json["id"]

    response_get = fast_api_test_client.get(f"/{row_id}")

    assert response_get.status_code == 200
    assert (
        response_post_json["split_building_limits"]
        == response_get.json()["split_building_limits"]
    )

    await delete_by_id(row_id)


@pytest.mark.integration
def test_delete_by_id(fast_api_test_client, plateaus_covering_building_limit):
    response_post = fast_api_test_client.post(
        "/split", json=plateaus_covering_building_limit
    )
    response_post_json = response_post.json()
    assert response_post.status_code == 200

    row_id = response_post_json["id"]

    fast_api_test_client.delete(f"/delete/{row_id}")

    response_get = fast_api_test_client.get(f"/{row_id}")

    assert response_get.status_code == 404
    assert "not found" in response_get.json()["message"]


# def test_delete_all_rows():
#     delete_all_rows()
