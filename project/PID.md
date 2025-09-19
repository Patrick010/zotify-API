# Project Initiation Document (PID)

**Project Name:** Zotify API Refactoring and Enhancement  
**Date:** 2025-08-12  
**Version:** 1.0
**Status:** Live Document

---

## 1. Full Business Case

**Justification:**  
The Zotify API was originally built as a lightweight wrapper for a single use case—interacting with Spotify through Zotify/Librespot—but without a sustainable architecture for long-term growth. It lacked persistent storage, modularity, and the flexibility to support multiple providers. This project aims to refactor and expand the API to form a robust, scalable, and provider-agnostic backend for automation, integrations, and developer tooling.

**Strategic Goals:**  
- Transition Zotify from a Spotify-only CLI wrapper into a fully modular API framework capable of integrating with multiple audio content sources.  
- Lay the foundation for a future-ready architecture that supports automation, sync, analytics, and secure multi-user workflows.  
- Deliver an API that is developer-friendly, self-documented, and scalable without major redesigns.  
- Enable both CLI and WebUI-based interactions, giving users and developers a choice of interfaces.  

**Business Benefits:**  
- **Reduced Operational Risk:** Persistent database eliminates data loss for queues, tokens, and state.  
- **Faster Development:** Cleaner, modular architecture accelerates new feature delivery.  
- **Better Scalability:** Prepared for higher load, more data, and multiple integrations.  
- **Future Expansion:** Provider-agnostic design allows easy addition of new streaming platforms.  
- **Enhanced Feature Set:** Full two-way playlist sync and advanced automation unlock entirely new workflows.  

---

## 2. Detailed Project Scope & Product Breakdown

### 2.1 In Scope
- Full audit of the codebase against documentation. *(In Progress)*  
- Refactoring to a unified, SQLAlchemy-based persistence layer.  
- Migration of all file-based and in-memory data (playlists, tokens, download jobs) to the new database.  
- Creation of a standalone developer testing UI (`gonk-testUI`) with `sqlite-web` integration.  
- Complete overhaul of system documentation (`INSTALLATION.md`, `USER_MANUAL.md`, etc.). *(In Progress)*  
- Creation of formal project management documents (Project Brief, PID).  
- Initial design and implementation of a provider-agnostic abstraction layer. *(In Progress)*  
- **Full two-way sync for Spotify playlists** as a core API feature.  

### 2.2 Out of Scope (Current Phase)
- None of the features are permanently out of scope. However, some items (e.g., **full JWT-based authentication** and other advanced security layers) are **strategic goals** for later phases, after the core architecture and sync features are complete.  

### 2.3 Main Products (Deliverables)
1. **Refactored Zotify API (v1.0):** New database architecture with modular design.  
2. **`gonk-testUI` Module (v0.1.0):** Developer testing tool with SQLite inspection.  
3. **System Documentation Set:** Fully updated `docs/system/` directory.  
4. **PRINCE2 Project Documentation:** PID, Project Brief, and supporting docs.  
5. **`scripts/start.sh`:** Unified startup script.  
6. **Spotify Two-Way Sync Module:** Bidirectional playlist sync, with conflict resolution.  

### 2.4 Deferred Features
Deferred features are tracked in `project/FUTURE_ENHANCEMENTS.md` until they are promoted to an active roadmap phase. These items are intentionally absent from design docs until scheduled for implementation.

Example of a deferred feature:
- *Webhook/Event System*

### 2.5 Supporting Modules
The Zotify Platform consists of the Core API and official supporting modules, currently:
- **Snitch — Secure OAuth Callback Helper:**
    - **Objective:** To provide a secure, reliable, and user-friendly mechanism for handling the browser-based OAuth 2.0 callback during CLI-driven authentication flows.
    - **Major Phases:** 1. Initial Implementation (Done), 2. Hardening & Integration (Planned).
    - **Delivery Checkpoints:** The module is considered complete when all tasks in the project plan are done, including full test coverage and an end-to-end integration test in the main CI pipeline.
    - **Project Plan:** `../snitch/docs/PROJECT_PLAN.md`
