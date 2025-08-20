import pytest

from zotify_api.main import app
from zotify_api.services import cache_service


@pytest.fixture
def cache_service_override():
    """Fixture to override the cache service with a predictable state."""
    cache_state = {"search": 80, "metadata": 222}

    def get_cache_service_override():
        return cache_service.CacheService(cache_state)

    original_override = app.dependency_overrides.get(cache_service.get_cache_service)
    app.dependency_overrides[cache_service.get_cache_service] = (
        get_cache_service_override
    )
    yield
    app.dependency_overrides.pop(cache_service.get_cache_service, None)
    if original_override:
        app.dependency_overrides[cache_service.get_cache_service] = original_override


def test_get_cache(client, cache_service_override):
    response = client.get("/api/cache")
    assert response.status_code == 200
    assert "total_items" in response.json()["data"]


def test_clear_cache_all_unauthorized(client, cache_service_override):
    response = client.request("DELETE", "/api/cache", json={})
    assert response.status_code == 401


def test_clear_cache_all(client, cache_service_override):
    # Get initial state
    initial_response = client.get("/api/cache")
    initial_total = initial_response.json()["data"]["total_items"]
    assert initial_total > 0

    # Clear all with correct API key
    response = client.request(
        "DELETE", "/api/cache", headers={"X-API-Key": "test_key"}, json={}
    )
    assert response.status_code == 200
    data = response.json().get("data", {})
    assert data.get("by_type", {}).get("search") == 0
    assert data.get("by_type", {}).get("metadata") == 0

    # Verify that the cache is empty
    final_response = client.get("/api/cache")
    assert final_response.json()["data"]["total_items"] == 0


def test_clear_cache_by_type_unauthorized(client, cache_service_override):
    response = client.request("DELETE", "/api/cache", json={"type": "search"})
    assert response.status_code == 401


def test_clear__by_type(client, cache_service_override):
    # Clear by type with correct API key
    response = client.request(
        "DELETE",
        "/api/cache",
        headers={"X-API-Key": "test_key"},
        json={"type": "search"},
    )
    assert response.status_code == 200
    data = response.json().get("data", {})
    assert data.get("by_type", {}).get("search") == 0
    assert data.get("by_type", {}).get("metadata") != 0
