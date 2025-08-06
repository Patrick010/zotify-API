import pytest
from fastapi.testclient import TestClient
from zotify_api.main import app

client = TestClient(app)

def test_trigger_sync_unauthorized(monkeypatch):
    monkeypatch.setattr("zotify_api.config.settings.enable_fork_features", True)
    monkeypatch.setattr("zotify_api.config.settings.feature_sync_automation", True)
    monkeypatch.setattr("zotify_api.config.settings.admin_api_key", "test_key")
    response = client.post("/api/sync/trigger", headers={"X-API-Key": "wrong_key"})
    assert response.status_code == 401

def test_trigger_sync(monkeypatch):
    monkeypatch.setattr("zotify_api.config.settings.enable_fork_features", True)
    monkeypatch.setattr("zotify_api.config.settings.feature_sync_automation", True)
    monkeypatch.setattr("zotify_api.config.settings.admin_api_key", "test_key")
    monkeypatch.setattr("zotify_api.services.sync.run_sync_job", lambda: None)
    response = client.post("/api/sync/trigger", headers={"X-API-Key": "test_key"})
    assert response.status_code == 200
    assert response.json() == {"status": "scheduled"}
