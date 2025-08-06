import pytest
from fastapi.testclient import TestClient
from zotify_api.main import app
from zotify_api.services import user_service
from pathlib import Path
import json

client = TestClient(app)

@pytest.fixture
def notifications_service_override(tmp_path, monkeypatch):
    user_data_path = tmp_path / "user_data.json"
    monkeypatch.setattr(user_service, "STORAGE_FILE", user_data_path)
    def get_user_service_override():
        return user_service.get_user_service()
    return get_user_service_override

def test_create_notification(notifications_service_override):
    app.dependency_overrides[user_service.get_user_service] = notifications_service_override
    response = client.post("/api/notifications", json={"user_id": "user1", "message": "Test message"})
    assert response.status_code == 200
    assert response.json()["message"] == "Test message"
    app.dependency_overrides = {}

def test_get_notifications(notifications_service_override):
    app.dependency_overrides[user_service.get_user_service] = notifications_service_override
    client.post("/api/notifications", json={"user_id": "user1", "message": "Test message"})
    response = client.get("/api/notifications/user1")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["message"] == "Test message"
    app.dependency_overrides = {}

def test_mark_notification_as_read(notifications_service_override):
    app.dependency_overrides[user_service.get_user_service] = notifications_service_override
    create_response = client.post("/api/notifications", json={"user_id": "user1", "message": "Test message"})
    notification_id = create_response.json()["id"]
    response = client.patch(f"/api/notifications/{notification_id}", json={"read": True})
    assert response.status_code == 204

    notifications = client.get("/api/notifications/user1").json()
    assert notifications[0]["read"] is True
    app.dependency_overrides = {}
