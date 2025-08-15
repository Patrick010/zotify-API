# Developer Guide: Generic Error Handling Module

**Status:** Proposed
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

### 4.1. Adding Custom Error Mappings

To map a specific exception type to a custom error code and message, you can add an entry to the (planned) error mapping configuration.

*(Note: The exact mechanism for this is TBD, but it will likely involve a dictionary in a configuration file.)*

### 4.2. Adding Custom Triggers and Actions

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

**To add a new action type:**
1.  Open `api/src/zotify_api/core/error_handler/triggers.py`.
2.  Create a new function that performs the desired action (e.g., `send_sms_alert(config)`).
3.  Register this new action type in the `TriggerManager`.

## 5. Best Practices

-   **Don't Swallow Exceptions:** Avoid generic `except Exception:` blocks that hide errors. Let unhandled exceptions propagate up to the global handler.
-   **Use Specific Exceptions:** When raising your own errors, use specific, descriptive exception classes rather than generic `Exception`. This makes it easier to configure triggers.
-   **Provide Context:** When manually handling an exception, pass any relevant contextual information (e.g., user ID, job ID, relevant data) to the `handle_exception` method. This will be invaluable for debugging.
