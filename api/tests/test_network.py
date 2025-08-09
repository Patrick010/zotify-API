import pytest
from zotify_api.main import app
from zotify_api.services import network_service

@pytest.fixture
def network_service_override():
    """Fixture to override the network service with a predictable state."""
    network_config = {
        "proxy_enabled": False,
        "http_proxy": None,
        "https_proxy": None
    }
    def get_network_service_override():
        return network_service.NetworkService(network_config)

    original_override = app.dependency_overrides.get(network_service.get_network_service)
    app.dependency_overrides[network_service.get_network_service] = get_network_service_override
    yield
    app.dependency_overrides[network_service.get_network_service] = original_override


def test_get_network(client, network_service_override):
    response = client.get("/api/network")
    assert response.status_code == 200
    assert "proxy_enabled" in response.json()

def test_update_network_unauthorized(client, network_service_override):
    update_data = {
        "proxy_enabled": True,
        "http_proxy": "http://proxy.local:3128",
        "https_proxy": "https://secure.proxy:443"
    }
    response = client.patch("/api/network", json=update_data)
    assert response.status_code == 401

def test_update_network(client, network_service_override):
    update_data = {
        "proxy_enabled": True,
        "http_proxy": "http://proxy.local:3128",
        "https_proxy": "https://secure.proxy:443"
    }
    response = client.patch("/api/network", headers={"X-API-Key": "test_key"}, json=update_data)
    assert response.status_code == 200
    assert response.json()["proxy_enabled"] is True
    assert response.json()["http_proxy"] == "http://proxy.local:3128"
