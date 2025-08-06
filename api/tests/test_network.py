import pytest
from fastapi.testclient import TestClient
from zotify_api.main import app
from zotify_api.services import network_service

client = TestClient(app)

@pytest.fixture
def network_service_override():
    network_config = {
        "proxy_enabled": False,
        "http_proxy": None,
        "https_proxy": None
    }
    def get_network_service_override():
        return network_service.NetworkService(network_config)
    return get_network_service_override

def test_get_network(network_service_override):
    app.dependency_overrides[network_service.get_network_service] = network_service_override
    response = client.get("/api/network")
    assert response.status_code == 200
    assert "proxy_enabled" in response.json()
    app.dependency_overrides = {}

def test_update_network_unauthorized(network_service_override):
    app.dependency_overrides[network_service.get_network_service] = network_service_override
    update_data = {
        "proxy_enabled": True,
        "http_proxy": "http://proxy.local:3128",
        "https_proxy": "https://secure.proxy:443"
    }
    response = client.patch("/api/network", json=update_data)
    assert response.status_code == 401
    app.dependency_overrides = {}

def test_update_network(network_service_override, monkeypatch):
    monkeypatch.setattr("zotify_api.config.settings.admin_api_key", "test_key")
    app.dependency_overrides[network_service.get_network_service] = network_service_override
    update_data = {
        "proxy_enabled": True,
        "http_proxy": "http://proxy.local:3128",
        "https_proxy": "https://secure.proxy:443"
    }
    response = client.patch("/api/network", headers={"X-API-Key": "test_key"}, json=update_data)
    assert response.status_code == 200
    assert response.json()["proxy_enabled"] is True
    assert response.json()["http_proxy"] == "http://proxy.local:3128"
    app.dependency_overrides = {}
