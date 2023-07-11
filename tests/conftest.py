import json

import pytest

from fastapi.testclient import TestClient

from src.app import app


@pytest.fixture
def fast_api_test_client():
    """Create a tess client."""
    client = TestClient(app)

    return client


@pytest.fixture
def plateaus_covering_building_limit():
    """Get data for plateaus covering a building limit."""
    with open("tests/input_files/plateaus_covering_building_limit.json") as input_file:
        input_json = json.load(input_file)
    return input_json


@pytest.fixture
def vaterlandsparken_input():
    """Get data for vaterlandsparken."""
    with open("tests/input_files/vaterlandsparken.json") as input_file:
        input_json = json.load(input_file)
    return input_json


@pytest.fixture
def plateaus_covering_multiple_buildings_limits():
    """Get data for plateaus covering multiple building limit."""
    with open(
        "tests/input_files/plateaus_covering_multiple_building_limits.json"
    ) as input_file:
        input_json = json.load(input_file)
    return input_json


@pytest.fixture
def plateaus_not_fully_covering_building_limits():
    """Get data for plateaus covering multiple building limit."""
    with open(
        "tests/input_files/plateaus_not_fully_covering_building_limits_error.json"
    ) as input_file:
        input_json = json.load(input_file)
    return input_json


@pytest.fixture
def plateaus_with_holes():
    """Get data for plateaus covering multiple building limit."""
    with open("tests/input_files/plateaus_with_holes_error.json") as input_file:
        input_json = json.load(input_file)
    return input_json


@pytest.fixture
def building_limit_with_holes():
    """Get data for plateaus covering multiple building limit."""
    with open("tests/input_files/building_limit_with_holes_error.json") as input_file:
        input_json = json.load(input_file)
    return input_json


@pytest.fixture
def plateaus_without_elevation_data():
    """Get data for plateaus covering multiple building limit."""
    with open(
        "tests/input_files/plateaus_without_elevation_data_error.json"
    ) as input_file:
        input_json = json.load(input_file)
    return input_json


@pytest.fixture
def building_limit_plateaus_coordinates_format_error():
    """Get data for plateaus covering multiple building limit."""
    with open(
        "tests/input_files/building_limit_plateaus_coordinates_format_error.json"
    ) as input_file:
        input_json = json.load(input_file)
    return input_json


@pytest.fixture
def overlapping_building_limits():
    """Get data for plateaus covering multiple building limit."""
    with open("tests/input_files/overlapping_building_limits_error.json") as input_file:
        input_json = json.load(input_file)
    return input_json


@pytest.fixture
def overlapping_height_plateaus():
    """Get data for plateaus covering multiple building limit."""
    with open("tests/input_files/overlapping_height_plateaus_error.json") as input_file:
        input_json = json.load(input_file)
    return input_json


@pytest.fixture
def building_limit_plateaus_format_error():
    """Get data for plateaus covering multiple building limit."""
    with open(
        "tests/input_files/building_limit_plateaus_format_error.json"
    ) as input_file:
        input_json = json.load(input_file)
    return input_json
