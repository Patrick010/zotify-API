# Action Plan: Phase 4 "Super-Lint"

**Status:** Proposed
**Author:** Jules
**Date:** 2025-08-16

## 1. Purpose & Scope

This document provides a detailed, step-by-step action plan for implementing the "Super-Lint," a comprehensive code quality and security enforcement mechanism for the Zotify API project.

### 1.1. Scope
- **Codebases Covered:** The Super-Lint will apply to all Python code within the `api/` directory and all Go code within the `snitch/` directory.
- **Goals:**
    - Automate the enforcement of coding standards and style.
    - Proactively identify security vulnerabilities (e.g., hardcoded secrets, unsafe calls).
    - Scan for insecure dependencies.
    - Ensure a consistent and high level of code quality to improve long-term maintainability.

## 2. Tools & Standards

### 2.1. Chosen Tools
- **Python:**
    - **`ruff`:** For high-performance linting and formatting. It will replace any existing linters like `pylint` or `flake8`.
    - **`mypy`:** For strict static type checking.
    - **`bandit`:** For security-focused static analysis.
    - **`safety`:** For scanning dependencies for known vulnerabilities.
- **Go:**
    - **`golangci-lint`:** An aggregator for many Go linters, providing comprehensive checks.
    - **`gosec`:** For security-focused static analysis.
- **General:**
    - **`pre-commit`:** A framework to manage and run git hooks, ensuring checks are performed before code is committed.

### 2.2. Coding Standards
- **Python:** Adherence to PEP 8, with formatting enforced by `ruff`. Strict typing will be enforced by `mypy`.
- **Go:** Standard Go formatting (`gofmt`) and best practices as enforced by `golangci-lint`.
- **Compliance Targets:** All new code must pass all Super-Lint checks to be merged. Existing code will be brought into compliance incrementally.

## 3. Phased Rollout Strategy

The Super-Lint will be rolled out in phases to manage the remediation of existing technical debt without blocking new development.

### Phase 4a: Foundational Setup (Current)
1.  **Remediate Existing Blockers:**
    - Fix all existing `mypy` errors that are currently preventing strict enforcement.
    - Address any critical vulnerabilities identified by an initial `bandit` and `safety` scan.
2.  **Establish Baseline Configuration:**
    - Create configuration files for all tools (`ruff.toml`, `mypy.ini`, `.golangci.yml`).
    - Configure the tools with the project's chosen rule sets.

### Phase 4b: CI Integration (Advisory Mode)
1.  **Integrate into CI:** Add a new step to the GitHub Actions workflow that runs all Super-Lint checks on every pull request.
2.  **Run in Advisory Mode:** Initially, the CI check will be configured to be non-blocking. It will report errors and vulnerabilities but will not fail the build or block merges. This allows developers to see the results and begin fixing issues without halting work.

### Phase 4c: CI Integration (Enforcement Mode)
1.  **Activate Blocking:** Once the majority of existing issues have been resolved, the CI check will be switched to "enforcement mode."
2.  **Block Merges:** Pull requests with any Super-Lint failures will be blocked from being merged until the issues are fixed.

### Phase 4d: Local Enforcement (Pre-commit Hooks)
1.  **Implement `pre-commit`:** A `.pre-commit-config.yaml` file will be added to the repository.
2.  **Configure Hooks:** The config will be set up to run `ruff`, `mypy`, and `golangci-lint` automatically when a developer runs `git commit`. This provides immediate feedback and prevents non-compliant code from even entering the remote repository.

## 4. Exemption Process

In rare cases where a rule must be violated (e.g., to support a legacy system), an exemption process will be followed:
1.  The line of code must be marked with a specific `# noqa: [RULE-ID]` comment.
2.  A justification for the exemption must be added to the code comment.
3.  The exemption must be explicitly approved during the code review process.

## 5. Traceability
- This plan is the primary deliverable for the "Define the Detailed Action Plan for Phase 4 'Super-Lint'" task, which originates from the "Phase 4: Enforce & Automate" goal in the [`HLD_LLD_ALIGNMENT_PLAN.md`](./audit/HLD_LLD_ALIGNMENT_PLAN.md).
- The implementation of this plan will be tracked via `LINT-TASK-*` entries in the [`BACKLOG.md`](./BACKLOG.md).
- The overall progress of Phase 4 will be reflected in the [`ROADMAP.md`](./ROADMAP.md).
