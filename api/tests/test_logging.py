import pytest
from fastapi.testclient import TestClient
from zotify_api.main import app
from zotify_api.services import logging_service

client = TestClient(app)

@pytest.fixture
def logging_service_override():
    log_config = {
        "level": "INFO",
        "log_to_file": False,
        "log_file": None
    }
    def get_logging_service_override():
        return logging_service.LoggingService(log_config)
    return get_logging_service_override

def test_get_logging(logging_service_override):
    app.dependency_overrides[logging_service.get_logging_service] = logging_service_override
    response = client.get("/api/logging")
    assert response.status_code == 200
    assert "level" in response.json()
    app.dependency_overrides = {}

def test_update_logging_unauthorized(logging_service_override):
    app.dependency_overrides[logging_service.get_logging_service] = logging_service_override
    update_data = {"level": "DEBUG"}
    response = client.patch("/api/logging", json=update_data)
    assert response.status_code == 401
    app.dependency_overrides = {}

def test_update_logging(logging_service_override, monkeypatch):
    monkeypatch.setattr("zotify_api.config.settings.admin_api_key", "test_key")
    app.dependency_overrides[logging_service.get_logging_service] = logging_service_override
    update_data = {"level": "DEBUG"}
    response = client.patch("/api/logging", headers={"X-API-Key": "test_key"}, json=update_data)
    assert response.status_code == 200
    assert response.json()["level"] == "DEBUG"
    app.dependency_overrides = {}

def test_update_logging_invalid_level(logging_service_override, monkeypatch):
    monkeypatch.setattr("zotify_api.config.settings.admin_api_key", "test_key")
    app.dependency_overrides[logging_service.get_logging_service] = logging_service_override
    update_data = {"level": "INVALID"}
    response = client.patch("/api/logging", headers={"X-API-Key": "test_key"}, json=update_data)
    assert response.status_code == 400
    app.dependency_overrides = {}
