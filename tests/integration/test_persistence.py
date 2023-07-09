import pytest


@pytest.mark.integration
def test_persisted_result():
    # make a post
    # make a query to the db for the posted geometry --> same as get by id or geometries
    # check expected result is stored
    pass


@pytest.mark.integration
def test_fetch_existing_computation():
    # make 2 post calls
    # make sure in the last one we dont compute the result (number of rows still the same) -> same as test_post_for_existing_result
    pass
