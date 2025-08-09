import pytest
from zotify_api.main import app
from zotify_api.services import logging_service

@pytest.fixture
def logging_service_override():
    """Fixture to override the logging service with a predictable state."""
    log_config = {
        "level": "INFO",
        "log_to_file": False,
        "log_file": None
    }
    def get_logging_service_override():
        return logging_service.LoggingService(log_config)

    original_override = app.dependency_overrides.get(logging_service.get_logging_service)
    app.dependency_overrides[logging_service.get_logging_service] = get_logging_service_override
    yield
    app.dependency_overrides[logging_service.get_logging_service] = original_override


def test_get_logging(client, logging_service_override):
    response = client.get("/api/logging")
    assert response.status_code == 200
    assert "level" in response.json()

def test_update_logging_unauthorized(client, logging_service_override):
    update_data = {"level": "DEBUG"}
    response = client.patch("/api/logging", json=update_data)
    assert response.status_code == 401

def test_update_logging(client, logging_service_override):
    update_data = {"level": "DEBUG"}
    response = client.patch("/api/logging", headers={"X-API-Key": "test_key"}, json=update_data)
    assert response.status_code == 200
    assert response.json()["level"] == "DEBUG"

def test_update_logging_invalid_level(client, logging_service_override):
    update_data = {"level": "INVALID"}
    response = client.patch("/api/logging", headers={"X-API-Key": "test_key"}, json=update_data)
    assert response.status_code == 400
