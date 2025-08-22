import asyncio
import unittest.mock
from typing import Any, Dict

import pytest
import yaml
from pydantic import ValidationError

from zotify_api.core.logging_framework.schemas import LoggingFrameworkConfig
from zotify_api.core.logging_framework.service import (
    LoggingService,
    get_logging_service,
)

# A valid YAML configuration for testing
VALID_CONFIG_YAML = """
logging:
  default_level: "INFO"
  sinks:
    - name: "test_console"
      type: "console"
      level: "INFO"
    - name: "test_file"
      type: "file"
      level: "DEBUG"
      path: "/tmp/test.log"
    - name: "test_webhook"
      type: "webhook"
      level: "ERROR"
      url: "http://test.com/webhook"
triggers:
  - event: "test_event"
    action: "forward"
    details:
      message: "Triggered event!"
      level: "WARNING"
      destinations: ["test_console"]
"""

# An invalid YAML configuration
INVALID_CONFIG_YAML = """
logging:
  sinks:
    - name: "bad_sink"
      type: "unknown_type"
"""


@pytest.fixture
def logging_service() -> LoggingService:
    """Fixture to get a clean logging service instance for each test."""
    service = get_logging_service()
    # Reset for isolation, as it's a singleton
    service.sinks = {}
    service.config = None
    return service


@pytest.fixture
def valid_config() -> Dict[str, Any]:
    """Fixture to provide a parsed valid config."""
    return yaml.safe_load(VALID_CONFIG_YAML)


def test_config_validation_success(valid_config):
    """Tests that a valid config is parsed correctly by Pydantic."""
    config = LoggingFrameworkConfig(**valid_config)
    assert len(config.logging.sinks) == 3
    assert len(config.triggers) == 1
    assert config.logging.sinks[0].name == "test_console"


def test_config_validation_failure():
    """Tests that an invalid config raises a ValidationError."""
    with pytest.raises(ValidationError):
        LoggingFrameworkConfig(**yaml.safe_load(INVALID_CONFIG_YAML))


@pytest.mark.asyncio
async def test_log_routing_no_destination(logging_service, valid_config, mocker):
    """Tests that a log event with no destination goes to all applicable sinks."""
    mocker.patch("asyncio.create_task")
    config = LoggingFrameworkConfig(**valid_config)
    logging_service.load_config(config)

    # Mock the emit methods on the sinks
    for sink in logging_service.sinks.values():
        mocker.patch.object(sink, "emit", new_callable=unittest.mock.AsyncMock)

    # Log an ERROR event, which should go to all three sinks
    logging_service.log("test error", level="ERROR")
    await asyncio.sleep(0)  # Allow tasks to be scheduled

    assert logging_service.sinks["test_console"].emit.call_count == 1
    assert logging_service.sinks["test_file"].emit.call_count == 1
    assert logging_service.sinks["test_webhook"].emit.call_count == 1

    # Log a DEBUG event, which should only go to the file sink
    logging_service.log("test debug", level="DEBUG")
    await asyncio.sleep(0)

    assert logging_service.sinks["test_console"].emit.call_count == 1  # No new call
    assert logging_service.sinks["test_file"].emit.call_count == 2  # New call
    assert logging_service.sinks["test_webhook"].emit.call_count == 1  # No new call


@pytest.mark.asyncio
async def test_log_routing_with_destination(logging_service, valid_config, mocker):
    """Tests that a log event with a specific destination is routed correctly."""
    mocker.patch("asyncio.create_task")
    config = LoggingFrameworkConfig(**valid_config)
    logging_service.load_config(config)

    for sink in logging_service.sinks.values():
        mocker.patch.object(sink, "emit", new_callable=unittest.mock.AsyncMock)

    # Log specifically to the webhook sink
    logging_service.log(
        "critical failure", level="CRITICAL", destinations=["test_webhook"]
    )
    await asyncio.sleep(0)

    assert logging_service.sinks["test_console"].emit.call_count == 0
    assert logging_service.sinks["test_file"].emit.call_count == 0
    assert logging_service.sinks["test_webhook"].emit.call_count == 1


@pytest.mark.asyncio
async def test_trigger_handling(logging_service, valid_config, mocker):
    """Tests that a log event with an 'event' key correctly fires a trigger."""
    mocker.patch("asyncio.create_task")
    config = LoggingFrameworkConfig(**valid_config)
    logging_service.load_config(config)

    # Mock the log method itself to spy on the recursive call
    mocker.spy(logging_service, "log")

    # Mock the emit methods to check the final output
    for sink in logging_service.sinks.values():
        mocker.patch.object(sink, "emit", new_callable=unittest.mock.AsyncMock)

    # This log should trigger a new log event
    logging_service.log("original message", level="INFO", event="test_event")
    await asyncio.sleep(0)

    # Check that log was called twice: once for the original, once for the trigger
    assert logging_service.log.call_count == 2

    # Check the details of the second (triggered) call, which is at index 1
    triggered_call_args = logging_service.log.call_args_list[1].kwargs
    assert triggered_call_args["message"] == "Triggered event!"
    assert triggered_call_args["level"] == "WARNING"
    assert triggered_call_args["destinations"] == ["test_console"]

    # Check that the triggered event was routed correctly to the console sink
    await asyncio.sleep(0)  # allow emit to be called
    assert logging_service.sinks["test_console"].emit.call_count == 1
    assert logging_service.sinks["test_file"].emit.call_count == 0
    assert logging_service.sinks["test_webhook"].emit.call_count == 0


# Note: Testing the reload API endpoint would typically be done in an integration
# test file using TestClient, not a unit test file, as it involves the
# FastAPI routing layer. For this task, we assume the logic within the endpoint
# is tested via unit tests of the service's `load_config` method.
