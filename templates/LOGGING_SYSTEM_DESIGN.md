# Logging System Design

**Status:** Proposed
**Date:** <DATE>

## 1. Purpose
This document outlines the architecture for a new, extendable logging system for the <PROJECT_NAME>. The goal is to create a robust, centralized service that can handle multiple logging scenarios (e.g., system debug, audit, job progress) in a pluggable and maintainable way.

## 2. Core Architecture: Pluggable Handlers

The system will be built around a central `LoggingService`. This service will not perform any logging itself; instead, it will act as a dispatcher, forwarding log messages to one or more registered "handlers."

- **`LoggingService`:** A singleton service responsible for receiving all log messages from the application. It will maintain a registry of active handlers.
- **`BaseLogHandler`:** An abstract base class defining the interface for all handlers (e.g., `handle_message(log_record)`).
- **Concrete Handlers:** Specific implementations of `BaseLogHandler` for different logging scenarios.

This design allows new logging capabilities (e.g., sending logs to a new destination, using a new format) to be added simply by creating a new handler class and registering it with the service, without modifying the core application logic.

## 3. Initial Handlers

The system can be launched with initial handlers to cover the most common log types.

### 3.1. System/Debug Handler (`ConsoleHandler`)
- **Purpose:** For standard application logging during development and operation.
- **Log Levels Handled:** `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.
- **Format:** Simple, human-readable text format.
- **Example:** `[<DATE> <TIME>] [INFO] User '<USER_ID>' successfully authenticated.`
- **Output:** Standard output (console).

### 3.2. Structured JSON Audit Handler (`JsonAuditHandler`)
- **Purpose:** For compliance-ready, machine-readable audit trails of security-sensitive and business-critical events.
- **Log Levels Handled:** `AUDIT`.
- **Format:** Structured JSON, written to a dedicated, append-only log file (e.g., `logs/audit.json.log`).
- **Mandatory Fields:**
  - `timestamp`: ISO 8601 format string.
  - `event_id`: A unique identifier for the log entry (e.g., UUID).
  - `event_name`: The name of the audit event (e.g., `user.login.success`, `playlist.create`).
  - `user_id`: The user associated with the event.
  - `source_ip`: The source IP address of the request.
  - `details`: A JSON object containing event-specific data.

### 3.3. Database-backed Job Handler (`DatabaseJobHandler`)
- **Purpose:** To track the progress and outcomes of long-running, asynchronous jobs (e.g., syncs, downloads, report generation).
- **Log Levels Handled:** `JOB_STATUS`.
- **Output:** Writes structured data to a dedicated `job_logs` table in the application's primary database.
- **Database Schema (`job_logs` table):**
  - `job_id` (string, primary key)
  - `job_type` (string)
  - `status` (string: `QUEUED`, `RUNNING`, `COMPLETED`, `FAILED`)
  - `progress` (integer, 0-100)
  - `details` (text/json)
  - `created_at` (datetime)
  - `updated_at` (datetime)

## 4. Pluggable Handler Interface

To allow for extensibility, all handlers must adhere to a common interface, likely defined in a `BaseLogHandler` abstract class.

- **`can_handle(level)`:** A method that returns `True` if the handler is configured to process logs of the given level/type.
- **`emit(log_record)`:** The core method that performs the logging action (e.g., writing to the console, a file, or a database).
- **`format(log_record)`:** A method that formats the log record into the desired string or structure.

## 5. Integration Points for <PROJECT_NAME>
- **Instantiation:** The `LoggingService` will be instantiated once in the main application entrypoint file (e.g., `main.py`).
- **Dependency Injection:** The service instance will be made available to all route handlers and services using the web framework's dependency injection system.
- **Configuration:** The logging configuration will be loaded from a new file, e.g., `logging_config.yml`, which will be read at startup. This file will define which handlers are active and their specific settings.

## 6. Guidelines for Adding New Handlers
1. **Create a new handler class** in a file under `<path_to_logging_handlers_directory>`.
2. **Inherit from `BaseLogHandler`** and implement the `can_handle` and `emit` methods.
3. **Define a custom formatter** if required.
4. **Register the new handler** in the `logging_config.yml` file, specifying its type, log levels, and any other configuration.
5. The `LoggingService` will automatically discover and initialize the new handler on the next application startup.
