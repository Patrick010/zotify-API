# Zotify Flexible Logging Framework: Developer's Guide

**Version:** 1.1
**Credo:** "Documentation can never be too detailed."

## 1. Introduction & Philosophy

Welcome to the Zotify Flexible Logging Framework. This is not just an internal logging utility; it is a first-class, developer-facing tool designed to give you maximum control over how your code generates and routes log events.

The core philosophy is **decentralized control**. Instead of modifying a central configuration file every time you want to change the logging behavior of a specific function, this framework empowers you to define logging rules, destinations, and metadata *directly in your code*, at the moment you log the event.

This guide will walk you through the architecture, API, configuration, and advanced usage of the framework.

## 2. Core Concepts

### The `log_event` Function

The primary way you will interact with this framework is through a single, powerful function: `log_event()`.

```python
from zotify_api.core.logging_framework import log_event

def process_payment(user_id: str, amount: float):
    log_event(
        f"Processing payment for user {user_id}",
        level="INFO",
        destinations=["audit_log", "console"],
        tags=["payment", "audit"],
        extra={"user_id": user_id, "amount": amount}
    )
```

This single call allows you to specify the message, severity level, intended destinations, descriptive tags, and any structured data you want to include.

### Tag-Based Routing

The most powerful feature of the framework is **tag-based routing**. Developers can add a `tags` list to any `log_event` call. Administrators can then create `triggers` in the configuration file that watch for these tags and route copies of the log message to specific destinations.

This decouples the *what* from the *where*. A developer can simply tag a log as `"security"` or `"performance"` without needing to know where it should be stored. An administrator can then, without any code changes, decide that all `"security"` events should go to a special `security.log` file.

## 3. Configuration

The framework is controlled by two main mechanisms: the `logging_framework.yml` file and environment variables.

### 3.1. Environment Variables

-   `APP_ENV`: This is the most important variable. It determines the application's run mode.
    -   `development` (default): In this mode, logs can be more verbose, and sensitive data (like tokens) may be logged for debugging purposes.
    -   `production`: In this mode, **automatic sensitive data redaction is enabled**. Any log message containing tokens, codes, or other sensitive patterns will have that data automatically replaced with `[REDACTED]`.
-   `SNITCH_API_CALLBACK_URL`: As used by the `snitch` application, must be a full URL.

### 3.2. The `logging_framework.yml` File

This file defines the *available* destinations (sinks) and the routing rules (triggers). It is located at `api/logging_framework.yml`.

#### The `logging` Section: Sinks

This section defines all available output destinations.

-   `name`: A unique identifier for the sink.
-   `type`: Can be `console`, `file`, or `webhook`.
-   `level`: The minimum log level this sink will process.

**Sink Type: `file`**
```yaml
- name: "debug_log"
  type: "file"
  level: "DEBUG"
  path: "logs/debug.log" # Relative to the api/ directory
  max_bytes: 5242880 # 5 MB
  backup_count: 3
```
The `path` is relative to the `api/` directory. The `start.sh` script automatically creates the `api/logs` directory.

#### The `triggers` Section: Routing Rules

This section defines rules that route logs. The most powerful trigger is `tag`.

**Tag-Based Trigger Example:**
This trigger watches for any log event that has `"security"` in its `tags` list and routes a copy to the `security_log` sink.
```yaml
triggers:
  - tag: "security"
    action: "route_to_sink"
    details:
      destination: "security_log"
```

## 4. The `log_event` API Reference

**Signature:**
`log_event(message: str, level: str = "INFO", destinations: Optional[List[str]] = None, tags: Optional[List[str]] = None, **extra)`

-   `message` (str): The primary log message.
-   `level` (str): The log's severity.
-   `destinations` (Optional[List[str]]): A list of sink `name`s to send this specific log to. If `None`, the log is sent to *all* configured sinks.
-   `tags` (Optional[List[str]]): A list of string tags to attach to the log event, used for tag-based routing.
-   `**extra` (dict): Any additional key-value pairs will be included in the structured log record.

## 5. Advanced Usage: Creating Custom Workflows

The true power of the framework comes from combining the developer's ability to create custom tags with the administrator's ability to configure routing. The tags are not predefined or special; they are arbitrary strings that developers can invent to add meaning to an event.

Here is a complete workflow for creating a new, custom log stream for a "podcast processing" feature.

### Step 1: The Developer Tags a New Event

A developer working on a podcast feature can decide to tag all related logs with `"podcast_processing"`. This requires no special registration; they simply add the tag to the `log_event` call.

```python
# In a hypothetical podcast_service.py
from zotify_api.core.logging_framework import log_event

def process_podcast_episode(episode_id: str):
    log_event(
        f"Starting processing for podcast episode {episode_id}",
        level="INFO",
        tags=["podcast_processing"], # A new, custom tag
        extra={"episode_id": episode_id}
    )
    # ...
```

### Step 2: The Administrator Creates a New Log Stream

An administrator, seeing that developers are now using the `"podcast_processing"` tag, can decide to route these specific logs to their own file. They can do this entirely by editing the `logging_framework.yml` file, without requiring any code changes from the developer.

1.  **Define a new sink:**
    ```yaml
    # In logging_framework.yml, under `sinks:`
    - name: "podcast_log_file"
      type: "file"
      level: "INFO"
      path: "logs/podcasts.log"
    ```

2.  **Define a new trigger for the custom tag:**
    ```yaml
    # In logging_framework.yml, under `triggers:`
    - tag: "podcast_processing"
      action: "route_to_sink"
      details:
        destination: "podcast_log_file"
    ```

### Step 3: Reload the Configuration

Finally, the administrator can apply these changes to a running server by calling `POST /api/system/logging/reload`.

From this point on, every time a developer logs an event with the `"podcast_processing"` tag, it will be automatically routed to the `logs/podcasts.log` file, in addition to any other destinations it was sent to. This allows for the creation of highly specific, custom log streams for any feature or subsystem.

## 6. Runtime Configuration Reloading

You can update the `logging_framework.yml` file and apply the changes without restarting the application by sending an authenticated `POST` request to `POST /api/system/logging/reload`.

## 6. Complete Example

```yaml
# /api/logging_framework.yml
logging:
  default_level: "INFO"
  sinks:
    - name: "default_console"
      type: "console"
      level: "INFO"
    - name: "debug_log"
      type: "file"
      level: "DEBUG"
      path: "logs/debug.log"
    - name: "security_log"
      type: "file"
      level: "INFO"
      path: "logs/security.log"
    - name: "slack_alerter"
      type: "webhook"
      level: "CRITICAL"
      url: "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"
triggers:
  - tag: "security"
    action: "route_to_sink"
    details:
      destination: "security_log"
  - event: "database_timeout"
    action: "alert"
    details:
      message: "Database connection timed out. Check DB health."
      level: "CRITICAL"
      destinations: ["slack_alerter"]
```
