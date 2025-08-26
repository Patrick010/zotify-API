# Action Plan: Phase 4 "Super-Lint" (Comprehensive)

**Status:** ✅ Superseded & Consolidated
**Note:** The goals and tasks outlined in this document have been implemented. The `HLD_LLD_ALIGNMENT_PLAN.md` and `PHASE_4_TRACEABILITY_MATRIX.md` are now the canonical sources of truth for the status of the Phase 4 work. This document is preserved for historical and contextual reference.

---

**Status:** Active
**Author:** Jules
**Date:** 2025-08-16

## 1. Purpose & Scope

This document provides a detailed, step-by-step action plan for implementing the
 "Super-Lint," a comprehensive code quality and security enforcement mechanism f
or the Zotify API project. This plan synthesizes the best elements of previous p
roposals to create a single, authoritative guide.

### 1.1. Scope
- **Codebases Covered:** The Super-Lint will apply to all Python code within the
 `api/` directory and all Go code within the `snitch/` directory.
- **Goals:**
    - Automate the enforcement of coding standards and style.
    - Proactively identify security vulnerabilities and insecure dependencies.
    - Automatically enforce "living documentation" policies.
    - Ensure a consistent and high level of code quality to improve long-term ma
intainability.

## 2. Tools & Standards

### 2.1. Chosen Tools
- **Python:**
    - **`ruff`:** For high-performance linting.
    - **`black`:** For automated code formatting.
    - **`mypy`:** For strict static type checking.
    - **`bandit`:** For security-focused static analysis.
    - **`safety`:** For scanning dependencies for known vulnerabilities.
- **Go:**
    - **`golangci-lint`:** An aggregator for many Go linters.
    - **`gosec`:** For security-focused static analysis.
- **General:**
    - **`pre-commit`:** A framework to manage and run git hooks for local enforc
ement.

### 2.2. Coding Standards
- **Python:** Adherence to PEP 8 (enforced by `ruff`). Strict typing enforced by
 `mypy`. The baseline strictness will be `--strict`, but gradual typing will be
tolerated during the initial remediation phase (`Phase 4a`), allowing for `# typ
e: ignore` comments where immediate fixes are not feasible.
- **Go:** Standard Go formatting (`gofmt`) and best practices enforced by `golan
gci-lint`.
- **Compliance Targets:** All new code must pass all Super-Lint checks to be mer
ged.

## 3. Phased Rollout Strategy

The Super-Lint will be rolled out in phases to manage the remediation of existin
g technical debt and to introduce checks progressively.

### Phase 4a: Prerequisite: Technical Debt Remediation
Before implementing new quality gates, the existing codebase must be brought to
a clean baseline.
- **TD-TASK-01:** Resolve `mypy` Blocker (e.g., conflicting module names).
- **TD-TASK-02:** Remediate Critical Security Vulnerabilities identified by an i
nitial `bandit` scan.
- **TD-TASK-03:** Establish baseline configurations for all tools (`ruff.toml`,
`mypy.ini`, `.golangci.yml`).

### Phase 4b: Foundational Static Analysis
- **Goal:** Automatically enforce baseline code quality, style, and security.
- **Tasks:**
    - **SL-TASK-01:** Integrate `ruff`, `mypy`, `bandit`, `safety`, and `golangc
i-lint` into the CI pipeline in "advisory mode" (reports errors but does not blo
ck merges).
    - **SL-TASK-02:** After a review period, switch the CI pipeline to "enforcem
ent mode," blocking merges on any failure.

### Phase 4c: Custom Architectural & Documentation Linting
- **Goal:** Automatically enforce the project's "living documentation" philosoph
y.
- **Tasks:**
    - **SL-TASK-03:** Develop a custom linting script for the CI pipeline to:
        1. Verify new API routes are documented.
        2. Verify significant new logic is linked to a feature specification.
        3. Check for the presence of docstrings on all public functions/classes.
        4. Flag PRs that modify core logic but do not update `TRACEABILITY_MATRI
X.md`.
      This check will also begin in "advisory mode" before being moved to enforc
ement.
    - **Note on Flexibility:** The script will include a simple override mechani
sm (e.g., a specific tag like `[DOC-LINT-IGNORE]` in the PR description) for cas
es where a PR legitimately does not require documentation changes, preventing de
velopers from being blocked by false positives.

### Phase 4d: Deep Code Review Process & Local Enforcement
- **Goal:** Formalize the human review process and provide immediate local feedb
ack.
- **Tasks:**
    - **SL-TASK-04:** Update `TASK_CHECKLIST.md` with a formal code review check
list based on the Super-Lint requirements (Maintainability, Performance, etc.) a
nd a code scoring rubric.
    - **SL-TASK-05:** Implement `pre-commit` hooks to run `ruff` and `golangci-l
int` locally, providing instant feedback to developers before code is even commi
tted.

## 4. Exemption Process

In rare cases where a rule must be violated, the following process is required:
1.  The line of code must be marked with a specific `# noqa: [RULE-ID]` comment.
2.  A justification for the exemption must be added to the code comment and the
Pull Request description.
3.  The exemption must be explicitly approved by a senior developer during code
review.

## 5. Traceability
- This plan is the primary deliverable for the "Define the Detailed Action Plan
for Phase 4 'Super-Lint'" task.
- Implementation will be tracked via `TD-TASK-*` and `SL-TASK-*` entries in `BAC
KLOG.md`.
- Overall progress will be reflected in `ROADMAP.md`.