- **Gonk-TestUI — Frontend testing and interaction suite for validation and QA:**
    - **Objective:** To provide a standalone developer UI for easily testing all API endpoints.
    - **Project Plan:** The `gonk-testUI` module is currently simple enough not to require a separate project plan. Its development is tracked directly in the main project backlog and roadmap.

Supporting modules are developed, tracked, and governed under the same policies, workflows, and quality standards as the Core API.
**Note:** Retroactive work on these modules must be documented and incorporated into all relevant project files.

---

## 3. Stage Plans (High-Level)

- **Stage 1: Audit & Alignment** *(In Progress)* — Code/documentation gap analysis and alignment.  
- **Stage 2: Core Refactoring** *(Completed)* — Unified database, new dev UI.  
- **Stage 3: Documentation & Formalization** *(In Progress)* — Full system documentation, formal project docs.  
- **Stage 4: Provider Abstraction** *(In Progress)* — Design and partial implementation of multi-provider layer.  

---

## 4. Project Controls

- **Reporting:** Progress tracked in `project/` (`ACTIVITY.md`, `CURRENT_STATE.md`).  
- **Change Control:** All changes require proposal, approval, and re-approval if scope deviates.  
- **Handling of Postponed Tasks:** Postponed or paused tasks must be moved from the `ACTIVITY.md` log to the `BACKLOG.md` with an appropriate status. This ensures the activity log remains a clear record of completed or actively in-progress work.
- **Backlog Management and Task Qualification:** To ensure a structured and traceable workflow, the following process is mandatory for managing the `BACKLOG.md`:
  - **Task Generation:**
    - Each task added to the backlog must reference at least one source item from a live project document (e.g., `TRACEABILITY_MATRIX.md`, `USECASES.md`, `FUTURE_ENHANCEMENTS.md`).
    - All tasks must conform to the template defined in `BACKLOG.md`, including fields for Task ID, Source, Description, Dependencies, Acceptance Criteria, Effort, and Priority.
  - **Task Qualification:**
    - A task is only eligible for execution if all of its dependencies are resolved, its acceptance criteria are fully defined, and its source references are valid.
    - Priority alone is not sufficient to begin work on a task; it must meet all readiness criteria.
  - **Review and Audit:**
    - A review of the backlog will be conducted at the start of each major work cycle to ensure tasks are traceable and meet readiness criteria.
    - A periodic audit will be performed to remove unlinked or outdated tasks.
