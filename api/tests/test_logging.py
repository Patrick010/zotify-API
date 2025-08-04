from fastapi.testclient import TestClient
from zotify_api.main import app

client = TestClient(app)

def test_get_logging():
    response = client.get("/api/logging")
    assert response.status_code == 200
    assert "level" in response.json()

def test_update_logging():
    update_data = {"level": "DEBUG"}
    response = client.patch("/api/logging", json=update_data)
    assert response.status_code == 200
    assert response.json()["level"] == "DEBUG"

def test_update_logging_invalid_level():
    update_data = {"level": "INVALID"}
    response = client.patch("/api/logging", json=update_data)
    assert response.status_code == 400
