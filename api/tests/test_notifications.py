import pytest
from fastapi.testclient import TestClient
from zotify_api.main import app
from zotify_api.services import user_service

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_notifications(monkeypatch):
    monkeypatch.setattr("zotify_api.services.user_service.STORAGE_FILE", Path("test_user_data.json"))
    monkeypatch.setattr("zotify_api.config.settings.admin_api_key", "test_key")
    user_data = {
        "profile": {"name": "Test User", "email": "test@example.com"},
        "liked": [],
        "history": [],
        "preferences": {},
        "notifications": [],
    }
    with open("test_user_data.json", "w") as f:
        json.dump(user_data, f)
    yield
    if Path("test_user_data.json").exists():
        Path("test_user_data.json").unlink()

def test_create_notification():
    response = client.post("/api/notifications", json={"user_id": "user1", "message": "Test message"})
    assert response.status_code == 200
    assert response.json()["message"] == "Test message"

def test_get_notifications():
    client.post("/api/notifications", json={"user_id": "user1", "message": "Test message"})
    response = client.get("/api/notifications/user1")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["message"] == "Test message"

def test_mark_notification_as_read():
    create_response = client.post("/api/notifications", json={"user_id": "user1", "message": "Test message"})
    notification_id = create_response.json()["id"]
    response = client.patch(f"/api/notifications/{notification_id}", json={"read": True})
    assert response.status_code == 204

    notifications = client.get("/api/notifications/user1").json()
    assert notifications[0]["read"] is True
