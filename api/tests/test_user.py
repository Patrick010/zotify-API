import pytest
from fastapi.testclient import TestClient
from zotify_api.main import app
from zotify_api.services import user_service

client = TestClient(app)

@pytest.fixture
def user_service_override():
    user_profile = {"name": "Test User", "email": "test@example.com"}
    user_liked = ["track1", "track2"]
    user_history = ["track3", "track4"]
    def get_user_service_override():
        return user_service.UserService(user_profile, user_liked, user_history)
    return get_user_service_override

def test_get_user_profile(user_service_override):
    app.dependency_overrides[user_service.get_user_service] = user_service_override
    response = client.get("/api/user/profile")
    assert response.status_code == 200
    assert response.json()["name"] == "Test User"
    app.dependency_overrides = {}

def test_get_user_liked(user_service_override):
    app.dependency_overrides[user_service.get_user_service] = user_service_override
    response = client.get("/api/user/liked")
    assert response.status_code == 200
    assert response.json()["items"] == ["track1", "track2"]
    app.dependency_overrides = {}

def test_sync_user_liked(user_service_override):
    app.dependency_overrides[user_service.get_user_service] = user_service_override
    response = client.post("/api/user/sync_liked")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    app.dependency_overrides = {}

def test_get_user_history(user_service_override):
    app.dependency_overrides[user_service.get_user_service] = user_service_override
    response = client.get("/api/user/history")
    assert response.status_code == 200
    assert response.json()["items"] == ["track3", "track4"]
    app.dependency_overrides = {}

def test_delete_user_history(user_service_override):
    app.dependency_overrides[user_service.get_user_service] = user_service_override
    response = client.delete("/api/user/history")
    assert response.status_code == 204
    app.dependency_overrides = {}
