# Lessons Learnt Log

**Purpose:**
Capture key takeaways from the <PROJECT_NAME> across all phases, with direct references to where the lesson was first applied or discussed.
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

## Phase 0 – Inception & Initial Scoping (Example)

| Lesson | Impact | Reference |
|--------|--------|-----------|
| Define project boundaries early to avoid scope confusion. | **High** – prevented weeks of wasted effort. | (doc: <link_to_scope_document>) |
| Start with a minimal viable architecture. | **Medium** – reduced technical debt early. | (doc: <link_to_hld>) |

---

## Phase 1 – Architecture & Design Foundations (Example)

| Lesson | Impact | Reference |
|--------|--------|-----------|
| Maintain a single source of truth for designs and keep it synced. | **High** – onboarding speed + reduced confusion. | (doc: <link_to_design_docs>) |
| Use strict phase sequencing to avoid scattered work. | **High** – prevented parallel half-finished tasks. | (doc: <link_to_execution_plan>) |

---

## Cross-Phase Lessons (Example)

| Lesson | Impact | Reference |
|--------|--------|-----------|
| Track phases and steps explicitly to prevent scope drift. | **High** | (doc: <link_to_execution_plan>) |
| Keep docs aligned continuously, not in large delayed batches. | **High** | (doc: <link_to_process_doc>) |
| Audit documents are worth the overhead for clean closure. | **Medium** | (doc: <link_to_audit_docs>) |
| Test critical mechanisms (e.g., queues, retries) thoroughly. | **High** | (code: <link_to_tests>) |
| Deliver iteratively, not as a single big launch. | **High** | (doc: <link_to_delivery_model_doc>) |
| Project state documents must be updated *during* the work session, not after, to prevent confusion. | **High** | (doc: <link_to_activity_log>) |

---
