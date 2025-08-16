"""
Logging service module.

This module contains the business logic for the logging subsystem.
The functions in this module are designed to be called from the API layer.
"""
from typing import Dict, Any

class LoggingService:
    def __init__(self, log_config: Dict[str, Any]):
        self._log_config = log_config

    def get_logging_config(self) -> Dict[str, Any]:
        return self._log_config

    def update_logging_config(self, update_data: Dict[str, Any]) -> Dict[str, Any]:
        if "level" in update_data and update_data["level"] not in ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]:
            raise ValueError("Invalid log level")
        for k, v in update_data.items():
            self._log_config[k] = v
        return self._log_config

def get_logging_service():
    # This is a placeholder for a real implementation that would get the logging config from a persistent storage.
    log_config = {
        "level": "INFO",
        "log_to_file": False,
        "log_file": None
    }
    return LoggingService(log_config)
