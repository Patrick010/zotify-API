import yaml
from unittest.mock import MagicMock, patch, mock_open

import pytest
from zotify_api.core.log_service import LoggingService, BaseLogHandler
from zotify_api.core.logging_handlers.console import ConsoleHandler
from zotify_api.core.logging_handlers.json_audit import JsonAuditHandler

@pytest.fixture(autouse=True)
def clear_singleton():
    """Ensures each test gets a fresh LoggingService instance."""
    if hasattr(LoggingService, '_instance'):
        LoggingService._instance = None
    yield


@patch("zotify_api.core.log_service.LoggingService._load_config", MagicMock())
def test_singleton_pattern():
    """Test that LoggingService is a singleton."""
    instance1 = LoggingService()
    instance2 = LoggingService()
    assert instance1 is instance2

def test_handler_registration_from_config():
    """Test that handlers from a YAML file are registered correctly."""
    yaml_content = """
    handlers:
      - type: console
        class: zotify_api.core.logging_handlers.console.ConsoleHandler
        levels: ["INFO", "WARNING"]
      - type: audit
        class: zotify_api.core.logging_handlers.json_audit.JsonAuditHandler
        filename: "test.log"
    """
    with patch("builtins.open", mock_open(read_data=yaml_content)):
        with patch("pathlib.Path.exists") as mock_exists:
            mock_exists.return_value = True
            with patch("zotify_api.core.logging_handlers.json_audit.Path.mkdir"):
                service = LoggingService()
                assert len(service.handlers) == 2
                assert isinstance(service.handlers[0], ConsoleHandler)
                assert isinstance(service.handlers[1], JsonAuditHandler)


@patch("zotify_api.core.log_service.LoggingService._load_config", MagicMock())
def test_log_dispatching():
    """Test that the service dispatches logs to the correct handlers."""
    handler1 = MagicMock(spec=BaseLogHandler)
    handler1.can_handle.side_effect = lambda level: level == "INFO"

    handler2 = MagicMock(spec=BaseLogHandler)
    handler2.can_handle.side_effect = lambda level: level == "AUDIT"

    # Manually initialize service to inject mock handlers
    service = LoggingService()
    service.handlers = [handler1, handler2]

    service.log("INFO", "This is an info message.")
    handler1.handle.assert_called_once_with("INFO", "This is an info message.", None)
    handler2.handle.assert_not_called()

    handler1.reset_mock()
    handler2.reset_mock()

    service.log("AUDIT", "This is an audit message.", extra={"user": "test"})
    handler1.handle.assert_not_called()
    handler2.handle.assert_called_once_with("AUDIT", "This is an audit message.", {"user": "test"})
