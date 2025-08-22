from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from zotify_api.main import app
from zotify_api.routes import sync

client = TestClient(app)


def test_trigger_sync_unauthorized(monkeypatch):
    monkeypatch.setattr("zotify_api.config.settings.admin_api_key", "test_key")
    response = client.post("/api/sync/trigger", headers={"X-API-Key": "wrong_key"})
    assert response.status_code == 401


def test_trigger_sync(monkeypatch):
    monkeypatch.setattr("zotify_api.config.settings.admin_api_key", "test_key")
    mock_runner = MagicMock()

    def get_sync_runner_override():
        return mock_runner

    app.dependency_overrides[sync.get_sync_runner] = get_sync_runner_override
    response = client.post("/api/sync/trigger", headers={"X-API-Key": "test_key"})
    assert response.status_code == 202
    assert response.json() == {
        "status": "success",
        "message": "Synchronization job triggered.",
    }
    mock_runner.assert_called_once()
    app.dependency_overrides = {}


def test_trigger_sync_runner_fails(monkeypatch):
    monkeypatch.setattr("zotify_api.config.settings.admin_api_key", "test_key")
    mock_runner = MagicMock(side_effect=Exception("Sync failed"))

    def get_sync_runner_override():
        return mock_runner

    app.dependency_overrides[sync.get_sync_runner] = get_sync_runner_override
    response = client.post("/api/sync/trigger", headers={"X-API-Key": "test_key"})
    assert response.status_code == 500
    assert "Sync failed" in response.text
    app.dependency_overrides = {}
