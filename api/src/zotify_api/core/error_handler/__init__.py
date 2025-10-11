# ID: API-027
import logging
from typing import Any, Dict, Optional

from .config import ErrorHandlerConfig
from .formatter import BaseFormatter, JsonFormatter, PlainTextFormatter
from .hooks import register_fastapi_hooks, register_system_hooks
from .triggers import TriggerManager

# Define the public API of this module
__all__ = [
    "ErrorHandler",
    "initialize_error_handler",
    "get_error_handler",
    "ErrorHandlerConfig",
    "BaseFormatter",
    "JsonFormatter",
    "PlainTextFormatter",
    "register_fastapi_hooks",
    "register_system_hooks",
    "TriggerManager",
]


# Global instance of the error handler
_error_handler_instance: Optional["ErrorHandler"] = None

log = logging.getLogger(__name__)


class ErrorHandler:
    """
    Centralized class for handling all unhandled exceptions across the platform.
    """

    def __init__(self, config: ErrorHandlerConfig, logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.trigger_manager = TriggerManager(config.triggers)
        log.info("Generic Error Handler initialized.")

    def handle_exception(
        self, exc: Exception, context: Optional[Dict[str, Any]] = None
    ) -> None:
        """Handles a synchronous exception."""
        self.logger.error(
            "An unhandled synchronous exception occurred",
            exc_info=exc,
            extra={"context": context},
        )
        self.trigger_manager.process_triggers(exc)

    async def handle_exception_async(
        self, exc: Exception, context: Optional[Dict[str, Any]] = None
    ) -> None:
        """Handles an asynchronous exception."""
        self.logger.error(
            "An unhandled asynchronous exception occurred",
            exc_info=exc,
            extra={"context": context},
        )
        self.trigger_manager.process_triggers(exc)


def initialize_error_handler(
    config: ErrorHandlerConfig, logger: logging.Logger
) -> "ErrorHandler":
    """Initializes the singleton error handler instance."""
    global _error_handler_instance
    if _error_handler_instance is not None:
        raise RuntimeError("ErrorHandler has already been initialized.")
    _error_handler_instance = ErrorHandler(config, logger)
    return _error_handler_instance


def get_error_handler() -> "ErrorHandler":
    """
    Returns the singleton instance of the ErrorHandler.
    Raises an exception if it has not been initialized.
    """
    if _error_handler_instance is None:
        raise RuntimeError(
            "ErrorHandler has not been initialized. "
            "Call initialize_error_handler() first."
        )
    return _error_handler_instance
