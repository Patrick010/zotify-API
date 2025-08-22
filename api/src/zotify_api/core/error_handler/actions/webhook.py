import logging
from typing import Any, Dict

log = logging.getLogger(__name__)


def run(exc: Exception, details: Dict[str, Any]):
    """Action to send a notification to a webhook."""
    url = details.get("url")
    payload = details.get("payload")
    if not url or not payload:
        log.error("Webhook action is missing 'url' or 'payload' in details.")
        return

    log.info(f"Sending webhook to {url}...")
    # In a real implementation, we would use httpx or requests here.
    # For now, we just log the intent.
    # import httpx
    # try:
    #     httpx.post(url, json=payload)
    # except Exception:
    #     log.exception(f"Failed to send webhook to {url}")
