from fastapi.testclient import TestClient
from zotify_api.main import app

client = TestClient(app)

def test_get_network():
    response = client.get("/api/network")
    assert response.status_code == 200
    assert "proxy_enabled" in response.json()

def test_update_network():
    update_data = {
        "proxy_enabled": True,
        "http_proxy": "http://proxy.local:3128",
        "https_proxy": "https://secure.proxy:443"
    }
    response = client.patch("/api/network", json=update_data)
    assert response.status_code == 200
    assert response.json()["proxy_enabled"] is True
    assert response.json()["http_proxy"] == "http://proxy.local:3128"
