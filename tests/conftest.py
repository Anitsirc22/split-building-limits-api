import json

import pytest


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
    """Get data for plateaus covering multiple building limits."""
    with open("tests/input_files/plateaus_covering_multiple_building_limits.json") as input_file:
        input_json = json.load(input_file)
    return input_json


@pytest.fixture
def plateaus_not_fully_covering_building_limits():
    """Get data for plateaus not fully covering building limits."""
    with open("tests/input_files/plateaus_not_fully_covering_building_limits_error.json") as input_file:
        input_json = json.load(input_file)
    return input_json


@pytest.fixture
def plateaus_with_holes():
    """Get data for plateaus with inner holes."""
    with open("tests/input_files/plateaus_with_holes_error.json") as input_file:
        input_json = json.load(input_file)
    return input_json


@pytest.fixture
def building_limit_with_holes():
    """Get data for a building limit with inner holes."""
    with open("tests/input_files/building_limit_with_holes_error.json") as input_file:
        input_json = json.load(input_file)
    return input_json


@pytest.fixture
def plateaus_without_elevation_data():
    """Get data for plateaus without elevation data."""
    with open("tests/input_files/plateaus_without_elevation_data_error.json") as input_file:
        input_json = json.load(input_file)
    return input_json


@pytest.fixture
def building_limit_plateaus_coordinates_format_error():
    """Get data for building limits and plateaus with invalid coordinate format."""
    with open("tests/input_files/building_limit_plateaus_coordinates_format_error.json") as input_file:
        input_json = json.load(input_file)
    return input_json


@pytest.fixture
def overlapping_building_limits():
    """Get data for overlapping building limits."""
    with open("tests/input_files/overlapping_building_limits_error.json") as input_file:
        input_json = json.load(input_file)
    return input_json


@pytest.fixture
def overlapping_height_plateaus():
    """Get data for overlapping height plateaus."""
    with open("tests/input_files/overlapping_height_plateaus_error.json") as input_file:
        input_json = json.load(input_file)
    return input_json


@pytest.fixture
def building_limit_plateaus_format_error():
    """Get data for a building limit and plateaus with invalid format."""
    with open("tests/input_files/building_limit_plateaus_format_error.json") as input_file:
        input_json = json.load(input_file)
    return input_json
