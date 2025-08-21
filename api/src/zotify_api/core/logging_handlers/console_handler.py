import logging
import sys
from datetime import datetime
from typing import Any, Dict, List

from .base import BaseLogHandler

log = logging.getLogger(__name__)

class ConsoleHandler(BaseLogHandler):
    """
    A log handler that prints formatted messages to the console (stdout).
    """

    def __init__(self, levels: List[str]):
        self.levels = [level.upper() for level in levels]
        log.debug(f"ConsoleHandler initialized for levels: {self.levels}")

    def can_handle(self, level: str) -> bool:
        return level.upper() in self.levels

    def format(self, log_record: Dict[str, Any]) -> str:
        """Formats the log record into a human-readable string."""
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        level = log_record.get("level", "UNKNOWN").upper()
        message = log_record.get("message", "")
        return f"[{timestamp}] [{level}] {message}"

    def emit(self, log_record: Dict[str, Any]):
        """Prints the formatted log record to stdout."""
        formatted_message = self.format(log_record)
        print(formatted_message, file=sys.stdout)
