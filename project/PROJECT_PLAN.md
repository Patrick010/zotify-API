# Zotify API Project Plan

**Date:** 2025-09-01
**Author:** Jules

**Reference Links:**
- **Roadmap:** `./ROADMAP.md`
- **Project Initiation Document (PID):** `./PID.md`
- **API Reference:** `../api/docs/reference/API_REFERENCE.md`
- **Traceability Matrix:** `./TRACEABILITY_MATRIX.md`

---

## 1. Executive Summary

**Purpose:**
The Zotify API project is a strategic refactor and enhancement of the original Zotify CLI tool. Its purpose is to transform the tool into a robust, scalable, and provider-agnostic API framework. This enables advanced automation, third-party integrations, and a choice of interfaces (CLI, Web) for developers and end-users.

**Scope:**
The project encompasses the core API, a developer testing UI (`gonk-testUI`), and a secure OAuth helper application (`snitch`). The current scope is focused on completing the "Platform Extensibility" phase, which involves establishing a dynamic plugin system and creating reference integrations.

**Dependencies:**
- The core API's download functionality is dependent on an underlying, fork-specific version of **Librespot**.
- The CLI-based authentication flow is dependent on the **Snitch** helper application.

---

## 2. Milestones & Phases

This plan is aligned with the high-level phases defined in the `ROADMAP.md`.

### Phase 1: Core Platform Stability & Security (✅ Done)
This phase focused on refactoring the core architecture, resolving critical regressions, and hardening the platform.
- **Owner:** Jules
- **Completed:** ~2025-08-31

### Phase 2: Platform Extensibility (Next Up)
This is the current, active phase. The goal is to make the Zotify API a truly extensible platform.

| Sub-Task | Description | Owner | Target Date | Status |
|---|---|---|---|---|
| **Archive Cleanup** | Consolidate and clean up the `project/archive` directory. | Jules | TBD | `In Progress` |
| **Dynamic Plugin System**| Implement a dynamic plugin system for logging sinks. | TBD | TBD | `Planned` |
| **Refactor Providers** | Refactor the Spotify provider as a standalone plugin. | TBD | TBD | `Planned` |
| **Low-Code Integration**| Create a Node-RED reference implementation. | TBD | TBD | `Planned` |
| **Home Automation** | Create a Home Assistant reference implementation. | TBD | TBD | `Planned` |

### Phase 3: Future Vision (Planned)
This phase will focus on expanding the core feature set based on the established, extensible architecture.
- **Owner:** TBD
- **Target Date:** TBD
- **Sub-Tasks:** Implement missing API baseline endpoints, full two-way sync, advanced API governance, and an enhanced UI.

---

## 3. Module Breakdown

### Core API
- **Purpose:** The central FastAPI application that provides all functionality.
- **Dependencies:** Librespot, Snitch (for CLI auth).
- **Current Status:** Stable. Core architecture is refactored with distinct layers for services, persistence, and providers.
- **Planned Next Steps:** Implement high-priority items from the `BACKLOG.md`, starting with the "Platform Extensibility" phase.

### `gonk-testUI` Module
- **Purpose:** A standalone developer testing UI for the API.
- **Dependencies:** The Core API's OpenAPI schema (`openapi.json`).
- **Current Status:** Stable and functional.
- **Planned Next Steps:** No major enhancements planned. Will be updated as needed to support new API features.

### `snitch` Module
- **Purpose:** A secure helper application for managing the CLI OAuth callback flow.
- **Dependencies:** None. It is a self-contained Go application.
- **Current Status:** Stable and functional after a significant refactoring.
- **Planned Next Steps:** No major enhancements planned. Future work might include adding an integration test to the CI pipeline to prevent regressions.

---

## 4. Alignment with Design

All development work must align with the project's core design documents.
- **High-Level Design:** All new features must be consistent with the architectural principles outlined in `project/HIGH_LEVEL_DESIGN.md`.
- **Low-Level Design:** Specific implementation details, endpoint definitions, and subsystem designs are documented in `project/LOW_LEVEL_DESIGN.md`. All new features must be designed here before implementation.
- **Deferred Features:** Features that are not part of the active roadmap are tracked in `project/FUTURE_ENHANCEMENTS.md` and are not included in the HLD/LLD until they are officially planned.

---

## 5. Quality & Compliance Tasks

Adherence to quality and compliance is mandatory for all tasks.
- **Testing:** All new code requires corresponding unit and/or integration tests. The full test suite must pass before submission (run `python3 scripts/linter.py`).
- **Documentation:** All documentation must be kept in sync with code changes. This is enforced by the `scripts/linter.py` script.
- **Code Quality:** Code must be analyzed with `ruff` and `mypy`. Scores are tracked in the `CODE_QUALITY_INDEX.md` files.
- **Security & Privacy:** All changes must be reviewed for security implications as per `project/SECURITY.md`. Any feature handling user data must consider the requirements of `api/docs/system/PRIVACY_COMPLIANCE.md`.

---

## 6. Task List / Backlog Integration

The official, tactical list of tasks is maintained in `project/BACKLOG.md`. All tasks are prioritized and must meet the readiness criteria defined in the `PID.md` before work can begin.

### Current High-Priority Tasks:
- **`FEAT-PRIVACY-01` (Planned):** Implement the newly designed GDPR endpoints.
- **`FEAT-SDK-01` (Planned):** Implement the dynamic plugin system for the logging framework.
- **`DOC-OVERHAUL-01` (Planned):** Perform a comprehensive quality overhaul of all project documentation.

### Ongoing Tasks:
- **Archive Cleanup (In Progress):** The initial documentation cleanup task that precedes the larger `DOC-OVERHAUL-01` task.
