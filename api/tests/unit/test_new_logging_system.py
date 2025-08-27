import contextlib
import json
from io import StringIO
from typing import Any
from unittest.mock import MagicMock, Mock, mock_open, patch

import yaml
from sqlalchemy.orm import Session

from zotify_api.core.logging_handlers.base import BaseLogHandler
from zotify_api.database import models
from zotify_api.services.logging_service import LoggingService

CONFIG_YAML = """
handlers:
  - type: console_handler
    levels: [DEBUG, INFO]
    # Other params for the constructor
  - type: json_audit_handler
    levels: [AUDIT]
    filename: "test_audit.log"
  - type: database_job_handler
    levels: [JOB_STATUS]
"""


@patch("zotify_api.services.logging_service.importlib")
@patch("zotify_api.services.logging_service.yaml")
@patch("builtins.open")
def test_logging_service_initialization(
    mock_open: Mock, mock_yaml: Mock, mock_importlib: Mock
) -> None:
    """Tests that the LoggingService loads all handlers from the config."""
    mock_yaml.safe_load.return_value = yaml.safe_load(CONFIG_YAML)

    # Mock the imported handler classes
    mock_console_handler_class = MagicMock()
    mock_json_handler_class = MagicMock()
    mock_db_handler_class = MagicMock()

    def import_side_effect(module_name: str) -> MagicMock:
        mock_module = MagicMock()
        if "console_handler" in module_name:
            mock_module.ConsoleHandler = mock_console_handler_class
        elif "json_audit_handler" in module_name:
            mock_module.JsonAuditHandler = mock_json_handler_class
        elif "database_job_handler" in module_name:
            mock_module.DatabaseJobHandler = mock_db_handler_class
        return mock_module

    mock_importlib.import_module.side_effect = import_side_effect

    service = LoggingService(config_path="dummy/path.yml")

    assert len(service.handlers) == 3
    mock_console_handler_class.assert_called_once_with(levels=["DEBUG", "INFO"])
    mock_json_handler_class.assert_called_once_with(
        levels=["AUDIT"], filename="test_audit.log"
    )
    mock_db_handler_class.assert_called_once_with(levels=["JOB_STATUS"])


@patch("zotify_api.services.logging_service.importlib")
@patch("zotify_api.services.logging_service.yaml")
@patch("builtins.open")
def test_log_dispatch(mock_open: Mock, mock_yaml: Mock, mock_importlib: Mock) -> None:
    """Tests that the log method dispatches to the correct handlers."""
    mock_yaml.safe_load.return_value = yaml.safe_load(CONFIG_YAML)

    mock_console_handler = MagicMock(spec=BaseLogHandler)
    mock_json_handler = MagicMock(spec=BaseLogHandler)
    mock_db_handler = MagicMock(spec=BaseLogHandler)

    mock_console_handler_class = MagicMock(return_value=mock_console_handler)
    mock_json_handler_class = MagicMock(return_value=mock_json_handler)
    mock_db_handler_class = MagicMock(return_value=mock_db_handler)

    def import_side_effect(module_name: str) -> MagicMock:
        mock_module = MagicMock()
        if "console_handler" in module_name:
            mock_module.ConsoleHandler = mock_console_handler_class
        elif "json_audit_handler" in module_name:
            mock_module.JsonAuditHandler = mock_json_handler_class
        elif "database_job_handler" in module_name:
            mock_module.DatabaseJobHandler = mock_db_handler_class
        return mock_module

    mock_importlib.import_module.side_effect = import_side_effect

    service = LoggingService(config_path="dummy/path.yml")

    mock_console_handler.can_handle.return_value = True
    mock_json_handler.can_handle.return_value = False
    mock_db_handler.can_handle.return_value = False

    service.log("INFO", "test info message")
    mock_console_handler.emit.assert_called_once()
    mock_json_handler.emit.assert_not_called()
    mock_db_handler.emit.assert_not_called()


@patch("sys.stdout", new_callable=StringIO)
def test_console_handler(mock_stdout: Mock) -> None:
    from zotify_api.core.logging_handlers.console_handler import ConsoleHandler

    handler = ConsoleHandler(levels=["INFO"])
    with patch("zotify_api.core.logging_handlers.console_handler.datetime") as mock_dt:
        mock_dt.utcnow.return_value.strftime.return_value = "2025-01-01 12:00:00"
        handler.emit({"level": "INFO", "message": "hello world"})
        output = mock_stdout.getvalue()
        assert output.strip() == "[2025-01-01 12:00:00] [INFO] hello world"


@patch("builtins.open", new_callable=mock_open)
def test_json_audit_handler(mock_file: Mock) -> None:
    from zotify_api.core.logging_handlers.json_audit_handler import JsonAuditHandler

    handler = JsonAuditHandler(levels=["AUDIT"], filename="dummy.log")
    handler.emit(
        {
            "level": "AUDIT",
            "event_name": "test.event",
            "user_id": "user123",
            "source_ip": "127.0.0.1",
            "details": {"foo": "bar"},
        }
    )
    mock_file().write.assert_called_once()
    written_data = mock_file().write.call_args[0][0]
    log_data = json.loads(written_data)
    assert log_data["event_name"] == "test.event"
    assert log_data["user_id"] == "user123"


def test_database_job_handler(test_db_session: Session) -> None:
    from zotify_api.core.logging_handlers.database_job_handler import DatabaseJobHandler

    # We need to patch get_db in the module where it's used
    with patch(
        "zotify_api.core.logging_handlers.database_job_handler.get_db"
    ) as mock_get_db:
        # Make get_db return a context manager that yields the test session
        @contextlib.contextmanager
        def db_context_manager() -> Any:
            yield test_db_session

        mock_get_db.side_effect = db_context_manager

        handler = DatabaseJobHandler(levels=["JOB_STATUS"])

        # Test creating a new job
        handler.emit(
            {
                "level": "JOB_STATUS",
                "job_id": "job-1",
                "job_type": "sync",
                "status": "QUEUED",
            }
        )

        job = (
            test_db_session.query(models.JobLog)
            .filter(models.JobLog.job_id == "job-1")
            .one()
        )
        assert job.status == "QUEUED"
        assert job.job_type == "sync"

        # Test updating a job
        handler.emit(
            {
                "level": "JOB_STATUS",
                "job_id": "job-1",
                "status": "COMPLETED",
                "progress": 100,
            }
        )

        job = (
            test_db_session.query(models.JobLog)
            .filter(models.JobLog.job_id == "job-1")
            .one()
        )
        assert job.status == "COMPLETED"
        assert job.progress == 100
