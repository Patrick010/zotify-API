# Lessons Learnt Log

**Purpose:**
Capture key takeaways from the Zotify API project across all phases, with direct references to where the lesson was first applied or discussed.
**Scope:**
Covers insights from initial planning (Phase 0) through current active development.

---

## Project Flow Requirement

- This file **must be updated** immediately after any lesson with project-wide or phase-relevant implications is identified.
- Updating this file is a **hard requirement** for phase closure.
- No phase is considered “complete” until:
  1. This file is reviewed and updated.
  2. All relevant entries are linked to code commits or documentation.
- Reviewers must confirm updates during **phase review gates**.

---

## Phase 0 – Inception & Initial Scoping

| Lesson | Impact | Reference |
|--------|--------|-----------|
| Define project boundaries early to avoid scope confusion. | **High** – prevented weeks of wasted effort. | (doc: README.md#project-scope) |
| Start with a minimal viable architecture. | **Medium** – reduced technical debt early. | (doc: HIGH_LEVEL_DESIGN.md#architecture-overview) |

---

## Phase 1 – Architecture & Design Foundations

| Lesson | Impact | Reference |
|--------|--------|-----------|
| Maintain a single source of truth for designs and keep it synced. | **High** – onboarding speed + reduced confusion. | (doc: HIGH_LEVEL_DESIGN.md, LOW_LEVEL_DESIGN.md) |
| Use strict phase sequencing to avoid scattered work. | **High** – prevented parallel half-finished tasks. | (doc: projectplan/EXECUTION_PLAN.md) |

---

## Phase 2 – Core Implementation & Alignment

| Lesson | Impact | Reference |
|--------|--------|-----------|
| Approval gates save effort by stopping drift. | **High** – avoided building on incomplete work. | (doc: AUDIT_TRACEABILITY_MATRIX.md) |
| Implementation and docs must move together. | **High** – avoided multiple audit rewrites. | (doc: projectplan/AUDIT-lessons-learnt.md) |
| Add operational control endpoints like `/api/download/process`. | **Medium** – faster debugging + validation. | (code: app/routers/download.py) |
| Maintain a Traceability Matrix to catch mismatches. | **High** – caught Admin Endpoint Security gap. | (doc: AUDIT_TRACEABILITY_MATRIX.md#admin-endpoint-security) |
| Don’t over-engineer security before it’s needed. | **Medium** – kept focus on deliverables. | (doc: HIGH_LEVEL_DESIGN.md#security) |

---

## Phase 3 – Documentation Reality Check (Current)

| Lesson | Impact | Reference |
|--------|--------|-----------|
| Keep designs realistic; avoid aspirational traps. | **High** – prevented false expectations. | (doc: HIGH_LEVEL_DESIGN.md#security) |
| Move advanced features to “Future Enhancements” to keep docs clean. | **Medium** – vision retained without clutter. | (doc: HIGH_LEVEL_DESIGN.md#future-enhancements) |
| A single, authoritative source for project status and next-steps is critical. | **High** – Discrepancies between `CURRENT_STATE.md`, `ACTIVITY.md`, and audit plans caused confusion and required significant clarification cycles to resolve. | (doc: CURRENT_STATE.md, ACTIVITY.md, audit/AUDIT-PHASE-3.md) |

---

## Phase 4 – Automation & Quality Gates

| Lesson | Impact | Reference |
|--------|--------|-----------|
| **A "single source of truth" for planning is non-negotiable.** | **Critical** – The existence of two parallel planning documents (`HLD_LLD_ALIGNMENT_PLAN.md` and `CODE_OPTIMIZATIONPLAN_PHASE_4.md`) caused significant confusion, rework, and required direct user intervention to resolve. Future phases must ensure a single, canonical plan is maintained. | (doc: project/audit/AUDIT_END_REPORT_PHASE_4.md) |
| **Automated enforcement is vastly superior to procedural enforcement.** | **High** – The most effective improvements in this phase were converting procedural hopes into automated realities. The "Trinity Rule" added to the doc linter, which programmatically enforces the update of log files, is a prime example of a successful conversion that prevents process decay. | (doc: scripts/lint-docs.py) |
| **The agent's execution environment can be unreliable.** | **Critical** – The agent's local `git` environment was consistently out of sync with the remote repository's true state. This led to incorrect assumptions about commit failures and significant wasted effort. Future work must not blindly trust the local `git` state and should rely on direct evidence (e.g., user feedback, file content verification) as the source of truth. | (doc: project/audit/AUDIT_END_REPORT_PHASE_4.md) |

---

## Cross-Phase Lessons

| Lesson | Impact | Reference |
|--------|--------|-----------|
| Track phases and steps explicitly to prevent scope drift. | **High** | (doc: projectplan/EXECUTION_PLAN.md) |
| Keep docs aligned continuously, not in large delayed batches. | **High** | (doc: projectplan/DOC-ALIGNMENT.md) |
| Audit documents are worth the overhead for clean closure. | **Medium** | (doc: projectplan/AUDIT-lessons-learnt.md) |
| Test queue and retry mechanisms thoroughly. | **High** | (code: tests/test_download_queue.py) |
| Provide safe admin/test endpoints for faster iteration. | **Medium** | (code: app/routers/admin.py) |
| Deliver iteratively, not as a single big launch. | **High** | (doc: projectplan/DELIVERY-MODEL.md) |
| Use nested review loops (code → docs → process) to catch issues early. | **Medium** | (doc: projectplan/REVIEW-CYCLE.md) |
| Providing sensible defaults (e.g., for `DATABASE_URI`) significantly improves the developer onboarding experience and reduces setup friction. | **Medium** | (doc: api/docs/manuals/SYSTEM_INTEGRATION_GUIDE.md, api/src/zotify_api/config.py) |
| Enforce unique filenames and directory names across the entire repository to prevent ambiguity and simplify searches. | **High** | (doc: project/LESSONS-LEARNT.md) |
| A hanging command can destabilize the entire execution environment. Long-running processes like test suites must be wrapped in a timeout to prevent them from blocking all other operations. | **Critical** | (doc: project/CURRENT_STATE.md) |
| Project state documents (`ACTIVITY.md`, `CURRENT_STATE.md`) must be updated *during* the work session, not after. Failure to do so leads to confusion, incorrect assumptions, and wasted effort. | **High** | (doc: project/ACTIVITY.md, project/CURRENT_STATE.md) |

---
