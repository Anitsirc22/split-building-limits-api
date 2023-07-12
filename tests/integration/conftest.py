import pytest

from fastapi.testclient import TestClient

from src.app import app


class PostClient:
    def __init__(self, client, *args, **kwargs):
        """Test Client context manager.
        Deletes row created by the test after the test is finished.
        """
        self.client = client
        self.result = None
        self.args = args
        self.kwargs = kwargs

    def __enter__(self):
        self.result = self.client.post(*self.args, **self.kwargs)
        return self.result

    def __exit__(self, exc_type, exc_val, exc_tb):
        response_json = self.result.json()

        # make sure the created row is deleted after the test
        row_id = response_json.get("id")
        if row_id is not None:
            self.client.delete(f"/delete/{row_id}")


@pytest.fixture
def fast_api_test_client():
    """Create a test client."""
    client = TestClient(app)

    return client
