# Developer Guide: Extendable Logging System

**Status:** Proposed
**Date:** 2025-08-14

## 1. Overview
This guide explains how to use and extend the Zotify API's logging system. The system is designed to be pluggable, allowing developers to easily add new logging behaviors (handlers) for different purposes without modifying the core application.

## 2. System Architecture
The logging system is built on two key components:
- **`LoggingService`**: A central dispatcher that receives all log messages.
- **`BaseLogHandler`**: An interface that defines how a handler should process a log message.

When a part of the application emits a log (e.g., `logging_service.audit(...)`), the service iterates through all registered handlers and passes the log record to each one. This allows a single event to be logged to multiple destinations in different formats (e.g., to a system log file, a JSON audit file, and a database table all at once).

## 3. How to Create a New Logging Handler

Creating a new handler is the standard way to add new logging functionality.

### Step 1: Create the Handler Class
Create a new class that inherits from `BaseLogHandler` and implements the required `handle_message` method.

**Example: `NewEmailAlertHandler`**
```python
# in api/src/zotify_api/logging/handlers/email_handler.py

from .base import BaseLogHandler
from ..email_service import send_email

class EmailAlertHandler(BaseLogHandler):
    def __init__(self, alert_level="ERROR", recipient=None):
        self.alert_level = alert_level
        self.recipient = recipient

    def handle_message(self, log_record: dict):
        if log_record.get("level") == self.alert_level and self.recipient:
            subject = f"Zotify Alert: {log_record.get('event_type')}"
            body = f"A new alert has been logged: {log_record}"
            send_email(to=self.recipient, subject=subject, body=body)

```

### Step 2: Register the Handler
In the main application startup logic (likely in `main.py` or a new `logging_setup.py`), instantiate your new handler and register it with the `LoggingService`.

```python
# in main.py or logging_setup.py

from zotify_api.services.logging_service import logging_service
from zotify_api.logging.handlers.email_handler import EmailAlertHandler

# ... during app startup ...

# Get config from settings
if settings.email_alerts_enabled:
    email_handler = EmailAlertHandler(
        alert_level=settings.email_alert_level,
        recipient=settings.email_alert_recipient
    )
    logging_service.register_handler(email_handler)
```

## 4. How to Emit Log Events

To ensure logs are processed by the new system, use the central `logging_service` instance. Different methods can be used for different log types to provide semantic meaning.

### Emitting a System/Debug Log
For general purpose logging.

```python
from zotify_api.services.logging_service import logging_service

logging_service.info("User service started successfully.")
```

### Emitting an Audit Event
For security-sensitive or business-critical events. This should be a structured dictionary.

```python
from zotify_api.services.logging_service import logging_service

event = {
    "event_type": "user.login.success",
    "user_id": "some_user_id",
    "ip_address": "127.0.0.1"
}
logging_service.audit(event)
```

### Emitting a Job Log
For logging progress of a long-running task.

```python
from zotify_api.services.logging_service import logging_service

job_id = "xyz-123"
logging_service.job_log(job_id, "Track 5/100 downloaded successfully.")
```

By following this pattern, all logging remains consistent, centralized, and extendable.
