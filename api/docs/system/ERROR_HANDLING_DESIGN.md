<!-- ID: API-194 -->
# Generic Error Handling Module - Design Specification

**Status:** Proposed
**Author:** Jules
**Related Documents:** `HLD.md`, `LLD.md`, `ERROR_HANDLING_GUIDE.md`

## 1. Overview

This document provides the detailed technical design for the Generic Error Handling Module. This module serves as the central, platform-wide mechanism for intercepting, processing, logging, and responding to all unhandled exceptions.

## 2. Core Components & Class Structure

The module will be located at `api/src/zotify_api/core/error_handler/` and will consist of the following key components:

### 2.1. `ErrorHandler` (in `main.py`)

This is the central class of the module, designed as a singleton.

```python
class ErrorHandler:
    def __init__(self, config: ErrorHandlerConfig, logger: Logger):
        # ...

    def handle_exception(self, exc: Exception, context: dict = None):
        # Main processing logic
        # 1. Determine error category (e.g., API, Internal, Provider)
        # 2. Generate standardized error response using a formatter
        # 3. Log the error with full traceback
        # 4. Check for and execute any configured triggers

    async def handle_exception_async(self, exc: Exception, context: dict = None):
        # Async version for use in async contexts
```

### 2.2. `IntegrationHooks` (in `hooks.py`)

This file will contain the functions to wire the `ErrorHandler` into the application.

```python
def register_fastapi_hooks(app: FastAPI, handler: ErrorHandler):
    # Adds a Starlette exception middleware to the FastAPI app.
    # This middleware will catch all exceptions from the API layer
    # and pass them to handler.handle_exception_async().

def register_system_hooks(handler: ErrorHandler):
    # Sets sys.excepthook to a function that calls handler.handle_exception().
    # This catches all unhandled exceptions in synchronous, non-FastAPI code.

    # Sets the asyncio event loop's exception handler to a function
    # that calls handler.handle_exception_async().
    # This catches unhandled exceptions in background asyncio tasks.
```

### 2.3. `Configuration` (in `config.py`)

This file defines the Pydantic models for the module's configuration, which will be loaded from a YAML file.

```python
class ActionConfig(BaseModel):
    type: Literal["log_critical", "webhook"]
    # ... action-specific fields (e.g., webhook_url)

class TriggerConfig(BaseModel):
    exception_type: str  # e.g., "requests.exceptions.ConnectionError"
    actions: list[ActionConfig]

class ErrorHandlerConfig(BaseModel):
    verbosity: Literal["debug", "production"] = "production"
    triggers: list[TriggerConfig] = []
```

## 3. Standardized Error Schema

All errors processed by the module will be formatted into a standard schema before being returned or logged.

### 3.1. API Error Schema (JSON)

For API responses, the JSON body will follow this structure:

```json
{
  "error": {
    "code": "E1001",
    "message": "An internal server error occurred.",
    "timestamp": "2025-08-14T14:30:00Z",
    "request_id": "uuid-...",
    "details": {
      // Optional, only in debug mode
      "exception_type": "ValueError",
      "exception_message": "...",
      "traceback": "..."
    }
  }
}
```

### 3.2. CLI/Log Error Format (Plain Text)

For non-API contexts, errors will be logged in a structured plain text format:
`[TIMESTAMP] [ERROR_CODE] [MESSAGE] [REQUEST_ID] -- Exception: [TYPE]: [MESSAGE] -- Traceback: [...]`

## 4. Trigger/Action System

The trigger/action system provides a mechanism for automating responses to specific errors.

-   **Triggers** are defined by the type of exception (e.g., `requests.exceptions.ConnectionError`).
-   **Actions** are the operations to perform when a trigger matches (e.g., `log_critical`, `webhook`).

### 4.1. Example Configuration (`error_handler_config.yaml`)

```yaml
verbosity: production
triggers:
  - exception_type: requests.exceptions.ConnectionError
    actions:
      - type: log_critical
        message: "External provider connection failed."
      - type: webhook
        url: "https://hooks.slack.com/services/..."
        payload:
          text: "CRITICAL: Provider connection error detected in Zotify API."
```

## 5. Integration Strategy

1.  The `ErrorHandler` singleton will be instantiated in `api/src/zotify_api/main.py`.
2.  The configuration will be loaded from `error_handler_config.yaml`.
3.  `register_fastapi_hooks()` will be called to attach the middleware to the FastAPI app.
4.  `register_system_hooks()` will be called to set the global `sys.excepthook` and asyncio loop handler.

This ensures that any unhandled exception, regardless of its origin, will be funneled through the central `ErrorHandler` for consistent processing.
