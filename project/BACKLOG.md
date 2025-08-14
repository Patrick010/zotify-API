# Project Backlog

**Status:** Live Document

## 1. Purpose

This document serves as the tactical backlog for the Zotify API project. It contains a list of clearly defined tasks that have been approved for implementation but are not yet assigned to a specific sprint or work cycle. This provides a work supply for future phases and ensures that good ideas are not lost.

Tasks in this backlog are distinct from the strategic, high-level goals outlined in `FUTURE_ENHANCEMENTS.md`.

## 2. Backlog Items

Items are to be flagged with a priority (`[HIGH]`, `[MEDIUM]`, `[LOW]`) and a status marker to aid in work planning.

---

### `P4-TASK-01` [HIGH]: Update Task Execution Checklist with Documentation Mandate
- **Status:** ❌ Not Started
- **Description:** This task involves adding a mandatory step to the project's `task_checklist.md`. This step will require developers to confirm they have updated all relevant project documentation as part of their pull request, making documentation updates an explicit part of the development workflow.
- **Source:** `project/audit/HLD_LLD_ALIGNMENT_PLAN.md` (Phase 4, Task 4.1)

---

### `P4-TASK-02` [MEDIUM]: Implement CI Check for Documentation Updates
- **Status:** ❌ Not Started
- **Description:** This task is to create an automated check within the CI/CD pipeline to enforce the documentation update mandate. This will serve as an automated safeguard to prevent code changes from being merged without corresponding documentation updates.
- **Source:** `project/audit/HLD_LLD_ALIGNMENT_PLAN.md` (Phase 4, Task 4.2)

---

### `P4-TASK-03` [LOW]: Formalize and Schedule Documentation Review Process
- **Status:** ❌ Not Started
- **Description:** This task involves defining and documenting a formal process for periodic reviews of the project's design documents. This process will specify the cadence, scope, and responsibilities for the reviews to proactively maintain documentation quality.
- **Source:** `project/audit/HLD_LLD_ALIGNMENT_PLAN.md` (Phase 4, Task 4.3)

---
### `TD-TASK-01` [CRITICAL]: Resolve MyPy Blocker
- **Status:** ❌ Not Started
- **Description:** The `mypy` type checker currently fails to run due to a duplicate module name conflict between `api/src/zotify_api/routes/config.py` and `api/src/zotify_api/models/config.py`. This task is to rename one of the files (e.g., to `config_routes.py`) to resolve the conflict and allow the type checker to run across the codebase. This is a blocker for all future type safety work.
- **Source:** `project/audit/CODE_OPTIMIZATIONPLAN_PHASE_4.md`

---

### `TD-TASK-02` [HIGH]: Remediate Critical Security Vulnerabilities
- **Status:** ❌ Not Started
- **Description:** Address the high-priority security issues identified by `bandit`. This includes removing the `debug=True` flag from the `gonk-testUI` server startup and refactoring the database query in `tracks_service.py` to use parameterized queries instead of string formatting to prevent SQL injection risks.
- **Source:** `project/audit/CODE_OPTIMIZATIONPLAN_PHASE_4.md`

---

### `TD-TASK-03` [MEDIUM]: One-Time Code Formatting
- **Status:** ❌ Not Started
- **Description:** Perform a one-time, automated pass across the entire repository with `black` and `isort` to fix all existing code formatting and import order issues. This will establish a clean, consistent baseline before automated checks are enforced in CI.
- **Source:** `project/audit/CODE_OPTIMIZATIONPLAN_PHASE_4.md`

---

### `SL-TASK-01` [HIGH]: Integrate Formatting Checks into CI
- **Status:** ❌ Not Started
- **Description:** Integrate `black`, `isort`, and `flake8` into the CI pipeline. The build must fail if any of these checks do not pass. This corresponds to Stage 1 of the Super-Lint plan.
- **Source:** `project/audit/CODE_OPTIMIZATIONPLAN_PHASE_4.md`

---

### `SL-TASK-02` [HIGH]: Integrate Type and Security Checks into CI
- **Status:** ❌ Not Started
- **Description:** Integrate `mypy` and `bandit` into the CI pipeline. The build must fail on any type errors or high/medium severity security issues. This corresponds to Stage 1 of the Super-Lint plan and depends on `TD-TASK-01`.
- **Source:** `project/audit/CODE_OPTIMIZATIONPLAN_PHASE_4.md`

---

### `SL-TASK-03` [MEDIUM]: Develop Custom Architectural Linting Script
- **Status:** ❌ Not Started
- **Description:** Develop the custom Python script for CI as outlined in Stage 2 of the Super-Lint plan. The script will enforce documentation linkages for endpoints, feature specs, and the traceability matrix, and check for basic docstring coverage.
- **Source:** `project/audit/CODE_OPTIMIZATIONPLAN_PHASE_4.md`

---

### `SL-TASK-04` [LOW]: Update Task Checklist
- **Status:** ❌ Not Started
- **Description:** Update the project's `task_checklist.md` (or create a `CONTRIBUTING.md`) with a formal code review checklist for reviewers, as outlined in Stage 3 of the Super-Lint plan. This fulfills the original goal of `P4-TASK-01`.
- **Source:** `project/audit/CODE_OPTIMIZATIONPLAN_PHASE_4.md`

---

### `SL-TASK-05` [LOW]: Document Code Scoring Rubric
- **Status:** ❌ Not Started
- **Description:** Document the 0-10 code scoring rubric and the process for scheduled documentation reviews, as outlined in Stage 3 of the Super-Lint plan. This fulfills the original goal of `P4-TASK-03`.
- **Source:** `project/audit/CODE_OPTIMIZATIONPLAN_PHASE_4.md`
