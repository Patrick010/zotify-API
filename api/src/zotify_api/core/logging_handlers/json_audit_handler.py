import json
import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List

from .base import BaseLogHandler

log = logging.getLogger(__name__)

class JsonAuditHandler(BaseLogHandler):
    """
    A log handler that writes structured JSON audit logs to a file.
    """

    def __init__(self, levels: List[str], filename: str):
        self.levels = [level.upper() for level in levels]
        self.filename = filename
        log.debug(
            "JsonAuditHandler initialized for levels: %s -> %s",
            self.levels,
            self.filename,
        )

    def can_handle(self, level: str) -> bool:
        return level.upper() in self.levels

    def format(self, log_record: Dict[str, Any]) -> str:
        """Formats the log record into a JSON string with all mandatory audit fields."""
        audit_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_id": str(uuid.uuid4()),
            "event_name": log_record.get("event_name", "undefined.event"),
            "user_id": log_record.get("user_id"),
            "source_ip": log_record.get("source_ip"),
            "details": log_record.get("details", {})
        }
        return json.dumps(audit_record)

    def emit(self, log_record: Dict[str, Any]):
        """Appends the formatted JSON log record to the audit log file."""
        formatted_message = self.format(log_record)
        try:
            with open(self.filename, "a") as f:
                f.write(formatted_message + "\n")
        except Exception:
            log.exception(f"Failed to write to audit log file: {self.filename}")
