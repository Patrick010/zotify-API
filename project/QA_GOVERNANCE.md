<!-- ID: DOC-018 -->
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
- **Trigger:** Any change to source code files within the `api/src/`, `snitch/`, `Gonk/GonkUI/`, or `scripts/` directories.
- **Rule:** When a change is detected in a source code file, a corresponding update to the `project/ALIGNMENT_MATRIX.md` is **mandatory**.
- **Enforcement:** The linter will fail if source code is modified without a corresponding change to the alignment matrix. This check is performed in every `pre-commit` hook and in the CI/CD pipeline.

### 3.2. Documentation Linkage Enforcement
- **Trigger:** Any change to source code that has a defined documentation dependency.
- **Rule:** The relationships between source code and their required documentation are defined in `scripts/doc-lint-rules.yml`. If a source file with a defined rule is changed, its corresponding documentation must also be changed.
- **Enforcement:** The linter will fail if the documentation is not updated alongside the code.

### 3.3. Linter Execution Scope
- **Scope:** The linter is designed to run **incrementally** on changed files as detected by `git diff`.
- **Rationale:** This ensures that checks are fast, relevant, and focused on the work being done.

### 3.4. Forbidden Document Enforcement
- **Trigger:** Any change to a file listed in the `forbidden_docs` section of a rule in `scripts/doc-lint-rules.yml`.
- **Rule:** These files are considered locked and must not be modified.
- **Enforcement:** The linter will fail if a change is detected in a forbidden document.
- **Note on Unreliable Environments:** In some CI/test environments, the `git diff` command used by the linter may be unreliable. In such cases, the `forbidden_docs` check may require manual verification during code review.

### 3.5. Code Quality Scorecard Enforcement
- **Trigger:** Any change to the `api/docs/CODE_QUALITY_INDEX.md` file.
- **Rule:** The scores in the index **must** align with the A-F scale defined in the `API_DEVELOPER_GUIDE.md`.
- **Enforcement:** The linter will parse the `CODE_QUALITY_INDEX.md` file on every change and validate that all `Doc Score` and `Code Score` values are one of `A, B, C, D, F`. Commits containing invalid scores will be rejected.

### 3.6. Mandatory Logging Enforcement
- **Trigger:** Any change to a file within the project's defined `source_paths` (e.g., any file in `api/src/`, `project/`, `scripts/`, etc.).
- **Rule:** If any code or documentation file is changed, the three project log files (`project/logs/ACTIVITY.md`, `project/logs/SESSION_LOG.md`, `project/logs/CURRENT_STATE.md`) must also be modified.
- **Enforcement:** The linter will fail if the log files are not included in a commit that contains other code/doc changes. This serves as a reminder to the developer to manually log their work using the `linter.py --log` command.

### 3.7. Code File Index Enforcement
- **Trigger:** Any addition, deletion, or renaming of a code file (`.py`, `.go`, `.js`).
- **Rule:** The canonical `api/docs/CODE_FILE_INDEX.md` must be updated to reflect the change. This file serves as the single source of truth for all code files in the repository.
- **Enforcement:** A dedicated CI script (`scripts/validate_code_index.py`) will run on every pull request. It compares the contents of the index with an actual file listing of the repository and fails if they do not match.

### 3.8. Project Registry Governance
- **Trigger:** Any change to files within the `project/` directory.
- **Rule:** The `project/PROJECT_REGISTRY.md` file serves as the canonical, human-readable index for all internal project documentation. This file is **auto-generated** from the master `project/reports/TRACE_INDEX.yml` and must not be edited manually.
- **Scope:** The registry is strictly limited to documents within the `project/` directory. The only exception is `api/docs/CODE_FILE_INDEX.md`, which is included as a cross-cutting project artifact.
- **Enforcement & Updates:** The registry is updated by running the governance script with a specific flag. To regenerate both the machine-readable JSON (`scripts/project_registry.json`) and the human-readable Markdown (`project/PROJECT_REGISTRY.md`), use the following command:
    ```bash
    python3 scripts/repo_inventory_and_governance.py --update-project-registry
    ```
- **Handling Exceptions:** To intentionally include a file that falls outside the standard `project/` scope, its path must be added to the `scripts/project_registry_extras.yml` file. This creates a clear, auditable trail for any exceptions to the rule.

### 3.9. Description Enforcement Policy

- **Trigger:** Any addition or modification of file entries in project indexes or registries, including:
  - `project/reports/TRACE_INDEX.yml`
  - Any `CODE_FILE_INDEX.md` (in any directory)
  - `project/PROJECT_REGISTRY.md`
  - Any future registry or traceability index under `project/` or `scripts/`

- **Rule:** Every file entry added to a registry **must** include a concise, meaningful one-line description at the moment it is added.
  - Descriptions must summarize the file’s function or purpose in clear, human-readable language.
  - Descriptions are mandatory for all file types — including `.md`, `.yml`, `.py`, `.sh`, and any others tracked by the system.
  - No placeholder or empty descriptions are allowed (e.g., “TBD”, “N/A”, “temp”).

- **Rationale:**
  This ensures that every file tracked in the repository is self-descriptive and immediately understandable from its registry entry.
  The policy eliminates the need for retroactive description passes and guarantees traceable documentation hygiene at the point of file registration.

- **Enforcement:**
  - The unified `scripts/linter.py` and CI/CD checks must verify that every file listed in any index or registry contains a valid, non-empty description field.
  - Missing or placeholder descriptions will trigger a **policy violation**, blocking commits or merges until corrected.
  - Contributors are responsible for supplying descriptions during file registration. Automation scripts should never auto-fill descriptions.

## 4. CI/CD & Pull Request (PR) Enforcement
The project uses a multi-stage CI/CD pipeline defined in `.github/workflows/ci.yml` to enforce quality gates. The pipeline is structured to be efficient by separating documentation and code checks.

- **`doc-linter` Job:** This job runs on **every commit** in a pull request. Its sole responsibility is to enforce documentation governance. It runs `scripts/linter.py`, which:
    - Validates documentation rules from `scripts/doc-lint-rules.yml`.
    - Validates the `CODE_QUALITY_INDEX.md` content.
    - Runs an `mkdocs build` to check for broken links in the `api/docs/` documentation.
    - This job **does not** run any code linters or tests.

- **`code-quality` Job:** This job is **conditional**. It only runs if changes are detected in source code directories (e.g., `api/src/`, `scripts/`, `snitch/`). It performs a comprehensive set of checks:
    - Lints code with `ruff`.
    - Checks formatting with `black`.
    - Runs type checking with `mypy`.
    - Scans for vulnerabilities with `bandit` and `safety`.
    - Runs the full `pytest` test suite.

A PR cannot be merged if any of these jobs fail. This ensures that no code or documentation that violates project governance can be merged into the `main` branch.

## 5. Key Governance Documents
- **This Document:** `project/QA_GOVERNANCE.md`
- **The Live Traceability Matrix:** `project/ALIGNMENT_MATRIX.md`
- **The Linter Ruleset:** `scripts/doc-lint-rules.yml`
