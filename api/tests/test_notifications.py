# ID: API-239
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from zotify_api.database import crud
from zotify_api.schemas import user as user_schemas, notifications as notification_schemas


@pytest.fixture
def test_user(test_db_session: Session):
    user_in = user_schemas.UserCreate(username="testuser", password="password123")
    user = crud.create_user(db=test_db_session, user=user_in)
    user.role = "admin"
    test_db_session.commit()
    test_db_session.refresh(user)
    return user


def test_create_notification(client: TestClient, test_user, get_auth_headers):
    headers = get_auth_headers(client, "testuser", "password123")
    response = client.post(
        "/api/notifications",
        headers=headers,
        json={"user_id": test_user.id, "message": "Test message"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Test message"


def test_get_notifications(client: TestClient, test_user, get_auth_headers):
    headers = get_auth_headers(client, "testuser", "password123")
    client.post(
        "/api/notifications",
        headers=headers,
        json={"user_id": test_user.id, "message": "Test message"},
    )
    response = client.get("/api/notifications", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["message"] == "Test message"


def test_mark_notification_as_read(client: TestClient, test_user, get_auth_headers):
    headers = get_auth_headers(client, "testuser", "password123")
    create_response = client.post(
        "/api/notifications",
        headers=headers,
        json={"user_id": test_user.id, "message": "Test message"},
    )
    notification_id = create_response.json()["id"]
    response = client.patch(
        f"/api/notifications/{notification_id}",
        headers=headers,
        json={"read": True},
    )
    assert response.status_code == 204

    notifications = client.get("/api/notifications", headers=headers).json()
    assert notifications[0]["read"] is True
