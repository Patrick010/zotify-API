import asyncio
import logging
from logging.handlers import RotatingFileHandler
from typing import Any, Dict, List, Optional

import httpx

from .schemas import AnySinkConfig, FileSinkConfig, LoggingFrameworkConfig, WebhookSinkConfig

# Global instance of the service
_logging_service_instance = None


class BaseSink:
    """Base class for all log sinks."""

    def __init__(self, config: AnySinkConfig):
        self.config = config
        self.level = logging.getLevelName(config.level)

    async def emit(self, log_record: Dict[str, Any]):
        """Abstract method to emit a log record."""
        raise NotImplementedError

    def should_log(self, level: str) -> bool:
        """Determines if a log should be processed based on its level."""
        return logging.getLevelName(level) >= self.level


class ConsoleSink(BaseSink):
    """A sink that logs to the console."""

    async def emit(self, log_record: Dict[str, Any]):
        # In a real implementation, this would use a more robust formatter.
        print(f"CONSOLE: {log_record}")


class FileSink(BaseSink):
    """A sink that logs to a rotating file."""

    def __init__(self, config: FileSinkConfig):
        super().__init__(config)
        self.handler = RotatingFileHandler(
            config.path, maxBytes=config.max_bytes, backupCount=config.backup_count
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
    """A sink that sends logs to a webhook URL."""

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
    """The main service for managing and dispatching logs."""

    def __init__(self):
        self.sinks: Dict[str, BaseSink] = {}
        self.config: Optional[LoggingFrameworkConfig] = None

    def load_config(self, config: LoggingFrameworkConfig):
        self.config = config
        self.sinks = {}  # Clear existing sinks
        for sink_config in config.logging.sinks:
            if sink_config.name in self.sinks:
                print(
                    f"Warning: Duplicate sink name '{sink_config.name}' found. "
                    "Skipping."
                )
                continue

            if sink_config.type == "console":
                self.sinks[sink_config.name] = ConsoleSink(sink_config)
            elif sink_config.type == "file":
                self.sinks[sink_config.name] = FileSink(sink_config)
            elif sink_config.type == "webhook":
                self.sinks[sink_config.name] = WebhookSink(sink_config)

    def _handle_event_trigger(self, event: str) -> bool:
        """
        Checks for and processes a matching event-based trigger.
        Event-based triggers are destructive; they stop the original event.
        Returns True if a trigger was handled, False otherwise.
        """
        if not self.config or not self.config.triggers:
            return False

        for trigger in self.config.triggers:
            if trigger.event == event:
                details = trigger.details
                self.log(
                    message=details.get("message", f"Triggered by event: {event}"),
                    level=details.get("level", "INFO"),
                    destinations=details.get("destinations"),
                    **details.get("extra", {}),
                )
                return True
        return False

    def _handle_tag_triggers(self, tags: List[str], log_record: Dict[str, Any]):
        """
        Checks for and processes any matching tag-based triggers.
        Tag-based triggers are non-destructive; they route a copy of the
        original event to a new destination.
        """
        if not self.config or not self.config.triggers:
            return

        for tag in tags:
            for trigger in self.config.triggers:
                if trigger.tag == tag:
                    # For now, we only support the "route_to_sink" action
                    if trigger.action == "route_to_sink":
                        dest_name = trigger.details.get("destination")
                        if dest_name and dest_name in self.sinks:
                            sink = self.sinks[dest_name]
                            if sink.should_log(log_record["level"]):
                                asyncio.create_task(sink.emit(log_record))

    def log(
        self,
        message: str,
        level: str = "INFO",
        destinations: Optional[List[str]] = None,
        **extra,
    ):
        """
        Primary method for logging an event.
        Dispatches the log to the appropriate sinks and handles triggers.
        """
        # Event triggers are handled first and are destructive
        # (they replace the original log)
        event_name = extra.get("event")
        if event_name:
            if self._handle_event_trigger(event_name):
                return

        log_record = {"level": level, "message": message, **extra}

        # Tag triggers are handled next and are non-destructive (they fork the log)
        tags = extra.get("tags")
        if tags and isinstance(tags, list):
            self._handle_tag_triggers(tags, log_record)

        # Finally, process the original log event
        sinks_to_log = []
        if destinations is None:
            sinks_to_log = self.sinks.values()
        else:
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
