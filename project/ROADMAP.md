# Zotify API — Execution Plan

**File:** `docs/projectplan/ROADMAP.md`
**Maintainer:** Jules
**Last Updated:** 2025-08-10 # JULES-NOTE: Realigned with codebase reality.
**Purpose:** This document outlines the high-level phases of development. For a detailed breakdown of tasks, see the [Execution Plan](./EXECUTION_PLAN.md).
**Status:** Live Document

> **Note on Future Ambitions:** This roadmap outlines the currently committed phases of work. A separate document, the [`FUTURE_ENHANCEMENTS.md`](./FUTURE_ENHANCEMENTS.md), serves as a "parking lot" for new ideas, long-term ambitions, and product vision that are not yet part of the active roadmap.

---

## 🚀 Snitch Module Development

This section tracks the development of the `snitch` helper application for handling OAuth callbacks.

| Phase | Status | Notes |
|-------|--------|-------|
| Phase 1: Initial Listener | ❌ | Conceptual design only. No implementation. |
| Phase 2: Secure Callback (Zero Trust) | 🟡 | In Progress. Implementing end-to-end payload encryption. See `PHASE_2_ZERO_TRUST_DESIGN.md`. |
| Phase 3: Code & Structure Refactor | ❌ | Not Started. |
| Phase 4: Secure POST Endpoint | ❌ | Not Started. |
| Phase 5: Cross-Platform IPC | ❌ | Not Started. |

---

## 🛠️ Developer Tooling

This section tracks the development of tools to aid in the development and testing of the Zotify API.

| Tool | Status | Notes |
|------|--------|-------|
| `gonk-testUI` | ✅ | A standalone web-based UI for API testing and database browsing. |

---

## 🏛️ Architectural Refactoring

This section tracks major architectural initiatives.

| Task | Status | Notes |
|------|--------|-------|
| Unified Database Layer | ✅ | Migrated all persistence to a unified SQLAlchemy backend. |
| Provider Abstraction Layer | ✅ | Implemented a provider interface and refactored Spotify into a connector. |
| Generic Error Handling Module | ✅ | A centralized error handling system has been implemented and verified. |

---

## 🔁 Structure and Update Policy

- **This file is mandatory and must be maintained after each major task or roadmap update.**
- **Each task must be marked with status:**
  - ✅ = Done
  - 🟡 = In Progress
  - ❌ = Not Started
- **Link each task to GitHub Issues (if available).**
- Completion Reports must update this file.
- Tightly linked to:
  - `spotify_gap_alignment_report.md`
  - `task_checklist.md`
  - `spotify_fullstack_capability_blueprint.md`

---

## ✅ Phase 0–2: Foundational Setup (Done)

- ✅ Repo and CI layout
- ✅ `webUI-baseline` branch and CLI extraction
- ✅ FastAPI skeleton with proper folder structure
- ✅ GitHub Actions: ruff, mypy, bandit, pytest
- ✅ `.env` handling for dev/prod switching
- ✅ Modular API layout prepared
- ✅ Basic Makefile and doc references

---

## ✅ Phase 3–5: Core API + Testing (Done)

- ✅ API endpoints for albums, tracks, metadata
- ✅ Notification endpoints # JULES-NOTE: Verified as functional.
- ✅ FastAPI response model scaffolding
- ✅ Pytest suite with example cases
- ✅ Full devdocs + API doc integration
- ✅ Reverse proxy support for /docs access
- ✅ Initial user system wiring (stub)
- ❌ Security layer with role-based examples # JULES-NOTE: No role-based security layer is implemented.
- ✅ CI passing for all environments
- ✅ `README.md` and `manual.md` updated with purpose explanation # JULES-NOTE: A full documentation overhaul has since been completed to align all documents with the codebase.

---

## 🟡 Phase 6: Fork-Specific Enhancements (Mostly Complete)

