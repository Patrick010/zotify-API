# Action Plan: Phase 4 "Super-Lint" (Comprehensive)

**Status:** Proposed
**Author:** Jules
**Date:** 2025-08-16

## 1. Purpose & Scope

This document provides a detailed, step-by-step action plan for implementing the "Super-Lint," a comprehensive code quality and security enforcement mechanism for the Zotify API project. This plan synthesizes the best elements of previous proposals to create a single, authoritative guide.

### 1.1. Scope
- **Codebases Covered:** The Super-Lint will apply to all Python code within the `api/` directory and all Go code within the `snitch/` directory.
- **Goals:**
    - Automate the enforcement of coding standards and style.
    - Proactively identify security vulnerabilities and insecure dependencies.
    - Automatically enforce "living documentation" policies.
    - Ensure a consistent and high level of code quality to improve long-term maintainability.

## 2. Tools & Standards

### 2.1. Chosen Tools
- **Python:**
    - **`ruff`:** For high-performance linting and formatting.
    - **`mypy`:** For strict static type checking.
    - **`bandit`:** For security-focused static analysis.
    - **`safety`:** For scanning dependencies for known vulnerabilities.
- **Go:**
    - **`golangci-lint`:** An aggregator for many Go linters.
    - **`gosec`:** For security-focused static analysis.
- **General:**
    - **`pre-commit`:** A framework to manage and run git hooks for local enforcement.

### 2.2. Coding Standards
- **Python:** Adherence to PEP 8 (enforced by `ruff`). Strict typing enforced by `mypy`.
- **Go:** Standard Go formatting (`gofmt`) and best practices enforced by `golangci-lint`.
- **Compliance Targets:** All new code must pass all Super-Lint checks to be merged.

## 3. Phased Rollout Strategy

The Super-Lint will be rolled out in phases to manage the remediation of existing technical debt and to introduce checks progressively.

### Phase 4a: Prerequisite: Technical Debt Remediation
Before implementing new quality gates, the existing codebase must be brought to a clean baseline.
- **TD-TASK-01:** Resolve `mypy` Blocker (e.g., conflicting module names).
- **TD-TASK-02:** Remediate Critical Security Vulnerabilities identified by an initial `bandit` scan.
- **TD-TASK-03:** Establish baseline configurations for all tools (`ruff.toml`, `mypy.ini`, `.golangci.yml`).

### Phase 4b: Foundational Static Analysis
- **Goal:** Automatically enforce baseline code quality, style, and security.
- **Tasks:**
    - **SL-TASK-01:** Integrate `ruff`, `mypy`, `bandit`, and `golangci-lint` into the CI pipeline in "advisory mode" (reports errors but does not block merges).
    - **SL-TASK-02:** After a review period, switch the CI pipeline to "enforcement mode," blocking merges on any failure.

### Phase 4c: Custom Architectural & Documentation Linting
- **Goal:** Automatically enforce the project's "living documentation" philosophy.
- **Tasks:**
    - **SL-TASK-03:** Develop a custom linting script for the CI pipeline to:
        1. Verify new API routes are documented.
        2. Verify significant new logic is linked to a feature specification.
        3. Check for the presence of docstrings on all public functions/classes.
        4. Flag PRs that modify core logic but do not update `TRACEABILITY_MATRIX.md`.

### Phase 4d: Deep Code Review Process & Local Enforcement
- **Goal:** Formalize the human review process and provide immediate local feedback.
- **Tasks:**
    - **SL-TASK-04:** Update `TASK_CHECKLIST.md` with a formal code review checklist based on the Super-Lint requirements (Maintainability, Performance, etc.) and a code scoring rubric.
    - **SL-TASK-05:** Implement `pre-commit` hooks to run `ruff` and `golangci-lint` locally, providing instant feedback to developers before code is even committed.

## 4. Exemption Process

In rare cases where a rule must be violated, the following process is required:
1.  The line of code must be marked with a specific `# noqa: [RULE-ID]` comment.
2.  A justification for the exemption must be added to the code comment and the Pull Request description.
3.  The exemption must be explicitly approved by a senior developer during code review.

## 5. Traceability
- This plan is the primary deliverable for the "Define the Detailed Action Plan for Phase 4 'Super-Lint'" task.
- Implementation will be tracked via `TD-TASK-*` and `SL-TASK-*` entries in `BACKLOG.md`.
- Overall progress will be reflected in `ROADMAP.md`.
