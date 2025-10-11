# ID: API-036
import logging
import re


class SensitiveDataFilter(logging.Filter):
    """
    A logging filter that redacts sensitive data from log records.
    """

    _PATTERNS = {
        "access_token": re.compile(r"\"access_token\":\s*\"[^\"]+\""),
        "refresh_token": re.compile(r"\"refresh_token\":\s*\"[^\"]+\""),
        "code": re.compile(r"\"code\":\s*\"[^\"]+\""),
        "state": re.compile(r"\"state\":\s*\"[^\"]+\""),
    }
    _REDACTION_STRING = "[REDACTED]"

    def filter(self, record: logging.LogRecord) -> bool:
        # We can filter based on both the raw message and the args
        record.msg = self._redact(record.msg)
        if record.args:
            redacted_args = [
                self._redact(arg) if isinstance(arg, str) else arg
                for arg in record.args
            ]
            record.args = tuple(redacted_args)
        return True

    def _redact(self, message: str) -> str:
        # Redact patterns for key-value pairs
        for key, pattern in self._PATTERNS.items():
            # Replacement function to keep the key but redact the value
            repl = f'"{key}": "{self._REDACTION_STRING}"'
            message = pattern.sub(repl, message)
        return message
