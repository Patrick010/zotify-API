from pathlib import Path
from typing import Any, Generator

import pytest
from fastapi.testclient import TestClient

from zotify_api.main import app
from zotify_api.services import config_service


@pytest.fixture
def temp_config_file(tmp_path: Path) -> Generator[Path, None, None]:
    """Fixture to provide a temporary config file path."""
    config_path = tmp_path / "config.json"
    yield config_path
    if config_path.exists():
        config_path.unlink()


@pytest.fixture
def config_service_override(
    temp_config_file: Path,
) -> Generator[None, None, None]:
    """Fixture to override the config service with a temporary storage path."""

    def get_config_service_override() -> config_service.ConfigService:
        return config_service.ConfigService(storage_path=temp_config_file)

    original_override = app.dependency_overrides.get(config_service.get_config_service)
    app.dependency_overrides[config_service.get_config_service] = (
        get_config_service_override
    )
    yield
    app.dependency_overrides[config_service.get_config_service] = original_override


def test_get_config(client: TestClient, config_service_override: Any) -> None:
    response = client.get("/api/config")
    assert response.status_code == 200
    assert "library_path" in response.json()["data"]


def test_update_config_unauthorized(
    client: TestClient, config_service_override: Any
) -> None:
    update_data = {"scan_on_startup": False}
    response = client.patch("/api/config", json=update_data)
    assert response.status_code == 401


def test_update_config(client: TestClient, config_service_override: Any) -> None:
    update_data = {"scan_on_startup": False}
    response = client.patch(
        "/api/config", headers={"X-API-Key": "test_key"}, json=update_data
    )
    assert response.status_code == 200
    assert response.json()["data"]["scan_on_startup"] is False


def test_reset_config_unauthorized(
    client: TestClient, config_service_override: Any
) -> None:
    response = client.post("/api/config/reset")
    assert response.status_code == 401


def test_reset_config(client: TestClient, config_service_override: Any) -> None:
    # First, change the config
    update_data = {"scan_on_startup": False}
    client.patch("/api/config", headers={"X-API-Key": "test_key"}, json=update_data)

    # Then, reset it
    response = client.post("/api/config/reset", headers={"X-API-Key": "test_key"})
    assert response.status_code == 200
    assert response.json()["data"]["scan_on_startup"] is True


def test_update_persists_across_requests(
    client: TestClient, config_service_override: Any
) -> None:
    update_data = {"library_path": "/new/path"}
    client.patch("/api/config", headers={"X-API-Key": "test_key"}, json=update_data)

    response = client.get("/api/config")
    assert response.json()["data"]["library_path"] == "/new/path"


def test_reset_works_after_multiple_updates(
    client: TestClient, config_service_override: Any
) -> None:
    client.patch(
        "/api/config",
        headers={"X-API-Key": "test_key"},
        json={"scan_on_startup": False},
    )
    client.patch(
        "/api/config",
        headers={"X-API-Key": "test_key"},
        json={"library_path": "/another/path"},
    )

    client.post("/api/config/reset", headers={"X-API-Key": "test_key"})
    response = client.get("/api/config")
    assert response.json()["data"]["scan_on_startup"] is True
    assert response.json()["data"]["library_path"] == "/music"


def test_bad_update_fails_gracefully(
    client: TestClient, config_service_override: Any
) -> None:
    # Assuming the model will reject this
    update_data = {"invalid_field": "some_value"}
    response = client.patch(
        "/api/config", headers={"X-API-Key": "test_key"}, json=update_data
    )
    assert response.status_code == 422  # Unprocessable Entity
