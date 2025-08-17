# Zotify Flexible Logging Framework: Developer's Guide

**Version:** 1.0
**Credo:** "Documentation can never be too detailed."

## 1. Introduction & Philosophy

Welcome to the Zotify Flexible Logging Framework. This is not just an internal logging utility; it is a first-class, developer-facing tool designed to give you maximum control over how your code generates and routes log events.

The core philosophy is **decentralized control**. Instead of modifying a central configuration file every time you want to change the logging behavior of a specific function, this framework empowers you to define logging rules, destinations, and metadata *directly in your code*, at the moment you log the event.

This guide will walk you through the architecture, API, configuration, and advanced usage of the framework.

## 2. Core Concepts

### Logging vs. Error Handling

It is crucial to understand the distinction between this framework and the global `ErrorHandler`:

-   **`ErrorHandler`**: This is a specialized system that **reacts to uncaught exceptions**. Its job is to be a safety net for the entire application. When an unexpected error occurs, it catches it and can trigger high-level actions (like sending an alert).
-   **`LoggingFramework`**: This is a general-purpose tool for **proactively creating log entries**. You use it to record informational messages, debug traces, audit trails, business events, and expected errors.

The two systems are integrated. By default, the `ErrorHandler` uses this `LoggingFramework` to log the exceptions it catches. This means a critical exception can be routed to multiple destinations (e-mail, Slack, a log file, etc.) using the power of this framework.

### The `log_event` Function

The primary way you will interact with this framework is through a single, powerful function: `log_event()`.

```python
from zotify_api.core.logging_framework import log_event

def process_payment(user_id: str, amount: float):
    log_event(
        f"Processing payment for user {user_id}",
        level="INFO",
        destinations=["audit_log", "console"],
        extra={"user_id": user_id, "amount": amount}
    )
    # ... payment processing logic ...
```

This single call allows you to specify the message, severity level, intended destinations, and any structured data you want to include.

## 3. Configuration (`logging_framework.yml`)

While the framework is designed for inline control, a central configuration file is used to define the *available* destinations (sinks) and global trigger rules.

**File Location:** The configuration file must be located at `api/logging_framework.yml`.

### Top-Level Structure

The YAML file has two main sections: `logging` and `triggers`.

```yaml
logging:
  # ... defines sinks and default behavior ...
triggers:
  # ... defines rules that react to log events ...
```

### The `logging` Section

This section defines the default logging level and all available output destinations, called "sinks".

```yaml
logging:
  default_level: INFO
  sinks:
    - # ... sink 1 config ...
    - # ... sink 2 config ...
```

-   `default_level`: The global log level. Messages below this level are ignored unless a sink specifies a more verbose level. Valid levels are `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.
-   `sinks`: A list of all configured sink objects.

### Sink Configuration

Every sink configuration shares three common properties:

-   `name` (string, required): A unique identifier for the sink. You will use this name in `log_event` to target specific destinations. Must contain only letters, numbers, and underscores.
-   `type` (string, required): The type of the sink. Determines which other fields are required. Valid types for the MVP are `console`, `file`, and `webhook`.
-   `level` (string, optional): The minimum log level this sink will process. If omitted, it uses the `default_level`.

#### Sink Type: `console`

Logs messages to the standard console output.

-   **Fields:**
    -   `name`, `type`, `level`
-   **Example:**
    ```yaml
    - name: "my_console"
      type: "console"
      level: "INFO"
    ```

#### Sink Type: `file`

Logs messages to a file, with built-in support for log rotation.

-   **Fields:**
    -   `name`, `type`, `level`
    -   `path` (string, required): The absolute or relative path to the log file.
    -   `max_bytes` (integer, optional): The maximum size of the log file in bytes before it is rotated. Defaults to `10485760` (10 MB).
    -   `backup_count` (integer, optional): The number of old log files to keep. Defaults to `5`.
-   **Example:**
    ```yaml
    - name: "debug_log"
      type: "file"
      level: "DEBUG"
      path: "/app/api/logs/debug.log"
      max_bytes: 5242880 # 5 MB
      backup_count: 3
    ```

#### Sink Type: `webhook`

Sends log messages as a JSON payload to a specified HTTP/S URL via a POST request.

-   **Fields:**
    -   `name`, `type`, `level`
    -   `url` (string, required): The full URL to send the webhook to.
-   **Example:**
    ```yaml
    - name: "critical_alert_webhook"
      type: "webhook"
      level: "CRITICAL"
      url: "https://hooks.example.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"
    ```

### The `triggers` Section

This section defines rules that can be triggered by log events. (Note: The action mechanism is basic in the MVP).

-   **Example:**
    ```yaml
    triggers:
      - event: "user_login_failed"
        action: "log_security_event"
        details:
          level: "WARNING"
          destinations: ["debug_log"]
    ```

## 4. The `log_event` API Reference

This is the primary function for all logging operations.

**Signature:**
`log_event(message: str, level: str = "INFO", destinations: Optional[List[str]] = None, **extra)`

-   `message` (str): The primary log message.
-   `level` (str): The log's severity. Defaults to `INFO`.
-   `destinations` (Optional[List[str]]): A list of sink `name`s to send this specific log to. If `None`, the log is sent to *all* configured sinks that meet the level threshold.
-   `**extra` (dict): Any additional key-value pairs will be included in the structured log record. This is useful for passing context like user IDs, request IDs, etc.

## 5. Runtime Configuration Reloading

You can update the `logging_framework.yml` file and apply the changes without restarting the application. This is useful for changing log levels on a live system or adding a new temporary sink for debugging.

To reload the configuration, send an authenticated `POST` request to the following endpoint:

`POST /api/system/logging/reload`

A successful request will return a `202 Accepted` status code and a JSON body confirming the reload. If the configuration file is missing or contains invalid syntax or schema errors, the endpoint will return an appropriate `4xx` error code with details.

## 6. Complete Example

Here is a complete `logging_framework.yml` example demonstrating multiple sinks.

```yaml
# /api/logging_framework.yml

logging:
  default_level: "INFO"  # Don't log DEBUG messages by default
  sinks:
    # A console sink for general information during development
    - name: "default_console"
      type: "console"
      level: "INFO"

    # A detailed log file for debugging and forensics
    - name: "main_log_file"
      type: "file"
      level: "DEBUG" # Capture everything in this file
      path: "/app/api/logs/main.log"
      max_bytes: 20971520 # 20MB
      backup_count: 5

    # A webhook to a Slack channel for critical errors
    - name: "slack_alerter"
      type: "webhook"
      level: "CRITICAL"
      url: "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"

triggers:
  - event: "database_timeout"
    action: "alert"
    details:
      message: "Database connection timed out. Check DB health."
      level: "CRITICAL"
      destinations: ["slack_alerter"]
```
