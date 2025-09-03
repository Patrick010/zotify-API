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

## 4. CI/CD & Pull Request (PR) Enforcement
- All policies are enforced at the PR level by the `ci.yml` GitHub Actions workflow.
- The workflow runs the unified linter (`python scripts/linter.py`) on all changes.
- A PR cannot be merged if the linter script fails. This ensures that no code that violates project governance can be merged into the `main` branch.

## 5. Key Governance Documents
- **This Document:** `project/QA_GOVERNANCE.md`
- **The Live Traceability Matrix:** `project/ALIGNMENT_MATRIX.md`
- **The Linter Ruleset:** `scripts/doc-lint-rules.yml`
