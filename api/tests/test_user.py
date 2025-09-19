import json
from pathlib import Path
from typing import Any, Callable, Dict, Generator, List

import pytest
from fastapi.testclient import TestClient

from zotify_api.main import app
from zotify_api.services import user_service

client = TestClient(app)


@pytest.fixture
def user_service_override(
    tmp_path: Path,
) -> Generator[Callable[[], user_service.UserService], None, None]:
    user_data_path = tmp_path / "user_data.json"
    user_profile = {"name": "Test User", "email": "test@example.com"}
    user_liked = ["track1", "track2"]
    user_history = ["track3", "track4"]
    user_preferences = {"theme": "dark", "language": "en"}
    notifications: List[Dict[str, Any]] = []

    def get_user_service_override() -> user_service.UserService:
        with open(user_data_path, "w") as f:
            json.dump(
                {
                    "profile": user_profile,
                    "liked": user_liked,
                    "history": user_history,
                    "preferences": user_preferences,
                    "notifications": notifications,
                },
                f,
            )
        return user_service.UserService(
            user_profile=user_profile,
            user_liked=user_liked,
            user_history=user_history,
            user_preferences=user_preferences,
            notifications=notifications,
        )

    original_storage_file = user_service.STORAGE_FILE
    user_service.STORAGE_FILE = user_data_path
    yield get_user_service_override
    user_service.STORAGE_FILE = original_storage_file


def test_get_user_profile(
    user_service_override: Callable[[], user_service.UserService],
) -> None:
    app.dependency_overrides[user_service.get_user_service] = user_service_override
    response = client.get("/api/user/profile")
    assert response.status_code == 200
    assert response.json()["data"]["name"] == "Test User"
    app.dependency_overrides = {}


def test_get_user_liked(
    user_service_override: Callable[[], user_service.UserService],
) -> None:
    app.dependency_overrides[user_service.get_user_service] = user_service_override
    response = client.get("/api/user/liked")
    assert response.status_code == 200
    assert response.json()["data"] == ["track1", "track2"]
    app.dependency_overrides = {}


def test_sync_user_liked(
    user_service_override: Callable[[], user_service.UserService],
) -> None:
    app.dependency_overrides[user_service.get_user_service] = user_service_override
    response = client.post("/api/user/sync_liked")
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "ok"
    app.dependency_overrides = {}


def test_get_user_history(
    user_service_override: Callable[[], user_service.UserService],
) -> None:
    app.dependency_overrides[user_service.get_user_service] = user_service_override
    response = client.get("/api/user/history")
    assert response.status_code == 200
    assert response.json()["data"] == ["track3", "track4"]
    app.dependency_overrides = {}


def test_delete_user_history(
    user_service_override: Callable[[], user_service.UserService],
) -> None:
    app.dependency_overrides[user_service.get_user_service] = user_service_override
    response = client.delete("/api/user/history")
    assert response.status_code == 204
    app.dependency_overrides = {}


def test_update_user_profile(
    user_service_override: Callable[[], user_service.UserService],
) -> None:
    app.dependency_overrides[user_service.get_user_service] = user_service_override
    update_data = {"name": "New Name"}
    response = client.patch("/api/user/profile", json=update_data)
    assert response.status_code == 200
    assert response.json()["data"]["name"] == "New Name"
    app.dependency_overrides = {}


def test_get_user_preferences(
    user_service_override: Callable[[], user_service.UserService],
) -> None:
    app.dependency_overrides[user_service.get_user_service] = user_service_override
    response = client.get("/api/user/preferences")
    assert response.status_code == 200
    assert response.json()["data"]["theme"] == "dark"
    app.dependency_overrides = {}


def test_update_user_preferences(
    user_service_override: Callable[[], user_service.UserService],
) -> None:
    app.dependency_overrides[user_service.get_user_service] = user_service_override
    update_data = {"theme": "light"}
    response = client.patch("/api/user/preferences", json=update_data)
    assert response.status_code == 200
    assert response.json()["data"]["theme"] == "light"
    app.dependency_overrides = {}
