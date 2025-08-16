import logging
import yaml
import importlib
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from pathlib import Path

class BaseLogHandler(ABC):
    """Abstract base class for all log handlers."""

    @abstractmethod
    def can_handle(self, level: str) -> bool:
        """Whether this handler can process a log of the given level."""
        pass

    @abstractmethod
    def handle(self, level: str, message: str, extra: Dict[str, Any] = None):
        """Process the log message."""
        pass


def _import_from_string(path: str):
    """Dynamically import a class from a string path."""
    module_name, class_name = path.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)


class LoggingService:
    """A singleton service that dispatches log messages to registered handlers."""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LoggingService, cls).__new__(cls)
        return cls._instance

    def __init__(self, config_path: str = "logging_config.yml"):
        if hasattr(self, '_initialized'):
            return

        self.handlers: List[BaseLogHandler] = []
        self.config_path = Path(config_path)
        self._load_config()
        self._initialized = True
        logging.getLogger(__name__).info(f"LoggingService initialized with {len(self.handlers)} handlers.")

    def _load_config(self):
        """Load handlers from the YAML configuration file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Logging configuration not found at {self.config_path}")

        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)

        for handler_config in config.get("handlers", []):
            try:
                handler_class = _import_from_string(handler_config["class"])

                # Prepare constructor arguments
                handler_args = handler_config.copy()
                del handler_args["type"]
                del handler_args["class"]

                handler_instance = handler_class(**handler_args)
                self.register_handler(handler_instance)
            except (ImportError, AttributeError, KeyError) as e:
                logging.getLogger(__name__).error(f"Failed to load handler {handler_config.get('type')}: {e}")


    def register_handler(self, handler: BaseLogHandler):
        """Register a new log handler."""
        if handler not in self.handlers:
            self.handlers.append(handler)

    def log(self, level: str, message: str, extra: Dict[str, Any] = None):
        """
        Log a message by dispatching it to all handlers that can handle
        the given log level.
        """
        for handler in self.handlers:
            if handler.can_handle(level):
                handler.handle(level, message, extra)