- ❌ GDPR and /privacy/data endpoint # JULES-NOTE: This feature is not implemented. The endpoint does not exist.
- ✅ Admin key and audit logging (basic)
- ✅ Documentation clarification integration (Jules task)
- 🟡 API key revocation flow (pending)
- 🟡 Docs: dev guide + operations guide split

---

## 🟡 Phase 7: Full Spotify Feature Integration (WIP)

| Task | Status | Notes |
|------|--------|-------|
| Library sync endpoints (read/pull) | ✅ | Fetched via Zotify CLI |
| Library sync endpoints (write/push) | ❌ | Needs mutation layer |
| Playlist list/fetch endpoints | ✅ | Completed in Phase 5 |
| Playlist creation + modification | ✅ | # JULES-NOTE: Core API endpoints for this are functional. |
| Webhook support base class | ❌ | Needed for Phase 8 |
| Admin API key: revoke + rotate | 🟡 | Core logic in draft |
| Expand CI to track coverage | ❌ | Not yet prioritized |
| DevOps templates (.github) | ❌ | Basic issue template only |

---

## ❌ Phase 8: Automation Layer

| Task | Status | Notes |
|------|--------|-------|
| Automation trigger model | ❌ | Event-based wiring required |
| Rules engine (CLI hooks) | ❌ | Phase design needed |
| Global config endpoint | ❌ | Setup defaults via admin API |

---

## ❌ Phase 9: Admin + Settings API

| Task | Status | Notes |
|------|--------|-------|
| Admin UI access tokens | ❌ | Secure tokens for config UI |
| Log access endpoints | ❌ | Tail + grep support |
| System info/reporting API | 🟡 | # JULES-NOTE: Partially implemented. /uptime and /env are functional. Disk/memory usage is not. |
| Background job management | 🟡 | In-memory download queue processor implemented. |

---

## ❌ Phase 10: Finalization & Release Readiness

| Task | Status | Notes |
|------|--------|-------|
| API versioning headers | ❌ | Core schema lock-in |
| Release packaging | ❌ | Makefile targets + GitHub release |
| Docs polish | ❌ | Archive reports, blueprints |
| Test suite coverage: 95% | ❌ | Stubbed + real endpoints |

---

## 🟡 Phase 11: Core Observability

- **Extendable Logging System**
  - See detailed breakdown in `project/LOGGING_PHASES.md`.
  - Current status: Phases 1 & 2 in progress (Core Service + Developer API).
  - All further phases (3–7) tracked and governed centrally.

---

## ❌ Phase 12: Code Quality & Enforcement (Super-Lint)

| Task | Status | Notes |
|------|--------|-------|
| Define Super-Lint Action Plan | ✅ | New design document `PHASE4_SUPERLINT_PLAN.md` created. |
| Foundational Setup | ❌ | Implementation tasks added to backlog (`LINT-TASK-01`). |
| CI Integration (Advisory Mode) | ❌ | Implementation tasks added to backlog (`LINT-TASK-02`). |
| CI Integration (Enforcement Mode) | ❌ | Implementation tasks added to backlog (`LINT-TASK-03`). |
| Local Enforcement (Pre-commit) | ❌ | Implementation tasks added to backlog (`LINT-TASK-04`). |

---

## 📋 Live TODO Queue (Sorted by Urgency)

- [ ] Create mutation layer for playlist management
- [ ] Finalize admin API key lifecycle (revoke, audit, rotate)
- [ ] Sync task_checklist.md with new report policy
- [ ] Wire `ROADMAP.md` to CI release candidate flow
- [ ] Prepare Phase 8 strategy doc

---

## 🧠 Notes

- Certain planned items, such as the Webhook/Event System, are intentionally deferred and tracked in `FUTURE_ENHANCEMENTS.md` until they are activated in a roadmap phase.
- `ROADMAP.md` is the only file allowed to define global task state.
- Phase transitions are **not time-based** but milestone-based.
- All Jules task prompts **must update this file** upon completion.
- Link to any task artifacts (e.g. `/docs/projectplan/completions/`).

---
