# Project Backlog

**Status:** Live Document

## 1. Purpose

This document serves as the tactical backlog for the Zotify API project. It contains a list of clearly defined tasks that have been approved for implementation but are not yet assigned to a specific sprint or work cycle.

The process for managing this backlog is defined in the `PID.md` and is designed to ensure that every task is traceable, fully defined, and qualified for execution.

---

## 2. Backlog Management Flow

The following diagram illustrates the process of generating, qualifying, and executing tasks from the backlog.

```text
Live Docs (TRACEABILITY_MATRIX.md, USECASES.md, GAP_ANALYSIS_USECASES.md, FUTURE_ENHANCEMENTS.md)
         │
         ▼
  Backlog Task Generation
         │
         ▼
  Backlog Template (This File)
         │
         ▼
 Task Qualification & Review Gate
         │
         ├─> Ready → Execution
         │
         └─> Not Ready → Returned / Revised
         │
         ▼
 Periodic Audit & Enforcement Scripts
```

---

## 3. Backlog Task Template

All new tasks added to this backlog **must** use the following template.

```markdown
---
- **Task ID:** `[TASK-ID]`
- **Source:** `[Link to source document, e.g., TRACEABILITY_MATRIX.md#REQ-001]`
- **Priority:** `[HIGH | MEDIUM | LOW]`
- **Dependencies:** `[List of other Task IDs or external conditions]`
- **Description:** `[Clear and concise description of the task and its goal.]`
- **Acceptance Criteria:**
  - `[ ] A specific, measurable, and verifiable condition for completion.`
  - `[ ] Another specific condition.`
- **Estimated Effort:** `[e.g., Small, Medium, Large, or Story Points]`
---
```

---

## 4. Backlog Items

### High Priority

- **Task ID:** `REM-TASK-01`
- **Source:** `project/audit/AUDIT-PHASE-4.md#AUDIT-4a`
- **Priority:** `HIGH`
- **Dependencies:** `None`
- **Description:** `Remediate documentation and environment based on findings from Audit Phase 4a to establish a reliable project baseline.`
- **Acceptance Criteria:**
  - `[ ]` `ACTIVITY.md` is corrected.
  - `[ ]` `.gitignore` is updated with storage and database paths.
  - `[ ]` `INSTALLATION.md` is updated with complete, working setup instructions.
- **Estimated Effort:** `Medium`

- **Task ID:** `LOG-TASK-01`
- **Source:** `project/audit/AUDIT-PHASE-4.md#AUDIT-4a`
- **Priority:** `HIGH`
- **Dependencies:** `REM-TASK-01`
- **Description:** `Implement the extendable logging system as defined in LOGGING_SYSTEM_DESIGN.md. This replaces the non-compliant placeholder and fulfills the original design.`
- **Acceptance Criteria:**
  - `[ ]` Placeholder logging service, routes, and tests are removed.
  - `[ ]` New `LoggingService` and handlers are implemented in `api/src/zotify_api/core/`.
  - `[ ]` New system is fully tested and integrated.
  - `[ ]` All relevant documentation is updated to reflect the new architecture.
- **Estimated Effort:** `Large`

- **Task ID:** `TD-TASK-01`
- **Source:** `project/audit/CODE_OPTIMIZATIONPLAN_PHASE_4.md#phase-4a`
- **Priority:** `[HIGH]`
- **Dependencies:** `None`
- **Description:** `Resolve mypy Blocker (e.g., conflicting module names) to enable static type checking.`
- **Acceptance Criteria:**
  - `[ ]` `mypy` runs successfully without configuration errors.
- **Estimated Effort:** `Small`

- **Task ID:** `TD-TASK-02`
- **Source:** `project/audit/CODE_OPTIMIZATIONPLAN_PHASE_4.md#phase-4a`
- **Priority:** `[HIGH]`
- **Dependencies:** `None`
- **Description:** `Remediate critical security vulnerabilities identified by initial bandit scan.`
- **Acceptance Criteria:**
  - `[ ]` High-priority `bandit` findings are resolved.
- **Estimated Effort:** `Medium`

- **Task ID:** `TD-TASK-03`
- **Source:** `project/audit/CODE_OPTIMIZATIONPLAN_PHASE_4.md#phase-4a`
- **Priority:** `[HIGH]`
- **Dependencies:** `None`
- **Description:** `Establish baseline configurations for all linting and security tools.`
- **Acceptance Criteria:**
  - `[ ]` Configuration files for `ruff`, `mypy`, `bandit`, `safety`, and `golangci-lint` are created and checked in.
- **Estimated Effort:** `Medium`

- **Task ID:** `SL-TASK-01`
- **Source:** `project/audit/CODE_OPTIMIZATIONPLAN_PHASE_4.md#phase-4b`
- **Priority:** `[HIGH]`
- **Dependencies:** `TD-TASK-01, TD-TASK-02, TD-TASK-03`
- **Description:** `Integrate all Super-Lint checks into the CI/CD pipeline in "advisory mode".`
- **Acceptance Criteria:**
  - `[ ]` A new GitHub Actions workflow runs all linting and security checks on pull requests.
  - `[ ]` The workflow is configured to report errors but not block merges.
- **Estimated Effort:** `Medium`

- **Task ID:** `SL-TASK-02`
- **Source:** `project/audit/CODE_OPTIMIZATIONPLAN_PHASE_4.md#phase-4b`
- **Priority:** `[HIGH]`
- **Dependencies:** `SL-TASK-01`
- **Description:** `Switch the Super-Lint CI/CD pipeline to "enforcement mode".`
- **Acceptance Criteria:**
  - `[ ]` The CI workflow is updated to fail the build and block merges if any Super-Lint checks fail.
- **Estimated Effort:** `Small`

### Medium Priority

- **Task ID:** `SL-TASK-03`
- **Source:** `project/audit/CODE_OPTIMIZATIONPLAN_PHASE_4.md#phase-4c`
- **Priority:** `[MEDIUM]`
- **Dependencies:** `SL-TASK-01`
- **Description:** `Develop a custom linting script for documentation and architectural checks.`
- **Acceptance Criteria:**
  - `[ ]` Script is created and integrated into the CI pipeline.
  - `[ ]` Script checks for docstrings and `TRACEABILITY_MATRIX.md` updates.
- **Estimated Effort:** `Large`

- **Task ID:** `SL-TASK-04`
- **Source:** `project/audit/CODE_OPTIMIZATIONPLAN_PHASE_4.md#phase-4d`
- **Priority:** `[MEDIUM]`
- **Dependencies:** `None`
- **Description:** `Update TASK_CHECKLIST.md with a formal code review checklist and scoring rubric.`
- **Acceptance Criteria:**
  - `[ ]` `TASK_CHECKLIST.md` is updated with the new section.
- **Estimated Effort:** `Small`

- **Task ID:** `SL-TASK-05`
- **Source:** `project/audit/CODE_OPTIMIZATIONPLAN_PHASE_4.md#phase-4d`
- **Priority:** `[MEDIUM]`
- **Dependencies:** `TD-TASK-03`
- **Description:** `Implement local enforcement of linting rules using pre-commit hooks.`
- **Acceptance Criteria:**
  - `[ ]` A `.pre-commit-config.yaml` is created and configured.
  - `[ ]` Developer documentation is updated with setup instructions.
- **Estimated Effort:** `Medium`

### Low Priority

*(No low priority tasks currently in the backlog.)*
