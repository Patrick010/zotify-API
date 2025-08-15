import logging
import pytest
from zotify_api.core.error_handler import ErrorHandler, initialize_error_handler, get_error_handler, ErrorHandlerConfig
from zotify_api.core.error_handler.formatter import JsonFormatter, PlainTextFormatter

# A mock logger to capture log messages
class MockLogger(logging.Logger):
    def __init__(self, name):
        super().__init__(name)
        self.messages = []
        self.records = []

    def error(self, msg, *args, **kwargs):
        self.messages.append(msg)
        # Create a mock log record. The 'exc_info' key might be in kwargs.
        record = self.makeRecord(self.name, logging.ERROR, "(unknown file)", 0, msg, args, **kwargs)
        self.records.append(record)

@pytest.fixture
def mock_logger():
    return MockLogger("test")

import zotify_api.core.error_handler

@pytest.fixture(autouse=True)
def reset_singleton():
    """Fixture to automatically reset the singleton before and after each test."""
    zotify_api.core.error_handler._error_handler_instance = None
    yield
    zotify_api.core.error_handler._error_handler_instance = None


from unittest.mock import patch

def test_error_handler_initialization():
    """Tests that the ErrorHandler can be initialized."""
    config = ErrorHandlerConfig()
    with patch("zotify_api.core.error_handler.log") as mock_log:
        handler = ErrorHandler(config, mock_log)
        assert handler is not None
        mock_log.info.assert_called_with("Generic Error Handler initialized.")

def test_singleton_pattern(mock_logger):
    """Tests that the singleton pattern works correctly."""
    config = ErrorHandlerConfig()

    handler1 = initialize_error_handler(config, mock_logger)
    handler2 = get_error_handler()

    assert handler1 is handler2

def test_get_handler_before_initialization():
    """Tests that getting the handler before initialization fails."""
    # The autouse reset_singleton fixture ensures the instance is None here.
    with pytest.raises(RuntimeError, match="ErrorHandler has not been initialized"):
        get_error_handler()

def test_double_initialization_fails(mock_logger):
    """Tests that initializing the singleton twice fails."""
    config = ErrorHandlerConfig()
    initialize_error_handler(config, mock_logger) # first time
    with pytest.raises(RuntimeError, match="ErrorHandler has already been initialized"):
        initialize_error_handler(config, mock_logger) # second time

@pytest.mark.parametrize("verbosity, expect_details", [("production", False), ("debug", True)])
def test_json_formatter(verbosity, expect_details):
    """Tests the JsonFormatter in both production and debug modes."""
    formatter = JsonFormatter(verbosity=verbosity)
    exc = ValueError("Test error")
    context = {"request_id": "123", "error_code": "E5000"}

    result = formatter.format(exc, context)

    assert result["error"]["code"] == "E5000"
    assert result["error"]["request_id"] == "123"
    assert "timestamp" in result["error"]

    if expect_details:
        assert "details" in result["error"]
        assert result["error"]["details"]["exception_type"] == "ValueError"
        assert result["error"]["details"]["exception_message"] == "Test error"
        assert "traceback" in result["error"]["details"]
    else:
        assert "details" not in result["error"]

@pytest.mark.parametrize("verbosity, expect_details", [("production", False), ("debug", True)])
def test_plain_text_formatter(verbosity, expect_details):
    """Tests the PlainTextFormatter in both production and debug modes."""
    formatter = PlainTextFormatter(verbosity=verbosity)
    exc = KeyError("Test key error")
    context = {"request_id": "456", "error_code": "E-CLI-1"}

    result = formatter.format(exc, context)

    assert "[E-CLI-1]" in result
    assert "[456]" in result

    if expect_details:
        assert "-- Exception: KeyError: 'Test key error'" in result
        assert "-- Traceback:" in result
    else:
        assert "-- Exception:" not in result
        assert "-- Traceback:" not in result

def test_handler_logs_exception(mock_logger):
    """Tests that the handle_exception method logs the error."""
    config = ErrorHandlerConfig()
    handler = ErrorHandler(config, mock_logger)

    try:
        raise ValueError("A test exception")
    except ValueError as e:
        handler.handle_exception(e)

    assert len(mock_logger.records) == 1
    assert mock_logger.records[0].levelname == "ERROR"
    assert "An unhandled synchronous exception occurred" in mock_logger.records[0].getMessage()
    assert mock_logger.records[0].exc_info is not None
