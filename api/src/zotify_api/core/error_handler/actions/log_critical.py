import logging
from typing import Dict, Any

log = logging.getLogger(__name__)

def run(exc: Exception, details: Dict[str, Any]):
    """Action to log a message with CRITICAL level."""
    message = details.get("message", "A critical, triggered event occurred.")
    log.critical(f"[TRIGGERED ACTION] {message}", exc_info=exc)
