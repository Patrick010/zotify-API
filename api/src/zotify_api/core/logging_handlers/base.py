from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseLogHandler(ABC):
    """
    Abstract base class for all log handlers.
    """

    @abstractmethod
    def can_handle(self, level: str) -> bool:
        """
        Determines if the handler should process a log message with the given level.
        """
        raise NotImplementedError

    @abstractmethod
    def emit(self, log_record: Dict[str, Any]):
        """
        Processes the log record (e.g., writes it to a file, console, or database).
        """
        raise NotImplementedError

    def format(self, log_record: Dict[str, Any]) -> Any:
        """
        Formats the log record into the desired output format.
        This can be overridden by subclasses.
        """
        return log_record
