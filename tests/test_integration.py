import pytest


@pytest.mark.integration
def test_vaterlandsparken(fast_api_test_client, vaterlandsparken_input):
    response = fast_api_test_client.post(
        "/split",
        json=vaterlandsparken_input,
        params={"gcs": "EPSG:4326", "pcs": "EPSG:3857"},
    )

    assert response.status_code == 200

    response_json = response.json()

    assert len(response_json["features"]) == 3
    assert response_json["features"][0]["properties"]["elevation"] == 3.63
    assert response_json["features"][1]["properties"]["elevation"] == 4.63
    assert response_json["features"][2]["properties"]["elevation"] == 2.63

    assert response_json["features"][0]["geometry"]["coordinates"] == [
        [
            [10.75678086443506, 59.91291413160555],
            [10.757212163013266, 59.913509268463564],
            [10.757867266534337, 59.91339283457274],
            [10.757486364709461, 59.91285434826322],
            [10.75678086443506, 59.91291413160555],
        ]
    ]
    assert response_json["features"][1]["geometry"]["coordinates"] == [
        [
            [10.756996990155885, 59.91321236033006],
            [10.756312148602724, 59.91334421009501],
            [10.756398999995643, 59.91346700000333],
            [10.756516000002959, 59.913633000004204],
            [10.757212163013254, 59.91350926846357],
            [10.756996990155885, 59.91321236033006],
        ]
    ]
    assert response_json["features"][2]["geometry"]["coordinates"] == [
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


@pytest.mark.integration
def test_plateaus_covering_building_limit(
    fast_api_test_client, plateaus_covering_building_limit
):
    response = fast_api_test_client.post(
        "/split", json=plateaus_covering_building_limit
    )

    assert response.status_code == 200

    response_json = response.json()

    assert len(response_json["features"]) == 2
    assert response_json["features"][0]["properties"]["elevation"] == 3.63
    assert response_json["features"][1]["properties"]["elevation"] == 4.63

    assert response_json["features"][0]["geometry"]["coordinates"] == [
        [[0.0, 0.0], [0.0, 10.0], [5.0, 10.0], [5.0, 0.0], [0.0, 0.0]]
    ]
    assert response_json["features"][1]["geometry"]["coordinates"] == [
        [[5.0, 0.0], [5.0, 10.0], [10.0, 10.0], [10.0, 0.0], [5.0, 0.0]]
    ]
