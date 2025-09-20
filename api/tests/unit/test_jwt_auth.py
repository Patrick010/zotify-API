import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from zotify_api.database import crud
from zotify_api.database.models import User
from zotify_api.schemas.user import UserCreate


from zotify_api.services import user_service


@pytest.fixture(autouse=True)
def clear_users():
    """
    Clear in-memory or test DB users before each test.
    Adjust if using database integration.
    """
    user_service.clear_all_users()
    yield
    user_service.clear_all_users()


@pytest.fixture(scope="function")
def test_user(test_db_session: Session):
    """Create a test user in the database."""
    user_in = UserCreate(username="testuser", password="password123")
    user = crud.create_user(db=test_db_session, user=user_in)
    user_service.create_user(
        "testuser",
        {
            "profile": {"name": "testuser", "email": ""},
            "liked": [],
            "history": [],
            "preferences": {"theme": "dark", "language": "en"},
            "notifications": [],
        },
    )
    return {"id": str(user.id), "username": user.username, "password": "password123"}


def test_register_user(client: TestClient, test_db_session: Session):
    response = client.post("/api/auth/register", json={"username": "newuser", "password": "newpassword"})
    assert response.status_code == 201
    data = response.json()
    assert data["msg"] == "User registered successfully"
    db_user = test_db_session.query(User).filter(User.username == "newuser").first()
    assert db_user is not None


def test_register_duplicate_user(client: TestClient, test_user):
    response = client.post("/api/auth/register", json={"username": test_user["username"], "password": "password123"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"


def test_login_for_access_token(client: TestClient, test_user):
    response = client.post(
        "/api/auth/login",
        data={"username": test_user["username"], "password": test_user["password"]},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client: TestClient, test_user):
    response = client.post(
        "/api/auth/login",
        data={"username": test_user["username"], "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


def test_get_profile_with_valid_token(client: TestClient, test_user):
    login_response = client.post(
        "/api/auth/login",
        data={"username": test_user["username"], "password": test_user["password"]},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    profile_response = client.get("/api/user/profile", headers=headers)
    assert profile_response.status_code == 200
    data = profile_response.json()["data"]
    assert data["name"] == test_user["username"]


def test_get_profile_with_invalid_token(client: TestClient):
    headers = {"Authorization": "Bearer invalidtoken"}
    response = client.get("/api/user/profile", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"


def test_get_profile_without_token(client: TestClient):
    response = client.get("/api/user/profile")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_get_own_notifications(client: TestClient, test_user):
    login_response = client.post(
        "/api/auth/login",
        data={"username": test_user["username"], "password": test_user["password"]},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(f"/api/notifications/{test_user['id']}", headers=headers)
    assert response.status_code == 200


def test_get_other_user_notifications(client: TestClient, test_db_session: Session, test_user):
    # Create another user
    other_user_in = UserCreate(username="otheruser", password="password123")
    other_user = crud.create_user(db=test_db_session, user=other_user_in)

    # Log in as test_user
    login_response = client.post(
        "/api/auth/login",
        data={"username": test_user["username"], "password": test_user["password"]},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Attempt to get other_user's notifications
    response = client.get(f"/api/notifications/{other_user.id}", headers=headers)
    assert response.status_code == 403
    assert response.json()["detail"] == "Not authorized to access these notifications"


def test_get_liked_with_valid_token(client: TestClient, test_user):
    login_response = client.post(
        "/api/auth/login",
        data={"username": test_user["username"], "password": test_user["password"]},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/user/liked", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "data" in data


def test_get_liked_without_token(client: TestClient):
    response = client.get("/api/user/liked")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_get_history_with_valid_token(client: TestClient, test_user):
    login_response = client.post(
        "/api/auth/login",
        data={"username": test_user["username"], "password": test_user["password"]},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/user/history", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "data" in data


def test_get_history_without_token(client: TestClient):
    response = client.get("/api/user/history")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_get_preferences_with_valid_token(client: TestClient, test_user):
    login_response = client.post(
        "/api/auth/login",
        data={"username": test_user["username"], "password": test_user["password"]},
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/user/preferences", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "data" in data


def test_get_preferences_without_token(client: TestClient):
    response = client.get("/api/user/preferences")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
