import traceback
from datetime import datetime, timezone
from typing import Any, Dict


class BaseFormatter:
    """Base class for error formatters."""
    def format(self, exc: Exception, context: Dict[str, Any]) -> Any:
        raise NotImplementedError

class JsonFormatter(BaseFormatter):
    """Formats errors into a standardized JSON structure for API responses."""

    def __init__(self, verbosity: str = "production"):
        self.verbosity = verbosity

    def format(self, exc: Exception, context: Dict[str, Any]) -> Dict[str, Any]:
        error_data = {
            "error": {
                "code": context.get("error_code", "E-UNKNOWN"),
                "message": context.get("message", "An unexpected error occurred."),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "request_id": context.get("request_id"),
            }
        }

        if self.verbosity == "debug":
            error_data["error"]["details"] = {
                "exception_type": type(exc).__name__,
                "exception_message": str(exc),
                "traceback": traceback.format_exc(),
            }

        return error_data

class PlainTextFormatter(BaseFormatter):
    """Formats errors into a plain text string for logs or CLI output."""

    def __init__(self, verbosity: str = "production"):
        self.verbosity = verbosity

    def format(self, exc: Exception, context: Dict[str, Any]) -> str:
        parts = [
            f"[{datetime.now(timezone.utc).isoformat()}]",
            f"[{context.get('error_code', 'E-UNKNOWN')}]",
            f"[{context.get('request_id', 'NO-REQ-ID')}]",
            f"- {context.get('message', 'An unexpected error occurred.')}",
        ]

        if self.verbosity == "debug":
            parts.append(f"-- Exception: {type(exc).__name__}: {str(exc)}")
            parts.append(f"-- Traceback: {traceback.format_exc()}")

        return " ".join(parts)
