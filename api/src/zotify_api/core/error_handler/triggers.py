import logging
from typing import List, Dict, Any
from .config import TriggerConfig

log = logging.getLogger(__name__)

class TriggerManager:
    """
    Manages the execution of actions based on configured triggers.
    """

    def __init__(self, triggers: List[TriggerConfig]):
        self.triggers = triggers
        self.action_map = {
            "log_critical": self._action_log_critical,
            "webhook": self._action_webhook,
        }
        log.info(f"TriggerManager initialized with {len(triggers)} triggers.")

    def process_triggers(self, exc: Exception):
        """
        Checks if the given exception matches any configured triggers and
        executes the associated actions.
        """
        exc_type_str = f"{exc.__class__.__module__}.{exc.__class__.__name__}"

        for trigger in self.triggers:
            if trigger.exception_type == exc_type_str:
                log.info(f"Exception '{exc_type_str}' matched a trigger. Executing actions.")
                for action_config in trigger.actions:
                    action_func = self.action_map.get(action_config.type)
                    if action_func:
                        try:
                            action_func(exc, action_config.details)
                        except Exception:
                            log.exception(f"Failed to execute action of type '{action_config.type}'")
                    else:
                        log.warning(f"Unknown action type '{action_config.type}' configured.")

    def _action_log_critical(self, exc: Exception, details: Dict[str, Any]):
        """Action to log a message with CRITICAL level."""
        message = details.get("message", "A critical, triggered event occurred.")
        log.critical(f"[TRIGGERED ACTION] {message}", exc_info=exc)

    def _action_webhook(self, exc: Exception, details: Dict[str, Any]):
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
