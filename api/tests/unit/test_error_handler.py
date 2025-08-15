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
        # Create a mock log record
        record = self.makeRecord(self.name, logging.ERROR, "(unknown file)", 0, msg, args, kwargs.get('exc_info'), **kwargs)
        self.records.append(record)

@pytest.fixture
def mock_logger():
    return MockLogger("test")

@pytest.fixture(autouse=True)
def reset_singleton():
    """Fixture to automatically reset the singleton before and after each test."""
    # Before the test
    from zotify_api.core.error_handler import _error_handler_instance
    _error_handler_instance = None

    yield

    # After the test
    from zotify_api.core.error_handler import _error_handler_instance
    _error_handler_instance = None


def test_error_handler_initialization(mock_logger):
    """Tests that the ErrorHandler can be initialized."""
    config = ErrorHandlerConfig()
    handler = ErrorHandler(config, mock_logger)
    assert handler is not None
    assert "Generic Error Handler initialized." in mock_logger.messages

def test_singleton_pattern(mock_logger):
    """Tests that the singleton pattern works correctly."""
    config = ErrorHandlerConfig()

    handler1 = initialize_error_handler(config, mock_logger)
    handler2 = get_error_handler()

    assert handler1 is handler2

    # Test that trying to get without initializing fails
    reset_singleton() # manually call fixture logic to reset
    with pytest.raises(RuntimeError):
        get_error_handler()

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
