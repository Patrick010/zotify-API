# ID: API-243
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from zotify_api.database import crud
from zotify_api.schemas import user as user_schemas


@pytest.fixture
def test_user(test_db_session: Session):
    user_in = user_schemas.UserCreate(username="testuser", password="password123")
    user = crud.create_user(db=test_db_session, user=user_in)
    return user


def test_get_user_profile(client: TestClient, test_user, get_auth_headers):
    headers = get_auth_headers(client, "testuser", "password123")
    response = client.get("/api/user/profile", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "testuser"
    assert data["email"] is None


def test_update_user_profile(client: TestClient, test_user, get_auth_headers):
    headers = get_auth_headers(client, "testuser", "password123")
    update_data = {"name": "New Name", "email": "new@email.com"}
    response = client.patch("/api/user/profile", headers=headers, json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Name"
    assert data["email"] == "new@email.com"


def test_get_user_preferences(client: TestClient, test_user, get_auth_headers):
    headers = get_auth_headers(client, "testuser", "password123")
    response = client.get("/api/user/preferences", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["theme"] == "dark"
    assert data["language"] == "en"
    assert data["notifications_enabled"] is True  # Check default value


def test_update_user_preferences(client: TestClient, test_user, get_auth_headers):
    headers = get_auth_headers(client, "testuser", "password123")
    update_data = {"theme": "light", "language": "fr", "notifications_enabled": False}
    response = client.patch("/api/user/preferences", headers=headers, json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["theme"] == "light"
    assert data["language"] == "fr"
    assert data["notifications_enabled"] is False


def test_get_user_liked(client: TestClient, test_user, get_auth_headers):
    headers = get_auth_headers(client, "testuser", "password123")
    response = client.get("/api/user/liked", headers=headers)
    assert response.status_code == 200
    assert response.json() == []


def test_add_user_liked(client: TestClient, test_user, get_auth_headers):
    headers = get_auth_headers(client, "testuser", "password123")
    response = client.post("/api/user/liked/track1", headers=headers)
    assert response.status_code == 200
    response = client.get("/api/user/liked", headers=headers)
    assert response.status_code == 200
    assert response.json() == ["track1"]


def test_get_user_history(client: TestClient, test_user, get_auth_headers):
    headers = get_auth_headers(client, "testuser", "password123")
    response = client.get("/api/user/history", headers=headers)
    assert response.status_code == 200
    assert response.json() == []


def test_add_user_history(client: TestClient, test_user, get_auth_headers):
    headers = get_auth_headers(client, "testuser", "password123")
    response = client.post("/api/user/history/track1", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["track_id"] == "track1"


def test_delete_user_history(client: TestClient, test_user, get_auth_headers):
    headers = get_auth_headers(client, "testuser", "password123")
    client.post("/api/user/history/track1", headers=headers)
    response = client.delete("/api/user/history", headers=headers)
    assert response.status_code == 204
    response = client.get("/api/user/history", headers=headers)
    assert response.status_code == 200
    assert response.json() == []
