# Project Backlog

**Status:** Live Document

## 1. Purpose

This document serves as the tactical backlog for the Zotify API project. It contains a list of clearly defined tasks that have been approved for implementation but are not yet assigned to a specific sprint or work cycle. This provides a work supply for future phases and ensures that good ideas are not lost.

Tasks in this backlog are distinct from the strategic, high-level goals outlined in `FUTURE_ENHANCEMENTS.md`.

## 2. Backlog Items

Items are to be flagged with a priority (`[HIGH]`, `[MEDIUM]`, `[LOW]`) and a status marker to aid in work planning.

---
### `TD-TASK-01` [CRITICAL]: Resolve MyPy Blocker
- **Status:** ❌ Not Started
- **Description:** The `mypy` type checker currently fails to run due to a duplicate module name conflict between `api/src/zotify_api/routes/config.py` and `api/src/zotify_api/models/config.py`. This task is to rename one of the files (e.g., to `config_routes.py`) to resolve the conflict and allow the type checker to run across the codebase. This is a blocker for all future type safety work.
- **Source:** `project/audit/CODE_OPTIMIZATIONPLAN_PHASE_4.md`

---

### `TD-TASK-02` [HIGH]: Remediate Critical Security Vulnerabilities
- **Status:** ❌ Not Started
- **Description:** Address the high-priority security issues identified by `bandit`. This includes removing the `debug=True` flag from the `gonk-testUI` server startup and refactoring the database query in `tracks_service.py` to use parameterized queries instead of string formatting to prevent SQL injection risks.
- **Source:** `project/audit/CODE_OPTIMIZATIONPLAN_PHASE_4.md`

---

### `TD-TASK-03` [MEDIUM]: One-Time Code Formatting
- **Status:** ❌ Not Started
- **Description:** Perform a one-time, automated pass across the entire repository with `black` and `isort` to fix all existing code formatting and import order issues. This will establish a clean, consistent baseline before automated checks are enforced in CI.
- **Source:** `project/audit/CODE_OPTIMIZATIONPLAN_PHASE_4.md`

---

### `SL-TASK-01` [HIGH]: Integrate Formatting Checks into CI
- **Status:** ❌ Not Started
- **Description:** Integrate `black`, `isort`, and `flake8` into the CI pipeline. The build must fail if any of these checks do not pass. This corresponds to Stage 1 of the Super-Lint plan.
- **Source:** `project/audit/CODE_OPTIMIZATIONPLAN_PHASE_4.md`

---

### `SL-TASK-02` [HIGH]: Integrate Type and Security Checks into CI
- **Status:** ❌ Not Started
- **Description:** Integrate `mypy` and `bandit` into the CI pipeline. The build must fail on any type errors or high/medium severity security issues. This corresponds to Stage 1 of the Super-Lint plan and depends on `TD-TASK-01`.
- **Source:** `project/audit/CODE_OPTIMIZATIONPLAN_PHASE_4.md`

---

### `SL-TASK-03` [MEDIUM]: Develop Custom Architectural Linting Script
- **Status:** ❌ Not Started
- **Description:** Develop the custom Python script for CI as outlined in Stage 2 of the Super-Lint plan. The script will enforce documentation linkages for endpoints, feature specs, and the traceability matrix, and check for basic docstring coverage.
- **Source:** `project/audit/CODE_OPTIMIZATIONPLAN_PHASE_4.md`

---

### `SL-TASK-04` [LOW]: Update Task Checklist
- **Status:** ❌ Not Started
- **Description:** Update the project's `task_checklist.md` (or create a `CONTRIBUTING.md`) with a formal code review checklist for reviewers, as outlined in Stage 3 of the Super-Lint plan.
- **Source:** `project/audit/CODE_OPTIMIZATIONPLAN_PHASE_4.md`

---

### `SL-TASK-05` [LOW]: Document Code Scoring Rubric
- **Status:** ❌ Not Started
- **Description:** Document the 0-10 code scoring rubric and the process for scheduled documentation reviews, as outlined in Stage 3 of the Super-Lint plan.
- **Source:** `project/audit/CODE_OPTIMIZATIONPLAN_PHASE_4.md`
---
### `LOG-TASK-01` [HIGH]: Implement Core Extendable Logging Service
- **Status:** ❌ Not Started
- **Description:** Implement the core `LoggingService` and the `BaseLogHandler` interface. The service will act as a dispatcher and manage a registry of different log handlers. This is the foundational task for the new logging system.
- **Source:** `project/LOGGING_SYSTEM_DESIGN.md`

---
### `LOG-TASK-02` [HIGH]: Implement FileStreamHandler for System Logs
- **Status:** ❌ Not Started
- **Description:** Create the `FileStreamHandler` to tail the main application log file. Implement the logic for efficient, real-time streaming of new log lines.
- **Source:** `project/LOGGING_SYSTEM_DESIGN.md`

---
### `LOG-TASK-03` [MEDIUM]: Implement JsonAuditHandler for Audit Logs
- **Status:** ❌ Not Started
- **Description:** Create the `JsonAuditHandler` to capture and format specific audit events into a structured JSON format and write them to a dedicated audit log file.
- **Source:** `project/LOGGING_SYSTEM_DESIGN.md`

---
### `LOG-TASK-04` [MEDIUM]: Implement DatabaseJobLogHandler for Job Logs
- **Status:** ❌ Not Started
- **Description:** Create the `DatabaseJobLogHandler` to write logs for long-running tasks (like downloads) to a new `job_logs` table in the database, linking them with a `job_id`.
- **Source:** `project/LOGGING_SYSTEM_DESIGN.md`

---
### `LOG-TASK-05` [HIGH]: Create API Endpoint for System Log Streaming
- **Status:** ❌ Not Started
- **Description:** Implement the `GET /api/logs/system/stream` endpoint using FastAPI's `StreamingResponse` to serve logs from the `FileStreamHandler`.
- **Source:** `project/LOGGING_SYSTEM_DESIGN.md`

---
### `LOG-TASK-06` [MEDIUM]: Create API Endpoint for Audit Logs
- **Status:** ❌ Not Started
- **Description:** Implement the `GET /api/logs/audit` endpoint to allow querying of the structured JSON audit logs, with support for filtering.
- **Source:** `project/LOGGING_SYSTEM_DESIGN.md`

---
### `LOG-TASK-07` [MEDIUM]: Create API Endpoint for Job Logs
- **Status:** ❌ Not Started
- **Description:** Implement the `GET /api/logs/jobs/{job_id}` endpoint to retrieve all logs associated with a specific job from the database.
- **Source:** `project/LOGGING_SYSTEM_DESIGN.md`
