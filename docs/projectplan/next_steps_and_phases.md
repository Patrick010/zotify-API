# Zotify API — Next Steps and Phase Sequencing

**File:** `docs/projectplan/next_steps_and_phases.md`
**Maintainer:** Jules
**Last Updated:** 2025-08-07
**Purpose:** This document actively tracks all planned, in-progress, and completed work across all phases. It defines each phase, breaks it down into granular tasks, and aligns all work with roadmap goals and deliverables.

---

## 🚀 Snitch Module Development

This section tracks the development of the `snitch` helper application for handling OAuth callbacks.

| Phase | Status | Notes |
|-------|--------|-------|
| Phase 1: Initial Listener | ✅ | Basic GET listener on a fixed port. |
| Phase 2: Secure State Validation | ✅ | Added mandatory `state` token validation. |
| Phase 3: Code & Structure Refactor | ✅ | Modularized into standard Go project layout. |
| Phase 4: Secure POST Endpoint | ✅ | Replaced GET with a secure POST endpoint. |
| Phase 5: Cross-Platform IPC | ✅ | Implemented secure IPC with Zotify API. |

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
- ✅ FastAPI response model scaffolding
- ✅ Pytest suite with example cases
- ✅ Full devdocs + API doc integration
- ✅ Reverse proxy support for /docs access
- ✅ Initial user system wiring (stub)
- ✅ Security layer with role-based examples
- ✅ CI passing for all environments
- ✅ `README.md` and `manual.md` updated with purpose explanation

---

## 🟡 Phase 6: Fork-Specific Enhancements (Mostly Complete)

- ✅ GDPR and `/privacy/data` endpoint
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
| Playlist creation + modification | ❌ | New CLI wrapping needed |
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
| Notification endpoints | ❌ | Include rate-limit + audit trail |
| Global config endpoint | ❌ | Setup defaults via admin API |

---

## ❌ Phase 9: Admin + Settings API

| Task | Status | Notes |
|------|--------|-------|
| Admin UI access tokens | ❌ | Secure tokens for config UI |
| Log access endpoints | ❌ | Tail + grep support |
| System info/reporting API | ❌ | Disk, memory, usage tracking |
| Background job management | ❌ | Pause/resume/restart sync jobs |

---

## ❌ Phase 10: Finalization & Release Readiness

| Task | Status | Notes |
|------|--------|-------|
| API versioning headers | ❌ | Core schema lock-in |
| Release packaging | ❌ | Makefile targets + GitHub release |
| Docs polish | ❌ | Archive reports, blueprints |
| Test suite coverage: 95% | ❌ | Stubbed + real endpoints |

---

## 📋 Live TODO Queue (Sorted by Urgency)

- [ ] Create mutation layer for playlist management
- [ ] Finalize admin API key lifecycle (revoke, audit, rotate)
- [ ] Sync task_checklist.md with new report policy
- [ ] Wire `next_steps_and_phases.md` to CI release candidate flow
- [ ] Prepare Phase 8 strategy doc

---

## 🧠 Notes

- `next_steps_and_phases.md` is the only file allowed to define global task state.
- Phase transitions are **not time-based** but milestone-based.
- All Jules task prompts **must update this file** upon completion.
- Link to any task artifacts (e.g. `/docs/projectplan/completions/`).

---
