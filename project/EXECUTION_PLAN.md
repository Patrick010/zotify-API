# Execution Plan

**Status:** Live Document

This document provides a detailed breakdown of the tasks required to fulfill the [Canonical Roadmap](./ROADMAP.md).

## Phase 0–2: Foundational Setup
**Goal:** Establish project skeleton, tooling, basic API layout.
**Status:** ✅ Done
**Steps:**
- ✅ Set up repository structure and version control.
- ✅ Configure CI pipelines (ruff, mypy, bandit, pytest).
- ✅ Implement `.env` environment handling for dev/prod modes.
- ✅ Build FastAPI skeleton with modular folder structure.
- ✅ Establish basic Makefile and documentation references.

## Phase 3–5: Core API + Testing
**Goal:** Deliver core API functionality and test coverage.
**Status:** 🟡 In Progress
**Steps:**
- ✅ Implement core endpoints: albums, tracks, metadata.
- ✅ Add notification endpoints, ensure proper response models.
- ✅ Wire up Pytest suite with example test cases covering core API.
- ✅ Integrate documentation and API specs (OpenAPI/Swagger). # JULES-NOTE: Completed. A new, canonical OpenAPI spec has been generated and integrated into the documentation.
- ✅ Add reverse proxy support for `/docs`.
- 🟡 Stub initial user system wiring (authentication placeholder). # JULES-NOTE: This is largely complete. Functional endpoints for profile, preferences, etc. exist.
- ✅ Achieve stable CI passes across environments.

## Phase 6: Fork-Specific Enhancements
**Goal:** Implement enhancements specific to client forks and improve docs.
**Status:** 🟡 In Progress
**Steps:**
- ✅ Integrate admin key and basic audit logging.
- 🟡 Add API key revocation and rotation workflows (in progress).
- ❌ Split developer guide and operations guide documentation.
- ✅ Clarify existing documentation with realignment tasks. # JULES-NOTE: A comprehensive documentation overhaul was completed.
- ❌ Address GDPR and `/privacy/data` endpoints (pending). # JULES-NOTE: Confirmed, this feature is not implemented.

## Phase 7: Full Spotify Feature Integration
**Goal:** Complete Spotify integration with full CRUD and sync features.
**Status:** 🟡 In Progress
**Steps:**
- 🟡 Implement library sync endpoints for both read (fetch) and write (push) operations. # JULES-NOTE: Read is functional, write is not.
- ✅ Finalize playlist management endpoints: creation, modification, deletion. # JULES-NOTE: Core CRUD endpoints for playlists are already functional.
- ❌ Build webhook support base class for event-driven updates (future).
- ❌ Expand CI to include code coverage tracking.
- ❌ Prepare DevOps templates (.github workflows, issue templates).

## Phase 8: Automation Layer
**Goal:** Introduce event-based automation and rules engine.
**Status:** ❌ Not Started
**Steps:**
- ❌ Design and implement automation trigger models.
- ❌ Build CLI hooks for rules engine integration.
- ❌ Create global config endpoint for defaults via admin API.

## Phase 9: Admin + Settings API
**Goal:** Provide administrative APIs and system monitoring tools.
**Status:** 🟡 In Progress
**Steps:**
- ❌ Develop secure UI access token management.
- ❌ Add endpoints for log access with filtering support.
- 🟡 Implement system info and reporting endpoints (uptime, env, disk/memory). # JULES-NOTE: Partially implemented. /uptime and /env are functional.
- 🟡 Introduce background job management for sync tasks. # JULES-NOTE: The foundational in-memory queue processing logic has been implemented for the Downloads Subsystem.

## Phase 10: Finalization & Release Readiness
**Goal:** Lock API schema, prepare release packaging and finalize docs.
**Status:** ❌ Not Started
**Steps:**
- ❌ Add API versioning headers for backward compatibility.
- ❌ Implement release packaging workflows and Makefile targets.
- ❌ Polish documentation, archive previous reports and blueprints.
- ❌ Achieve 95% test coverage, covering both stubbed and real endpoints.

## Phase 11: Developer Tooling
**Goal:** Provide tools to improve the developer experience and testing workflow.
**Status:** ✅ Done
**Steps:**
- ✅ Implement `gonk-testUI`: A standalone web-based UI for API testing and database browsing with `sqlite-web`.
