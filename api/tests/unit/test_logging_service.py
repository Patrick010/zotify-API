import pytest
from zotify_api.services.logging_service import LoggingService

@pytest.fixture
def log_config():
    return {
        "level": "INFO",
        "log_to_file": False,
        "log_file": None
    }

def test_get_logging_config(log_config):
    service = LoggingService(log_config)
    config = service.get_logging_config()
    assert config == log_config

def test_update_logging_config(log_config):
    service = LoggingService(log_config)
    update_data = {"level": "DEBUG"}
    config = service.update_logging_config(update_data)
    assert config["level"] == "DEBUG"

def test_update_logging_config_invalid_level(log_config):
    service = LoggingService(log_config)
    update_data = {"level": "INVALID"}
    with pytest.raises(ValueError, match="Invalid log level"):
        service.update_logging_config(update_data)
