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


def test_register_user(client: TestClient, test_db_session: Session):
    response = client.post(
        "/api/auth/register",
        json={"username": "newuser", "password": "newpassword"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["msg"] == "User registered successfully"


def test_register_duplicate_user(client: TestClient, test_user):
    response = client.post(
        "/api/auth/register",
        json={"username": "testuser", "password": "password123"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"


def test_login_for_access_token(client: TestClient, test_user):
    response = client.post(
        "/api/auth/login",
        data={"username": "testuser", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client: TestClient, test_user):
    response = client.post(
        "/api/auth/login",
        data={"username": "testuser", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


def get_auth_headers(client: TestClient, username, password):
    response = client.post(
        "/api/auth/login",
        data={"username": username, "password": password},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_user_endpoints_unauthorized(client: TestClient):
    response = client.get("/api/user/profile")
    assert response.status_code == 401
    response = client.get("/api/user/preferences")
    assert response.status_code == 401
    response = client.get("/api/user/liked")
    assert response.status_code == 401
    response = client.get("/api/user/history")
    assert response.status_code == 401


def test_user_endpoints_invalid_token(client: TestClient):
    headers = {"Authorization": "Bearer invalidtoken"}
    response = client.get("/api/user/profile", headers=headers)
    assert response.status_code == 401
    response = client.get("/api/user/preferences", headers=headers)
    assert response.status_code == 401
    response = client.get("/api/user/liked", headers=headers)
    assert response.status_code == 401
    response = client.get("/api/user/history", headers=headers)
    assert response.status_code == 401


def test_get_user_profile(client: TestClient, test_user):
    headers = get_auth_headers(client, "testuser", "password123")
    response = client.get("/api/user/profile", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "testuser"


def test_update_user_profile(client: TestClient, test_user):
    headers = get_auth_headers(client, "testuser", "password123")
    response = client.patch(
        "/api/user/profile",
        headers=headers,
        json={"name": "newname", "email": "new@email.com"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "newname"
    assert data["email"] == "new@email.com"


def test_get_user_preferences(client: TestClient, test_user):
    headers = get_auth_headers(client, "testuser", "password123")
    response = client.get("/api/user/preferences", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["theme"] == "dark"
    assert data["language"] == "en"


def test_update_user_preferences(client: TestClient, test_user):
    headers = get_auth_headers(client, "testuser", "password123")
    response = client.patch(
        "/api/user/preferences",
        headers=headers,
        json={"theme": "light", "language": "fr"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["theme"] == "light"
    assert data["language"] == "fr"


def test_liked_songs(client: TestClient, test_user):
    headers = get_auth_headers(client, "testuser", "password123")
    response = client.get("/api/user/liked", headers=headers)
    assert response.status_code == 200
    assert response.json() == []

    response = client.post("/api/user/liked/track1", headers=headers)
    assert response.status_code == 200
    response = client.get("/api/user/liked", headers=headers)
    assert response.status_code == 200
    assert response.json() == ["track1"]


def test_history(client: TestClient, test_user):
    headers = get_auth_headers(client, "testuser", "password123")
    response = client.get("/api/user/history", headers=headers)
    assert response.status_code == 200
    assert response.json() == []

    response = client.post("/api/user/history/track1", headers=headers)
    assert response.status_code == 200
    response = client.get("/api/user/history", headers=headers)
    assert response.status_code == 200
    assert response.json() == ["track1"]

    response = client.delete("/api/user/history", headers=headers)
    assert response.status_code == 204
    response = client.get("/api/user/history", headers=headers)
    assert response.status_code == 200
    assert response.json() == []
