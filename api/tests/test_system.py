# ID: API-241
from unittest.mock import MagicMock, mock_open, patch

from fastapi.testclient import TestClient
from pytest import MonkeyPatch

from zotify_api.main import app

client = TestClient(app)


def test_get_system_status_stub(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("zotify_api.config.settings.admin_api_key", "test_key")
    response = client.get("/api/system/status", headers={"X-API-Key": "test_key"})
    assert response.status_code == 501


def test_get_system_storage_stub(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("zotify_api.config.settings.admin_api_key", "test_key")
    response = client.get("/api/system/storage", headers={"X-API-Key": "test_key"})
    assert response.status_code == 501


def test_get_system_logs_stub(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("zotify_api.config.settings.admin_api_key", "test_key")
    response = client.get("/api/system/logs", headers={"X-API-Key": "test_key"})
    assert response.status_code == 501


def test_reload_system_config_stub(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("zotify_api.config.settings.admin_api_key", "test_key")
    response = client.post("/api/system/reload", headers={"X-API-Key": "test_key"})
    assert response.status_code == 501


def test_reset_system_state_stub(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("zotify_api.config.settings.admin_api_key", "test_key")
    response = client.post("/api/system/reset", headers={"X-API-Key": "test_key"})
    assert response.status_code == 501


def test_get_uptime(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("zotify_api.config.settings.admin_api_key", "test_key")
    response = client.get("/api/system/uptime", headers={"X-API-Key": "test_key"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "uptime_seconds" in data["data"]
    assert "uptime_human" in data["data"]


def test_get_env(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("zotify_api.config.settings.admin_api_key", "test_key")
    response = client.get("/api/system/env", headers={"X-API-Key": "test_key"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "version" in data["data"]
    assert "python_version" in data["data"]


def test_get_human_readable_uptime() -> None:
    from zotify_api.routes.system import get_human_readable_uptime

    assert "1d 1h 1m 1s" in get_human_readable_uptime(90061)


@patch("zotify_api.routes.system.get_logging_service")
@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data="logging:\n  default_level: INFO\n  sinks: []",
)
def test_reload_logging_config_success(
    mock_file: MagicMock, mock_get_service: MagicMock, monkeypatch: MonkeyPatch
) -> None:
    monkeypatch.setattr("zotify_api.config.settings.admin_api_key", "test_key")
    mock_service = MagicMock()
    mock_get_service.return_value = mock_service

    response = client.post(
        "/api/system/logging/reload", headers={"X-API-Key": "test_key"}
    )

    assert response.status_code == 202
    assert response.json()["message"] == "Logging framework configuration reloaded."
    mock_service.load_config.assert_called_once()


@patch("builtins.open")
def test_reload_logging_config_file_not_found(
    mock_file: MagicMock, monkeypatch: MonkeyPatch
) -> None:
    monkeypatch.setattr("zotify_api.config.settings.admin_api_key", "test_key")
    mock_file.side_effect = FileNotFoundError
    response = client.post(
        "/api/system/logging/reload", headers={"X-API-Key": "test_key"}
    )
    assert response.status_code == 404


@patch("builtins.open", new_callable=mock_open, read_data="bad: yaml:")
def test_reload_logging_config_yaml_error(
    mock_file: MagicMock, monkeypatch: MonkeyPatch
) -> None:
    monkeypatch.setattr("zotify_api.config.settings.admin_api_key", "test_key")
    response = client.post(
        "/api/system/logging/reload", headers={"X-API-Key": "test_key"}
    )
    assert response.status_code == 400


@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data="logging:\n  default_level: 123\n  sinks: []",
)
def test_reload_logging_config_validation_error(
    mock_file: MagicMock, monkeypatch: MonkeyPatch
) -> None:
    monkeypatch.setattr("zotify_api.config.settings.admin_api_key", "test_key")
    response = client.post(
        "/api/system/logging/reload", headers={"X-API-Key": "test_key"}
    )
    assert response.status_code == 422
