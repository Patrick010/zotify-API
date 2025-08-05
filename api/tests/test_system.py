from fastapi.testclient import TestClient
from zotify_api.main import app

client = TestClient(app)

def test_get_system_info():
    """ Test for GET /system """
    response = client.get("/api/system")
    assert response.status_code == 200
    response_json = response.json()
    assert "status" in response_json
    assert "free_space" in response_json
    assert "total_space" in response_json
    assert "logs" in response_json

def test_get_system_status_stub():
    response = client.get("/api/system/status")
    assert response.status_code == 200

def test_get_system_storage_stub():
    response = client.get("/api/system/storage")
    assert response.status_code == 200

def test_get_system_logs_stub():
    response = client.get("/api/system/logs")
    assert response.status_code == 200

def test_reload_system_config_stub():
    response = client.post("/api/system/reload")
    assert response.status_code == 200

def test_reset_system_state_stub():
    response = client.post("/api/system/reset")
    assert response.status_code == 200
