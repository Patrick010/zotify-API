# QA & Governance Policy

**Status:** Live Document
**Owner:** Project Lead

## 1. Overview
This document is the single source of truth for all Quality Assurance (QA) and governance policies for this project. All contributors are required to understand and adhere to these rules. The policies outlined here are enforced automatically by the project's tooling wherever possible.

## 2. Core Policy: Root Cause & Design Alignment
The cornerstone of our QA process is the strict alignment between code, design, and documentation.

> ⚠️ **Root Cause & Design Alignment Policy:**
> Any code change must be traced back to its design section (HLD/LLD) and reflected in `ALIGNMENT_MATRIX.md`.
> No “coding away” issues without documenting root cause and alignment.

This policy is enforced automatically by the project's linter.

## 3. Linter Enforcement
The primary mechanism for enforcing these policies is the unified linter script, located at `scripts/linter.py`.

### 3.1. Traceability Enforcement
- **Trigger:** Any change to source code files within the `api/src/`, `snitch/`, `gonk-testUI/`, or `scripts/` directories.
- **Rule:** When a change is detected in a source code file, a corresponding update to the `project/ALIGNMENT_MATRIX.md` is **mandatory**.
- **Enforcement:** The linter will fail if source code is modified without a corresponding change to the alignment matrix. This check is performed in every `pre-commit` hook and in the CI/CD pipeline.

### 3.2. Documentation Linkage Enforcement
- **Trigger:** Any change to source code that has a defined documentation dependency.
- **Rule:** The relationships between source code and their required documentation are defined in `scripts/doc-lint-rules.yml`. If a source file with a defined rule is changed, its corresponding documentation must also be changed.
- **Enforcement:** The linter will fail if the documentation is not updated alongside the code.

### 3.3. Linter Execution Scope
- **Scope:** The linter is designed to run **incrementally** on changed files as detected by `git diff`.
- **Rationale:** This ensures that checks are fast, relevant, and focused on the work being done.
- **Removed `--run-all` Flag:** A previous `--run-all` flag was removed from the linter. It was found to be incompatible with the incremental nature of the checks and introduced bugs related to the project's "living documentation" policies. All checks are now exclusively run on the set of files included in a commit or pull request.

### 3.4. Forbidden Document Enforcement
- **Trigger:** Any change to a file listed in the `forbidden_docs` section of a rule in `scripts/doc-lint-rules.yml`.
- **Rule:** These files are considered locked and must not be modified.
- **Enforcement:** The linter will fail if a change is detected in a forbidden document.
- **Note on Unreliable Environments:** In some CI/test environments, the `git diff` command used by the linter may be unreliable. In such cases, the `forbidden_docs` check may require manual verification during code review.

### 3.5. Code Quality Scorecard Enforcement
- **Trigger:** Any change to the `api/docs/CODE_QUALITY_INDEX.md` file.
- **Rule:** The scores in the index **must** align with the A-F scale defined in the `API_DEVELOPER_GUIDE.md`.
- **Enforcement:** The linter will parse the `CODE_QUALITY_INDEX.md` file on every change and validate that all `Doc Score` and `Code Score` values are one of `A, B, C, D, F`. Commits containing invalid scores will be rejected.

## 4. CI/CD & Pull Request (PR) Enforcement
- All policies are enforced at the PR level by the `ci.yml` GitHub Actions workflow.
- The workflow runs the unified linter (`python scripts/linter.py`) on all changes.
- A PR cannot be merged if the linter script fails. This ensures that no code that violates project governance can be merged into the `main` branch.

## 5. Key Governance Documents
- **This Document:** `project/QA_GOVERNANCE.md`
- **The Live Traceability Matrix:** `project/ALIGNMENT_MATRIX.md`
- **The Linter Ruleset:** `scripts/doc-lint-rules.yml`
