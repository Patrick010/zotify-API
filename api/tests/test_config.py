from fastapi.testclient import TestClient
from zotify_api.main import app

client = TestClient(app)

def test_get_config():
    response = client.get("/api/config")
    assert response.status_code == 200
    assert "library_path" in response.json()

def test_update_config():
    update_data = {"scan_on_startup": False}
    response = client.patch("/api/config", json=update_data)
    assert response.status_code == 200
    assert response.json()["scan_on_startup"] is False

def test_reset_config():
    # First, change the config
    update_data = {"scan_on_startup": False}
    client.patch("/api/config", json=update_data)

    # Then, reset it
    response = client.post("/api/config/reset")
    assert response.status_code == 200
    assert response.json()["scan_on_startup"] is True
