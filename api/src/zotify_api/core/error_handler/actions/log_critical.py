from typing import Dict, Any
from zotify_api.core.logging_framework import log_event

def run(exc: Exception, details: Dict[str, Any]):
    """
    Action to log a message with CRITICAL level using the flexible
    logging framework.
    """
    message = details.pop("message", "A critical, triggered event occurred.")

    # Prepare extra context for structured logging
    extra_context = {
        "exception_type": exc.__class__.__name__,
        "exception_module": exc.__class__.__module__,
        "triggered_by": "ErrorHandler",
        **details  # Include any other details from the trigger config
    }

    log_event(
        message=f"[TRIGGERED ACTION] {message}",
        level="CRITICAL",
        **extra_context
    )
