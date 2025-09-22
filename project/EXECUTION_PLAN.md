# Execution Plan

**Status:** Live Document

This document provides a detailed breakdown of the tasks required to fulfill the [Canonical Roadmap](./ROADMAP.md).

**Note on "Code QA":** This is a mandatory step for every phase. It involves assessing all new or modified source code against the rubric in the `API_DEVELOPER_GUIDE.md` and updating the `CODE_QUALITY_INDEX.md` accordingly.

## Phase 0–2: Foundational Setup
**Goal:** Establish project skeleton, tooling, basic API layout.
**Status:** ✅ Done
**Steps:**
- ✅ Set up repository structure and version control.
- ✅ Configure CI pipelines (ruff, mypy, bandit, pytest).
- ✅ Implement `.env` environment handling for dev/prod modes.
- ✅ Build FastAPI skeleton with modular folder structure.
- ✅ Establish basic Makefile and documentation references.
- ✅ Code QA

## Phase 3 – Core API Implementation
**Goal:** Deliver core API functionality and test coverage.
**Status:** ✅ Done
**Steps:**
- ✅ Implemented core endpoints: albums, tracks, metadata, downloads, playlists.
- ✅ Notification endpoints added with proper response models.
- ✅ Pytest suite covering core API.
- ✅ OpenAPI/Swagger integration.
- ✅ Reverse proxy support for /docs.
- ✅ Stable CI passes and code QA.

## Phase 4 / 3a – Authentication & User System
**Goal:** Implement a robust authentication system and user-specific features.
**Status:** ✅ Done
**Steps:**
- ✅ JWT-based authentication implemented.
- ✅ /auth/register and /auth/login endpoints.
- ✅ User-specific endpoints protected: /user/profile, /user/preferences, /user/liked, /user/history.
- ✅ Notifications preference added to user schema and database; migration script included.
- ✅ Tests for auth flow and protected endpoints.
- ✅ Documentation updated (API_REFERENCE.md, OpenAPI spec).

## Phase 5 / 3b – Testing, Documentation & Gonk Integration
**Goal:** Provide comprehensive testing tools and user documentation.
**Status:** ✅ Done
**Steps:**
- ✅ Gonk CLI (Gonk/GonkCLI) with login, profile, preferences, liked, history commands.
- ✅ GonkUI (Gonk/GonkUI) panel for the same CLI functionality.
- ✅ Internal/API JWT testing toggle (--api for CLI, toggle button in UI).
- ✅ Expanded tests covering CLI, UI, and JWT integration.
- ✅ Comprehensive user manual with examples added.

## Phase 6: Fork-Specific Enhancements
**Goal:** Implement enhancements specific to client forks and improve docs.
**Status:** 🟡 In Progress
**Steps:**
- ✅ Integrate admin key and basic audit logging.
- 🟡 Add API key revocation and rotation workflows (in progress).
- ❌ Split developer guide and operations guide documentation.
- ✅ Clarify existing documentation with realignment tasks. # JULES-NOTE: A comprehensive documentation overhaul was completed.
- ❌ Address GDPR and `/privacy/data` endpoints (pending). # JULES-NOTE: Confirmed, this feature is not implemented.
- [ ] Code QA

## Phase 7: Full Spotify Feature Integration
**Goal:** Complete Spotify integration with full CRUD and sync features.
**Status:** 🟡 In Progress
**Steps:**
- 🟡 Implement library sync endpoints for both read (fetch) and write (push) operations. # JULES-NOTE: Read is functional, write is not.
- ✅ Finalize playlist management endpoints: creation, modification, deletion. # JULES-NOTE: Core CRUD endpoints for playlists are already functional.
- ❌ Build webhook support base class for event-driven updates (future).
- ❌ Expand CI to include code coverage tracking.
- ❌ Prepare DevOps templates (.github workflows, issue templates).
- [ ] Code QA

## Phase 8: Extensibility & Automation
**Goal:** Make the Zotify API a truly extensible platform and introduce event-based automation.
**Status:** ❌ Not Started
**Steps:**
- ❌ **Dynamic Plugin System:** Design and implement a dynamic plugin system (e.g., using entry points) for custom components. (Source: `DYNAMIC_PLUGIN_PROPOSAL.md`)
- ❌ **Providers as Plugins:** Refactor the existing provider model to use the new plugin system.
- ❌ **External Integrations:** Develop reference implementations for Node-RED and Home Assistant. (Source: `LOW_CODE_PROPOSAL.md`, `HOME_AUTOMATION_PROPOSAL.md`)
- ❌ **Automation Triggers:** Design and implement automation trigger models for an event-based rules engine.
- [ ] Code QA

## Phase 9: Admin + Settings API
**Goal:** Provide administrative APIs and system monitoring tools.
**Status:** 🟡 In Progress
**Steps:**
- ❌ Develop secure UI access token management.
- ❌ Add endpoints for log access with filtering support.
- 🟡 Implement system info and reporting endpoints (uptime, env, disk/memory). # JULES-NOTE: Partially implemented. /uptime and /env are functional.
- 🟡 Introduce background job management for sync tasks. # JULES-NOTE: The foundational in-memory queue processing logic has been implemented for the Downloads Subsystem.
- [ ] Code QA

## Phase 10: Finalization & Release Readiness
**Goal:** Lock API schema, prepare release packaging and finalize docs.
**Status:** ❌ Not Started
**Steps:**
- ❌ Add API versioning headers for backward compatibility.
- ❌ Implement release packaging workflows and Makefile targets.
- ❌ Polish documentation, archive previous reports and blueprints.
- ❌ Achieve 95% test coverage, covering both stubbed and real endpoints.
- [ ] Code QA

## Phase 11: Developer Tooling
**Goal:** Provide tools to improve the developer experience and testing workflow.
**Status:** ✅ Done
**Steps:**
- ✅ Implement `Gonk/GonkUI`: A standalone web-based UI for API testing and database browsing with `sqlite-web`.
- ✅ Code QA

---

## Documentation

**Goal:** Ensure documentation is clear, accurate, and serves as a reliable source of truth for both developers and users.
**Status:** 🟡 In Progress
**Steps:**
- [ ] Maintain `project/api/endpoints.yaml` as the authoritative baseline for planned vs. implemented endpoints.
