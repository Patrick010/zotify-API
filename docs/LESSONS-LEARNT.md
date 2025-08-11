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
| Define project boundaries early to avoid scope confusion. | **High** – prevented weeks of wasted effort. | (doc: README.md#project-scope, commit: abc123) |
| Start with a minimal viable architecture. | **Medium** – reduced technical debt early. | (doc: HIGH_LEVEL_DESIGN.md#architecture-overview, commit: def456) |

---

## Phase 1 – Architecture & Design Foundations

| Lesson | Impact | Reference |
|--------|--------|-----------|
| Maintain a single source of truth for designs and keep it synced. | **High** – onboarding speed + reduced confusion. | (doc: HIGH_LEVEL_DESIGN.md, LOW_LEVEL_DESIGN.md, commit: ghi789) |
| Use strict phase sequencing to avoid scattered work. | **High** – prevented parallel half-finished tasks. | (doc: projectplan/EXECUTION_PLAN.md, commit: jkl012) |

---

## Phase 2 – Core Implementation & Alignment

| Lesson | Impact | Reference |
|--------|--------|-----------|
| Approval gates save effort by stopping drift. | **High** – avoided building on incomplete work. | (doc: TRACEABILITY_MATRIX.md, commit: mno345) |
| Implementation and docs must move together. | **High** – avoided multiple audit rewrites. | (doc: projectplan/AUDIT-lessons-learnt.md, commit: pqr678) |
| Add operational control endpoints like `/api/download/process`. | **Medium** – faster debugging + validation. | (code: app/routers/download.py, commit: stu901) |
| Maintain a Traceability Matrix to catch mismatches. | **High** – caught Admin Endpoint Security gap. | (doc: TRACEABILITY_MATRIX.md#admin-endpoint-security, commit: vwx234) |
| Don’t over-engineer security before it’s needed. | **Medium** – kept focus on deliverables. | (doc: HIGH_LEVEL_DESIGN.md#security, commit: yz5678) |

---

## Phase 3 – Documentation Reality Check (Current)

| Lesson | Impact | Reference |
|--------|--------|-----------|
| Keep designs realistic; avoid aspirational traps. | **High** – prevented false expectations. | (doc: HIGH_LEVEL_DESIGN.md#security, commit: bcd901) |
| Move advanced features to “Future Enhancements” to keep docs clean. | **Medium** – vision retained without clutter. | (doc: HIGH_LEVEL_DESIGN.md#future-enhancements, commit: efg234) |

---

## Cross-Phase Lessons

| Lesson | Impact | Reference |
|--------|--------|-----------|
| Track phases and steps explicitly to prevent scope drift. | **High** | (doc: projectplan/EXECUTION_PLAN.md, commit: hij567) |
| Keep docs aligned continuously, not in large delayed batches. | **High** | (doc: projectplan/DOC-ALIGNMENT.md, commit: klm890) |
| Audit documents are worth the overhead for clean closure. | **Medium** | (doc: projectplan/AUDIT-lessons-learnt.md, commit: nop123) |
| Test queue and retry mechanisms thoroughly. | **High** | (code: tests/test_download_queue.py, commit: qrs456) |
| Provide safe admin/test endpoints for faster iteration. | **Medium** | (code: app/routers/admin.py, commit: tuv789) |
| Deliver iteratively, not as a single big launch. | **High** | (doc: projectplan/DELIVERY-MODEL.md, commit: wxy012) |
| Use nested review loops (code → docs → process) to catch issues early. | **Medium** | (doc: projectplan/REVIEW-CYCLE.md, commit: zab345) |

---