- **Quality Assurance:**  
  - Code reviews before merge.  
  - Unit/integration testing (test runner stability is a known issue).  
  - Continuous documentation updates in sync with code changes.  
  - **Logging of Changes:** All significant changes (e.g., refactors, new features) must be logged and reflected in all relevant project documentation (PID, HLD, LLD, CHANGELOG, etc.) as part of the implementation task itself. This ensures the 'living documentation' principle is maintained.
  - **Traceability Matrix Maintenance:** `TRACEABILITY_MATRIX.md` is a live document. All requirement, enhancement, or system-level changes must update the matrix in the same commit.
  - **Use Case Gap Analysis Maintenance:** Any time a new use case is added to `USECASES.md`, the `USECASES_GAP_ANALYSIS.md` must be updated to reflect its implementation status. The gap analysis will be formally reviewed once per major release cycle to ensure accuracy.
  - **Verification of Documentation Integration:** When new documents are created, a verification step must be performed to ensure they are correctly integrated and referenced in the existing documentation hierarchy (e.g., `PROJECT_REGISTRY.md`).
  - **Feature Specification Maintenance:** All new or modified functionality (including Core API, Supporting Modules, etc.) must have a corresponding, up-to-date entry in the Feature Specification documents (`api/docs/reference/FEATURE_SPECS.md`). This is a mandatory requirement for pull request approval.
  - **Structured Logging Mandate:** All new and existing functionality must use the new **Flexible Logging Framework**. This is done via the `log_event()` function, which provides a developer-centric API for creating structured logs with per-event control over destinations, severity, and tags. The framework supports tag-based routing (defined in `logging_framework.yml`) to direct logs to specific sinks, and features automatic redaction of sensitive data in production environments. The framework is the single source for all application logging. Direct use of `print()` or basic loggers is forbidden. See the `LOGGING_GUIDE.md` for full implementation details. A proposal for a future dynamic plugin system to allow for custom, third-party sinks has been documented in `DYNAMIC_PLUGIN_PROPOSAL.md`.
  - **Centralized Error Handling Mandate:** All unhandled exceptions across the entire platform (including API, background tasks, and CLI tools) must be processed by the Generic Error Handling Module. This module provides standardized error responses, structured logging, and a configurable trigger/action system for automated responses. Direct, unhandled exceptions that result in a crash or an inconsistent error format are forbidden. See `ERROR_HANDLING_DESIGN.md` and `ERROR_HANDLING_GUIDE.md` for details.
  - **Automated Documentation Workflow:** The project enforces its "living documentation" policy through a unified linter script (`scripts/linter.py`). This script handles both pre-submission verification of all project standards and standardized work logging. It is a mandatory quality gate for all contributions. See the `automated_documentation_workflow.md` feature spec for details.
  - **Preservation of Previous Versions:** Before modifying any existing project documentation (`.md` files), a copy of the file must be made with the suffix `_previous` (e.g., `PID_previous.md`). This ensures that a record of the last stable version is always available for easy rollback or comparison.

---

## 5. Risk, Issue, and Quality Registers

- **Risk Register:**  
  - *Risk:* Development tools for filesystem manipulation/testing are unreliable.  
  - *Impact:* Delays and workarounds reduce efficiency.  
  - *Mitigation:* External code review, safe file operations instead of rename/move.  

- **Issue Register:**  
  - *Issue #1:* Duplicate `devtools/` directory exists alongside `gonk-testUI/`.  
  - *Status:* Open.  
  - *Impact:* Minor clutter, no functional risk.  
  - *Action:* Cleanup in future refactor.  

- **Quality Register:**  
  - All code must be reviewed.  
  - All docs must be updated with every change.  
  - PID, `CURRENT_STATE.md`, `ACTIVITY.md` remain in sync.  

---

## 6. Project Organisation (Roles & Responsibilities)

- **Project Board / Project Executive:** Primary user — provides mandate, sets requirements, approves plans.  
- **Project Manager:** Primary user — manages flow, gives detailed direction.  
- **Senior Supplier / Lead Developer:** Jules (AI agent) — responsible for technical design, implementation, testing, and documentation.  

---

## 7. Communication Management Approach

- All communication via interactive session.  
- Jules provides regular updates and `CURRENT_STATE.md` hand-offs.  
- User provides approvals and new directives.  

---

## 8. Configuration Management Approach

- **Source Code:** Managed in Git with feature branches.  
- **Documentation:** Markdown in repo, versioned alongside code.  
- **Project State:** Tracked in living docs (`ACTIVITY.md`, `CURRENT_STATE.md`, `PID.md`).  

---

## 9. Tailoring Approach

- PRINCE2 principles applied in a minimal, agile form for a one-on-one AI/human workflow.  
- Quality, risk, and change managed through interactive process and living documentation.  
- Stage boundaries managed via user approval of new high-level plans.  

---

Appendix / References

    project/ROADMAP.md

    project/EXECUTION_PLAN.md

    project/TRACEABILITY_MATRIX.md

    project/PROJECT_REGISTRY.md

    docs/providers/spotify.md (starter)

    project/ACTIVITY.md (live)

    project/CURRENT_STATE.md (live)
