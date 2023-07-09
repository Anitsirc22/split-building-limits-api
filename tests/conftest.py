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
