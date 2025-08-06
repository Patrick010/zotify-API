import pytest
from fastapi.testclient import TestClient
from zotify_api.main import app
from zotify_api.services import cache_service
import json

client = TestClient(app)

@pytest.fixture
def cache_service_override():
    cache_state = {
        "search": 80,
        "metadata": 222
    }
    def get_cache_service_override():
        return cache_service.CacheService(cache_state)
    return get_cache_service_override

def test_get_cache(cache_service_override):
    app.dependency_overrides[cache_service.get_cache_service] = cache_service_override
    response = client.get("/api/cache")
    assert response.status_code == 200
    assert "total_items" in response.json()["data"]
    app.dependency_overrides = {}

def test_clear_cache_all_unauthorized(cache_service_override):
    app.dependency_overrides[cache_service.get_cache_service] = cache_service_override
    response = client.request("DELETE", "/api/cache", content=json.dumps({}))
    assert response.status_code == 401
    app.dependency_overrides = {}

def test_clear_cache_all(cache_service_override, monkeypatch):
    monkeypatch.setattr("zotify_api.config.settings.admin_api_key", "test_key")
    app.dependency_overrides[cache_service.get_cache_service] = cache_service_override
    # Get initial state
    initial_response = client.get("/api/cache")
    initial_total = initial_response.json()["data"]["total_items"]
    assert initial_total > 0

    # Clear all
    response = client.request("DELETE", "/api/cache", headers={"X-API-Key": "test_key"}, content=json.dumps({}))
    assert response.status_code == 200
    assert response.json()["data"]["by_type"]["search"] == 0
    assert response.json()["data"]["by_type"]["metadata"] == 0

    # Verify that the cache is empty
    final_response = client.get("/api/cache")
    assert final_response.json()["data"]["total_items"] == 0
    app.dependency_overrides = {}

def test_clear_cache_by_type_unauthorized(cache_service_override):
    app.dependency_overrides[cache_service.get_cache_service] = cache_service_override
    response = client.request("DELETE", "/api/cache", content=json.dumps({"type": "search"}))
    assert response.status_code == 401
    app.dependency_overrides = {}

def test_clear__by_type(cache_service_override, monkeypatch):
    monkeypatch.setattr("zotify_api.config.settings.admin_api_key", "test_key")
    app.dependency_overrides[cache_service.get_cache_service] = cache_service_override
    # Clear by type
    response = client.request("DELETE", "/api/cache", headers={"X-API-Key": "test_key"}, content=json.dumps({"type": "search"}))
    assert response.status_code == 200
    assert response.json()["data"]["by_type"]["search"] == 0
    assert response.json()["data"]["by_type"]["metadata"] != 0
    app.dependency_overrides = {}
