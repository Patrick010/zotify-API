import json
import logging
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any

from ..log_service import BaseLogHandler

class JsonAuditHandler(BaseLogHandler):
    """A log handler that writes structured JSON audit logs to a file."""

    def __init__(self, filename: str):
        self.log_file_path = Path(filename)
        # Ensure the directory exists
        self.log_file_path.parent.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger("zotify.audit")
        self.logger.setLevel(logging.INFO) # Use INFO as a proxy for AUDIT level

        if not self.logger.handlers:
            handler = logging.FileHandler(self.log_file_path)
            # The formatter just passes the message through, as we format it ourselves
            handler.setFormatter(logging.Formatter('%(message)s'))
            self.logger.addHandler(handler)
            self.logger.propagate = False

    def can_handle(self, level: str) -> bool:
        return level.upper() == "AUDIT"

    def handle(self, level: str, message: str, extra: Dict[str, Any] = None):
        extra = extra or {}
        log_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_id": str(uuid.uuid4()),
            "event_name": message,
            "user_id": extra.get("user_id"),
            "source_ip": extra.get("source_ip"),
            "details": extra.get("details", {}),
        }
        self.logger.info(json.dumps(log_record))
