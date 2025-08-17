from typing import Optional, List

from .service import get_logging_service

def log_event(
    message: str,
    level: str = "INFO",
    destinations: Optional[List[str]] = None,
    **extra
):
    """
    Public API for the flexible logging framework.

    Developers should use this function to log events. It provides a stable
    interface that is decoupled from the underlying service implementation.

    Args:
        message: The log message.
        level: The severity level (e.g., "INFO", "DEBUG").
        destinations: A list of specific sink names to send this log to.
                      If None, logs to all sinks that meet the level threshold.
        **extra: Additional key-value pairs to include in the structured log.
    """
    service = get_logging_service()
    service.log(message, level=level, destinations=destinations, **extra)

# This makes `from zotify_api.core.logging_framework import log_event` possible.
__all__ = ["log_event"]
