# Project Backlog

**Date:** 2025-08-18
**Status:** Live Document

## 1. Purpose

This document serves as the tactical backlog for the Zotify API Platform. It contains a list of clearly defined, approved tasks for future implementation. The process for managing this backlog is defined in the `PID.md`.

---

## 2. Backlog Items

All new tasks added to this backlog **must** use the template defined in the `PID.md`'s "Project Controls" section.

### High Priority

-   **Task ID:** `FEAT-QA-GATE-01`
-   **Source:** `project/proposals/QA_GATE_IMPLEMENTATION_PLAN.md`
-   **Priority:** CRITICAL
-   **Dependencies:** None
-   **Description:** Implement Phase 1 of the new QA Gate system. This involves creating the main `qa_gate.py` script, installing new Python dependencies (`Radon`, `mutmut`), and implementing all Python-specific code quality checks (ruff, pytest, mutmut, radon).
-   **Acceptance Criteria:**
    -   `[ ]` The `scripts/qa_gate.py` script is created and functional for Python code.
    -   `[ ]` The script successfully runs all specified tools and checks their output against the defined thresholds.
    -   `[ ]` A new `api/docs/manuals/QA_GATE.md` document is created and explains the new system.
-   **Estimated Effort:** Large

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

### FEAT-ZOTIFY-PLAYLISTS-01
- **Task ID:** `FEAT-ZOTIFY-PLAYLISTS-01`
- **Audit Ref:** `AR-013`
- **Source:** `Trace Policy: Retrospective — added for alignment completeness.`
- **Priority:** LOW
- **Dependencies:** None
- **Description:** Retrospective alignment for the initial implementation of the core playlist management service, including creating, reading, and managing user playlists.
- **Acceptance Criteria:**
  - [x] The `playlists_service.py` module provides core business logic for playlists.
  - [x] The `playlists.py` routes expose this functionality via the API.
  - [x] The feature is fully aligned in the `ALIGNMENT_MATRIX.md` and design documents.
- **Estimated Effort:** Small

### FEAT-ZOTIFY-TRACKS-01
- **Task ID:** `FEAT-ZOTIFY-TRACKS-01`
- **Audit Ref:** `AR-017`
- **Source:** `Trace Policy: Retrospective — added for alignment completeness.`
- **Priority:** LOW
- **Dependencies:** None
- **Description:** Retrospective alignment for the core track management feature, including API endpoints for retrieving track information.
- **Acceptance Criteria:**
  - [x] The `tracks_service.py` module provides core business logic for tracks.
  - [x] The `tracks.py` routes expose this functionality via the API.
  - [x] The feature is fully aligned in the `ALIGNMENT_MATRIX.md` and design documents.
- **Estimated Effort:** Small

### FEAT-ZOTIFY-SEARCH-01
- **Task ID:** `FEAT-ZOTIFY-SEARCH-01`
- **Audit Ref:** `AR-014`
- **Source:** `Trace Policy: Retrospective — added for alignment completeness.`
- **Priority:** LOW
- **Dependencies:** None
- **Description:** Retrospective alignment for the core search feature, which allows users to search for tracks, albums, and artists.
- **Acceptance Criteria:**
  - [x] The `search.py` service provides the core business logic for search.
  - [x] The `search.py` route exposes this functionality via the API.
  - [x] The feature is fully aligned in the `ALIGNMENT_MATRIX.md` and design documents.
- **Estimated Effort:** Small

### FEAT-ZOTIFY-USER-01
- **Task ID:** `FEAT-ZOTIFY-USER-01`
- **Audit Ref:** `AR-018`
- **Source:** `Trace Policy: Retrospective — added for alignment completeness.`
- **Priority:** LOW
- **Dependencies:** None
- **Description:** Retrospective alignment for the core user management feature, including API endpoints for retrieving user profiles and preferences.
- **Acceptance Criteria:**
  - [x] The `user_service.py` module provides core business logic for user management.
  - [x] The `user.py` route exposes this functionality via the API.
  - [x] The feature is fully aligned in the `ALIGNMENT_MATRIX.md` and design documents.
- **Estimated Effort:** Small

### FEAT-ZOTIFY-SYNC-01
- **Task ID:** `FEAT-ZOTIFY-SYNC-01`
- **Audit Ref:** `AR-015`
- **Source:** `Trace Policy: Retrospective — added for alignment completeness.`
- **Priority:** LOW
- **Dependencies:** None
- **Description:** Retrospective alignment for the core sync feature, which handles synchronization of data between the local database and the music provider.
- **Acceptance Criteria:**
  - [x] The `sync_service.py` module provides core business logic for synchronization.
  - [x] The `sync.py` route exposes this functionality via the API.
  - [x] The feature is fully aligned in the `ALIGNMENT_MATRIX.md` and design documents.
- **Estimated Effort:** Small

### FEAT-ZOTIFY-CACHE-01
- **Task ID:** `FEAT-ZOTIFY-CACHE-01`
- **Audit Ref:** `AR-008`
- **Source:** `Trace Policy: Retrospective — added for alignment completeness.`
- **Priority:** LOW
- **Dependencies:** None
- **Description:** Retrospective alignment for the cache management feature, which provides endpoints for inspecting and clearing the application cache.
- **Acceptance Criteria:**
  - [x] The `cache_service.py` module provides core business logic for cache management.
  - [x] The `cache.py` route exposes this functionality via the API.
  - [x] The feature is fully aligned in the `ALIGNMENT_MATRIX.md` and design documents.
