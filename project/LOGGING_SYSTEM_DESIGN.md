# Logging System Design

**Status:** Proposed
**Date:** 2025-08-14

## 1. Purpose
This document outlines the architecture for a new, extendable logging system for the Zotify API. The goal is to create a robust, centralized service that can handle multiple logging scenarios (e.g., system debug, audit, job progress) in a pluggable and maintainable way.

## 2. Core Architecture: Pluggable Handlers

The system will be built around a central `LoggingService`. This service will not perform any logging itself; instead, it will act as a dispatcher, forwarding log messages to one or more registered "handlers."

- **`LoggingService`:** A singleton service responsible for receiving all log messages from the application. It will maintain a registry of active handlers.
- **`BaseLogHandler`:** An abstract base class defining the interface for all handlers (e.g., `handle_message(log_record)`).
- **Concrete Handlers:** Specific implementations of `BaseLogHandler` for different logging scenarios.

This design allows new logging capabilities (e.g., sending logs to a new destination, using a new format) to be added simply by creating a new handler class and registering it with the service, without modifying the core application logic.

## 3. Proposed Handlers

### 3.1. `FileStreamHandler` (System & Debug Logs)
- **Purpose:** Provides basic, real-time streaming of application logs for developer debugging.
- **Implementation:** Tails the main application log file (e.g., `zotify_api.log`) and makes new lines available via a streaming API endpoint.
- **API Endpoint:** `GET /api/logs/system/stream` (returns a `StreamingResponse`).

### 3.2. `JsonAuditHandler` (Audit Logging)
- **Purpose:** Captures security-sensitive and business-critical events in a structured format.
- **Implementation:**
    - Listens for specific, predefined audit events (e.g., `user.login`, `config.update`).
    - Formats these events as JSON objects with a consistent schema (e.g., `{"timestamp": "...", "event_type": "...", "user_id": "...", "details": {...}}`).
    - Writes the structured logs to a separate, dedicated audit log file (e.g., `audit.log.json`).
- **API Endpoint:** `GET /api/logs/audit` (a queryable endpoint that can filter by user, event type, etc.).

### 3.3. `DatabaseJobLogHandler` (Job & Task Logging)
- **Purpose:** Records the detailed progress of long-running, asynchronous tasks like downloads and syncs.
- **Implementation:**
    - Associates log entries with a specific `job_id`.
    - Writes log messages (e.g., "Track 5/100 downloaded") to a new `job_logs` table in the database.
- **API Endpoint:** `GET /api/logs/jobs/{job_id}` (retrieves all log entries for a specific job).

## 4. Configuration

The logging system will be configurable via the application's main configuration. The configuration will allow enabling/disabling specific handlers and setting handler-specific parameters (e.g., log file paths).
