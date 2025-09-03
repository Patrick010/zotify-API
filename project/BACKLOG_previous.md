# Project Backlog

**Date:** 2025-08-18
**Status:** Live Document

## 1. Purpose

This document serves as the tactical backlog for the Zotify API Platform. It contains a list of clearly defined, approved tasks for future implementation. The process for managing this backlog is defined in the `PID.md`.

---

## 2. Backlog Items

All new tasks added to this backlog **must** use the template defined in the `PID.md`'s "Project Controls" section.

### High Priority

-   **Task ID:** `FEAT-PRIVACY-01`
-   **Source:** `project/LOW_LEVEL_DESIGN.md`
-   **Priority:** HIGH
-   **Dependencies:** None
-   **Description:** Implement the GDPR-compliant endpoints for data export and erasure, as designed in the Low-Level Design document. This includes `GET /privacy/data` and `DELETE /privacy/data`.
-   **Acceptance Criteria:**
    -   `[ ]` The `GET /privacy/data` endpoint is implemented and returns all personal data for the authenticated user.
    -   `[ ]` The `DELETE /privacy/data` endpoint is implemented and securely deletes all personal data for the authenticated user.
    -   `[ ]` The endpoints are protected by authentication.
    -   `[ ]` The changes are documented in the `API_REFERENCE.md`.
-   **Estimated Effort:** Medium

-   **Task ID:** `FEAT-SDK-01`
-   **Source:** `project/DYNAMIC_PLUGIN_PROPOSAL.md`
-   **Priority:** HIGH
-   **Dependencies:** None
-   **Description:** Implement the core dynamic plugin system for the Flexible Logging Framework, allowing third-party developers to create and install custom logging sinks.
-   **Acceptance Criteria:**
    -   `[ ]` The `LoggingService` can discover and load plugins defined via `entry_points`.
    -   `[ ]` A simple reference plugin can be installed and used successfully.
    -   `[ ]` A `PLUGIN_DEVELOPMENT_GUIDE.md` is created.
-   **Estimated Effort:** Large

-   **Task ID:** `DOC-OVERHAUL-01`
-   **Source:** User Directive
-   **Priority:** HIGH
-   **Dependencies:** None
-   **Description:** Perform a comprehensive quality overhaul of all project documentation (`.md` files) across the `project/`, `api/docs/`, and `snitch/docs/` directories to align them with the high standard of the `LOGGING_GUIDE.md`.
-   **Acceptance Criteria:**
    -   `[ ]` All specified documents are reviewed and rewritten for clarity, accuracy, and detail.
-   **Estimated Effort:** Large

### Medium Priority

-   **Task ID:** `FEAT-INTEGRATION-01`
-   **Source:** `project/LOW_CODE_PROPOSAL.md`
-   **Priority:** MEDIUM
-   **Dependencies:** A stable API
-   **Description:** Create a reference implementation of a Node-RED integration by developing a `node-red-contrib-zotify` package with custom nodes for core API functions.
-   **Acceptance Criteria:**
    -   `[ ]` A basic set of nodes (e.g., Search, Download) is created and published.
-   **Estimated Effort:** Medium

-   **Task ID:** `FEAT-INTEGRATION-02`
-   **Source:** `project/HOME_AUTOMATION_PROPOSAL.md`
-   **Priority:** MEDIUM
-   **Dependencies:** A stable API
-   **Description:** Create a reference implementation of a Home Assistant integration, exposing Zotify as a `media_player` entity and providing services for automations.
-   **Acceptance Criteria:**
    -   `[ ]` A custom component for Home Assistant is created and published.
-   **Estimated Effort:** Medium

### Low Priority

*(This section includes tasks from a previous audit that are still relevant but are a lower priority than the new feature work.)*

-   **Task ID:** `TD-TASK-01`
-   **Source:** `project/audit/CODE_OPTIMIZATIONPLAN_PHASE_4.md#phase-4a`
-   **Priority:** LOW
-   **Dependencies:** None
-   **Description:** `Resolve mypy Blocker (e.g., conflicting module names) to enable static type checking.`
-   **Acceptance Criteria:**
    -   `[ ]` `mypy` runs successfully without configuration errors.
-   **Estimated Effort:** Small

### Technical Debt

-   **Task ID:** `TD-REFACTOR-01`
    -   **Source:** `project/LOW_LEVEL_DESIGN.md` (originally), User finding
    -   **Priority:** LOW
    -   **Dependencies:** None
    -   **Description:** The `tracks_service.py` module currently uses raw, hardcoded SQL queries instead of using the SQLAlchemy ORM and the `Track` model. This led to a schema divergence and a runtime error.
    -   **Acceptance Criteria:**
        -   `[ ]` Refactor all database operations in `tracks_service.py` to use the SQLAlchemy ORM and the `Track` model.
        -   `[ ]` Remove the temporary `artist` and `album` columns from the `Track` model if they are not needed after the refactor, or confirm they are correctly used by the ORM.
    -   **Estimated Effort:** Medium
