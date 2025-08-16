import logging
import sys
from typing import Dict, Any, List

from ..log_service import BaseLogHandler

class ConsoleHandler(BaseLogHandler):
    """A log handler that prints messages to the console."""

    def __init__(self, levels: List[str] = None):
        self.levels = levels or ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        self.logger = logging.getLogger("zotify.console")

        # Configure the logger to output to stdout
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                "[%(asctime)s] [%(levelname)s] %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.DEBUG)
            self.logger.propagate = False


    def can_handle(self, level: str) -> bool:
        return level.upper() in self.levels

    def handle(self, level: str, message: str, extra: Dict[str, Any] = None):
        log_level = getattr(logging, level.upper(), logging.INFO)
        self.logger.log(log_level, message, extra=extra)
