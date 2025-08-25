# Developer Guide: Generic Error Handling Module

**Status:** Implemented
**Author:** Jules

## 1. Introduction

This guide explains how to work with the Generic Error Handling Module. This module is the centralized system for processing all unhandled exceptions. All developers working on the Zotify API platform should be familiar with its operation.

## 2. Core Concepts

-   **Automatic Interception:** You do not need to wrap your code in `try...except` blocks for general error handling. The module automatically catches all unhandled exceptions from API endpoints, background tasks, and other services.
-   **Standardized Output:** All errors are automatically formatted into a standard JSON response for APIs or a plain text format for other contexts. Your code should not return custom error formats.

## 3. Manually Triggering the Error Handler

In some cases, you may want to handle an exception but still report it to the central handler for logging and trigger processing. You can do this by injecting the `ErrorHandler` singleton and calling it directly.

```python
from zotify_api.core.error_handler import get_error_handler

async def some_function():
    handler = get_error_handler()
    try:
        # Some fallible operation
        result = await some_api_call()
    except SomeExpectedException as e:
        # Perform some local cleanup
        await handler.handle_exception_async(e, context={"user_id": "123"})
        # Return a custom, safe response to the user
        return {"status": "failed_safely"}
```

## 4. Extending the Module

The module is designed to be extensible without modifying its core code.

### 4.1. Adding Custom Triggers

The trigger/action system allows you to automate responses to specific errors. This is configured entirely through the `error_handler_config.yaml` file.

**To add a new trigger:**
1.  Identify the full path of the exception type you want to catch (e.g., `sqlalchemy.exc.IntegrityError`).
2.  Add a new entry to the `triggers` list in `error_handler_config.yaml`.
3.  Define one or more actions to be executed.

**Example:**
```yaml
triggers:
  - exception_type: sqlalchemy.exc.IntegrityError
    actions:
      - type: log_critical
        message: "Database integrity violation detected!"
```

### 4.2. Adding a New Action Type

The system is now fully extensible. Adding a new action requires no modification of the core `TriggerManager`.

1.  Create a new Python file in the `src/zotify_api/core/error_handler/actions/` directory. The name of the file will be the `type` of your action (e.g., `send_sms.py` would create an action of type `send_sms`).
2.  In that file, create a class that inherits from `zotify_api.core.error_handler.actions.base.BaseAction`. The class name should be the PascalCase version of the filename (e.g., `SendSms`).
3.  Implement the `run(self, context: dict)` method. The `context` dictionary contains the original exception and the action configuration from the YAML file.

**Example `.../actions/send_sms.py`:**
```python
import logging
from .base import BaseAction

log = logging.getLogger(__name__)

class SendSms(BaseAction):
    def run(self, context: dict):
        """
        A custom action to send an SMS notification.
        """
        exc = context.get("exception")
        action_config = context.get("action_config") # Details from the YAML

        phone_number = action_config.get("phone_number")
        if not phone_number:
            log.error("SMS action is missing 'phone_number' in config.")
            return

        message = f"Critical error detected: {exc}"
        log.info(f"Sending SMS to {phone_number}: {message}")
        # In a real implementation, you would use a service like Twilio here.
```

The `TriggerManager` will automatically discover and load your new action at startup. You can then use the action `type` (e.g., `send_sms`) in your `error_handler_config.yaml`.

## 5. Best Practices

-   **Don't Swallow Exceptions:** Avoid generic `except Exception:` blocks that hide errors. Let unhandled exceptions propagate up to the global handler.
-   **Use Specific Exceptions:** When raising your own errors, use specific, descriptive exception classes rather than generic `Exception`. This makes it easier to configure triggers.
-   **Provide Context:** When manually handling an exception, pass any relevant contextual information (e.g., user ID, job ID, relevant data) to the `handle_exception` method. This will be invaluable for debugging.
