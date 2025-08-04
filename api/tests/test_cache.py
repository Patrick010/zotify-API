import json
import pytest
from fastapi.testclient import TestClient
from zotify_api.main import app
from zotify_api.routes.cache import cache_state as app_cache_state

client = TestClient(app)

@pytest.fixture(autouse=True)
def run_around_tests():
    # Reset the cache state before each test
    global app_cache_state
    app_cache_state.update({
        "search": 80,
        "metadata": 222
    })
    yield

def test_get_cache():
    response = client.get("/api/cache")
    assert response.status_code == 200
    assert "total_items" in response.json()

def test_clear_cache_all():
    # Get initial state
    initial_response = client.get("/api/cache")
    initial_total = initial_response.json()["total_items"]
    assert initial_total > 0

    # Clear all
    response = client.request("DELETE", "/api/cache", json={})
    assert response.status_code == 200
    assert response.json()["by_type"]["search"] == 0
    assert response.json()["by_type"]["metadata"] == 0

    # Verify that the cache is empty
    final_response = client.get("/api/cache")
    assert final_response.json()["total_items"] == 0


def test_clear_cache_by_type():
    # Clear by type
    response = client.request("DELETE", "/api/cache", json={"type": "search"})
    assert response.status_code == 200
    assert response.json()["by_type"]["search"] == 0
    assert response.json()["by_type"]["metadata"] != 0