- **Estimated Effort:** Small

### FEAT-ZOTIFY-NOTIFICATIONS-01
- **Task ID:** `FEAT-ZOTIFY-NOTIFICATIONS-01`
- **Audit Ref:** `AR-012`
- **Source:** `Trace Policy: Retrospective — added for alignment completeness.`
- **Priority:** LOW
- **Dependencies:** None
- **Description:** Retrospective alignment for the notifications feature, which provides endpoints for managing notifications.
- **Acceptance Criteria:**
  - [x] The `notifications_service.py` module provides core business logic for notifications.
  - [x] The `notifications.py` route exposes this functionality via the API.
  - [x] The feature is fully aligned in the `ALIGNMENT_MATRIX.md` and design documents.
- **Estimated Effort:** Small

### FEAT-ZOTIFY-NETWORK-01
- **Task ID:** `FEAT-ZOTIFY-NETWORK-01`
- **Audit Ref:** `AR-011`
- **Source:** `Trace Policy: Retrospective — added for alignment completeness.`
- **Priority:** LOW
- **Dependencies:** None
- **Description:** Retrospective alignment for the network utilities feature, which provides endpoints for network-related diagnostics.
- **Acceptance Criteria:**
  - [x] The `network_service.py` module provides core business logic for network utilities.
  - [x] The `network.py` route exposes this functionality via the API.
  - [x] The feature is fully aligned in the `ALIGNMENT_MATRIX.md` and design documents.
- **Estimated Effort:** Small

### FEAT-ZOTIFY-WEBHOOKS-01
- **Task ID:** `FEAT-ZOTIFY-WEBHOOKS-01`
- **Audit Ref:** `AR-019`
- **Source:** `Trace Policy: Retrospective — added for alignment completeness.`
- **Priority:** LOW
- **Dependencies:** None
- **Description:** Retrospective alignment for the webhooks feature, which provides endpoints for managing webhooks.
- **Acceptance Criteria:**
  - [x] The `webhooks.py` service provides core business logic for webhooks.
  - [x] The `webhooks.py` route exposes this functionality via the API.
  - [x] The feature is fully aligned in the `ALIGNMENT_MATRIX.md` and design documents.
- **Estimated Effort:** Small

### FEAT-ZOTIFY-DATABASE-01
- **Task ID:** `FEAT-ZOTIFY-DATABASE-01`
- **Audit Ref:** `AR-004`
- **Source:** `Trace Policy: Retrospective — added for alignment completeness.`
- **Priority:** LOW
- **Dependencies:** None
- **Description:** Retrospective alignment for the core database management components, including the SQLAlchemy ORM, Alembic migrations, and related documentation.
- **Acceptance Criteria:**
  - [x] The database module provides core ORM and session management.
  - [x] Alembic is configured for schema migrations.
  - [x] The feature is fully aligned in the `ALIGNMENT_MATRIX.md` and design documents.
- **Estimated Effort:** Small

### FEAT-ZOTIFY-GONK-01
- **Task ID:** `FEAT-ZOTIFY-GONK-01`
- **Audit Ref:** `AR-024`
- **Source:** `Trace Policy: Retrospective — added for alignment completeness.`
- **Priority:** LOW
- **Dependencies:** None
- **Description:** Retrospective alignment for the Gonk Test UI, a standalone developer tool for testing the Zotify API.
- **Acceptance Criteria:**
  - [x] The Gonk Test UI provides a web interface and CLI for API interaction.
  - [x] The feature is fully aligned in the `ALIGNMENT_MATRIX.md` and design documents.
- **Estimated Effort:** Small

### FEAT-ZOTIFY-SNITCH-01
- **Task ID:** `FEAT-ZOTIFY-SNITCH-01`
- **Audit Ref:** `AR-025`
- **Source:** `Trace Policy: Retrospective — added for alignment completeness.`
- **Priority:** LOW
- **Dependencies:** None
- **Description:** Retrospective alignment for the Snitch microservice, a helper application to securely manage the OAuth callback flow.
- **Acceptance Criteria:**
  - [x] The Snitch microservice is a self-contained Go application.
  - [x] The feature is fully aligned in the `ALIGNMENT_MATRIX.md` and design documents.
- **Estimated Effort:** Small

### FEAT-ZOTIFY-GOVERNANCE-01
- **Task ID:** `FEAT-ZOTIFY-GOVERNANCE-01`
- **Audit Ref:** `AR-027, AR-030, AR-065, AR-066`
- **Source:** `Trace Policy: Retrospective — added for alignment completeness.`
- **Priority:** LOW
- **Dependencies:** None
- **Description:** Retrospective alignment for the core project governance framework, including the agent operating manual, QA policies, and automated linting and validation scripts.
- **Acceptance Criteria:**
  - [x] The core governance documents (`AGENTS.md`, `QA_GOVERNANCE.md`) are defined.
  - [x] The core governance scripts (`linter.py`, `repo_inventory_and_governance.py`) are implemented.
  - [x] The feature is fully aligned in the `ALIGNMENT_MATRIX.md` and design documents.
- **Estimated Effort:** Medium

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
