import asyncio
import logging
from logging.handlers import RotatingFileHandler
from typing import Dict, Any, Optional, List

import httpx

from .schemas import LoggingFrameworkConfig, AnySinkConfig, ConsoleSinkConfig, FileSinkConfig, WebhookSinkConfig

# Global instance of the service
_logging_service_instance = None


class BaseSink:
    """ Base class for all log sinks. """
    def __init__(self, config: AnySinkConfig):
        self.config = config
        self.level = logging.getLevelName(config.level)

    async def emit(self, log_record: Dict[str, Any]):
        """ Abstract method to emit a log record. """
        raise NotImplementedError

    def should_log(self, level: str) -> bool:
        """ Determines if a log should be processed based on its level. """
        return logging.getLevelName(level) >= self.level


class ConsoleSink(BaseSink):
    """ A sink that logs to the console. """
    async def emit(self, log_record: Dict[str, Any]):
        # In a real implementation, this would use a more robust formatter.
        print(f"CONSOLE: {log_record}")


class FileSink(BaseSink):
    """ A sink that logs to a rotating file. """
    def __init__(self, config: FileSinkConfig):
        super().__init__(config)
        self.handler = RotatingFileHandler(
            config.path,
            maxBytes=config.max_bytes,
            backupCount=config.backup_count
        )
        # A unique logger name to prevent conflicts
        self.logger = logging.getLogger(f"file_sink.{config.path}")
        self.logger.addHandler(self.handler)
        self.logger.setLevel(self.level)
        self.logger.propagate = False

    async def emit(self, log_record: Dict[str, Any]):
        # The logging call itself is synchronous, but we run it in a way
        # that doesn't block the main event loop if it were I/O heavy.
        # For standard file logging, this is fast enough.
        self.logger.info(str(log_record))


class WebhookSink(BaseSink):
    """ A sink that sends logs to a webhook URL. """
    def __init__(self, config: WebhookSinkConfig):
        super().__init__(config)
        self.client = httpx.AsyncClient()

    async def emit(self, log_record: Dict[str, Any]):
        try:
            await self.client.post(str(self.config.url), json=log_record)
        except httpx.RequestError as e:
            # In a real implementation, this failure should be logged
            # to a fallback sink (like the console).
            print(f"Webhook request failed: {e}")


class LoggingService:
    """ The main service for managing and dispatching logs. """
    def __init__(self):
        self.sinks: Dict[str, BaseSink] = {}
        self.config: Optional[LoggingFrameworkConfig] = None

    def load_config(self, config: LoggingFrameworkConfig):
        self.config = config
        self.sinks = {}  # Clear existing sinks
        for sink_config in config.logging.sinks:
            # Use the user-defined name as the key
            if sink_config.name in self.sinks:
                # Handle duplicate sink names gracefully
                print(f"Warning: Duplicate sink name '{sink_config.name}' found. Skipping.")
                continue

            if sink_config.type == "console":
                self.sinks[sink_config.name] = ConsoleSink(sink_config)
            elif sink_config.type == "file":
                self.sinks[sink_config.name] = FileSink(sink_config)
            elif sink_config.type == "webhook":
                self.sinks[sink_config.name] = WebhookSink(sink_config)

    def _handle_triggers(self, event: str, original_message: str) -> bool:
        """
        Checks for and processes any matching triggers for a given event.
        Returns True if a trigger was handled, False otherwise.
        """
        if not self.config or not self.config.triggers:
            return False

        triggered = False
        for trigger in self.config.triggers:
            if trigger.event == event:
                triggered = True
                details = trigger.details
                new_message = details.get("message", f"Triggered by event: {event}")
                new_level = details.get("level", "INFO")
                new_destinations = details.get("destinations")
                new_extra = details.get("extra", {})
                new_extra["is_triggered_event"] = True

                self.log(
                    message=new_message,
                    level=new_level,
                    destinations=new_destinations,
                    **new_extra
                )
        return triggered

    def log(self, message: str, level: str = "INFO", destinations: Optional[List[str]] = None, **extra):
        """
        Primary method for logging an event.
        Dispatches the log to the appropriate sinks and handles triggers.
        """
        # If a trigger is handled, we suppress the original log event.
        if not extra.get("is_triggered_event"):
            event_name = extra.get("event")
            if event_name:
                if self._handle_triggers(event_name, message):
                    return

        log_record = {"level": level, "message": message, **extra}

        sinks_to_log = []
        if destinations is None:
            # If no specific destinations, log to all sinks.
            sinks_to_log = self.sinks.values()
        else:
            # Log only to the specified, existing sinks.
            for dest_name in destinations:
                if dest_name in self.sinks:
                    sinks_to_log.append(self.sinks[dest_name])

        for sink in sinks_to_log:
            if sink.should_log(level):
                asyncio.create_task(sink.emit(log_record))


def get_logging_service() -> LoggingService:
    """
    Returns the singleton instance of the LoggingService.
    Initializes it if it doesn't exist.
    """
    global _logging_service_instance
    if _logging_service_instance is None:
        _logging_service_instance = LoggingService()
    return _logging_service_instance
