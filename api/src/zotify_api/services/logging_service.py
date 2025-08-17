import logging
import yaml
import importlib
from typing import List, Dict, Any
from zotify_api.core.logging_handlers.base import BaseLogHandler

log = logging.getLogger(__name__)

class LoggingService:
    """
    Centralized logging service that dispatches log messages to registered handlers.
    Handlers are dynamically loaded from a configuration file.
    """

    def __init__(self, config_path: str):
        self.handlers: List[BaseLogHandler] = self._load_handlers_from_config(config_path)
        log.info(f"LoggingService initialized with {len(self.handlers)} handlers.")

    def _load_handlers_from_config(self, config_path: str) -> List[BaseLogHandler]:
        """Loads and instantiates handlers from a YAML configuration file."""
        handlers = []
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
        except Exception:
            log.exception(f"Failed to load logging config file: {config_path}")
            return []

        handler_configs = config.get("handlers", [])
        for handler_conf in handler_configs:
            try:
                handler_type = handler_conf.pop("type")
                module_name = f"zotify_api.core.logging_handlers.{handler_type}"
                class_name = "".join(word.capitalize() for word in handler_type.split('_'))

                module = importlib.import_module(module_name)
                handler_class = getattr(module, class_name)

                # Pass the rest of the config as kwargs to the handler's constructor
                instance = handler_class(**handler_conf)
                handlers.append(instance)
                log.debug(f"Successfully loaded and instantiated handler: {class_name}")
            except Exception:
                log.exception(f"Failed to load handler with config: {handler_conf}")

        return handlers

    def log(self, level: str, message: str, **kwargs):
        """
        Logs a message by dispatching it to all relevant handlers.
        """
        log_record = {
            "level": level.upper(),
            "message": message,
            **kwargs
        }
        for handler in self.handlers:
            if handler.can_handle(level):
                try:
                    handler.emit(log_record)
                except Exception:
                    log.exception(f"Failed to execute log handler: {handler.__class__.__name__}")

# Singleton instance logic will be added later in main.py or deps.py
def get_logging_service():
    # This is a placeholder for a real implementation
    return LoggingService(config_path="logging_config.yml")
