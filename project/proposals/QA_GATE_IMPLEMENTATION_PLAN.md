<!-- ID: DOC-055 -->
# QA Gate Implementation Plan

**Status:** Proposed

## 1. Overview
This document outlines the phased implementation plan for creating a professional-level, multi-language QA Gate for the project. This system will complement the current, simpler linter with a robust set of checks for code quality, documentation quality, and index consistency.The QA Gate linter will need to be run at the end of project phases.

The implementation is broken down into the following phases to ensure a structured rollout and allow for feedback at each stage.

---

## Phase 1: Python Code Quality Foundation (Active)

**Objective:** To establish the core `qa_gate.py` script and implement all specified quality checks for the Python codebase.

**Tasks:**
1.  **Create `qa_gate.py` script:**
    -   Create the main entrypoint script in `scripts/qa_gate.py`.
    -   Implement the `run_code_quality()` and `run_docs_quality()` function stubs.
2.  **Install New Python Dependencies:**
    -   Add `Radon` and `mutmut` to the project's dependencies.
3.  **Implement Python Code Checks in `run_code_quality()`:**
    -   Integrate `ruff` for baseline linting.
    -   Integrate `pytest` with a coverage check of `>= 85%`.
    -   Integrate `radon` to check for cyclomatic complexity (`<= 5`) and maintainability index (`>= 80`).
    -   Integrate `mutmut` for mutation testing with a score threshold of `>= 90%`.
4.  **Create Placeholder Helper Scripts:**
    -   Create `scripts/check_docs_alignment.py` with a placeholder "Not Implemented" message.
    -   Create `scripts/check_quality_indexes.py` with a placeholder "Not Implemented" message.
5.  **Create `QA_GATE.md` Documentation:**
    -   Create the new manual at `api/docs/manuals/QA_GATE.md`.
    -   Document the purpose and scope of the QA Gate.
    -   Detail the Python-specific checks and tools implemented in this phase.
    -   Register the new manual in `api/docs/MASTER_INDEX.md`.

---

## Phase 2: Documentation Quality Checks (Planned)

**Objective:** To implement the logic for the complex documentation quality checks.

**Tasks:**
1.  **Implement `check_docs_alignment.py`:**
    -   The script must scan all source files (`.py`, `.go`, `.js`, .html, .sh).
    -   It must verify that a corresponding `.md` file exists in `api/docs/reference/source/`.
    -   It must parse the markdown file to ensure it contains the required sections (Role, Usage, API, etc.).
    -   It must parse the source file (e.g., using `ast` for Python) to get a list of public functions/classes and ensure they are referenced in the markdown file.
2.  **Implement `check_quality_indexes.py`:**
    -   The script must parse both `CODE_QUALITY_INDEX.md` and `DOCS_QUALITY_INDEX.md`.
    -   It must validate that every source file and every documentation file has an entry.
    -   It must perform consistency checks (e.g., if a file has an 'A' rating for test coverage, the script must verify that the coverage is indeed >= 85%).
3.  **Update `qa_gate.py`:**
    -   Integrate the calls to these two new helper scripts into the `run_docs_quality()` function.

---

## Phase 3: Go & JavaScript/TypeScript Integration (Planned)

**Objective:** To expand the code quality checks to cover all languages in the repository.

**Tasks:**
1.  **Install Go Dependencies:**
    -   Install `gocyclo`.
2.  **Install JS/TS Dependencies:**
    -   Set up a `package.json` if one doesn't exist.
    -   Install `eslint` (with complexity plugin), `jest`, and `stryker`.
3.  **Update `qa_gate.py`:**
    -   Add logic to the `run_code_quality()` function to call the appropriate tools based on file extensions.
    -   Run `golangci-lint` and `gocyclo` for `.go` files.
    -   Run `eslint`, `jest`, and `stryker` for `.js`/`.ts` files.

---

## Phase 4: CI/CD Integration (Planned)

**Objective:** To fully integrate the new QA Gate into the CI/CD pipeline.

**Tasks:**
1.  **Update `.github/workflows/ci.yml`:**
    -   Replace the current `code-quality` job with a new job that runs `python scripts/qa_gate.py`.
    -   Ensure all new dependencies for all languages are installed in the CI environment.
2.  **Update `project/QA_GOVERNANCE.md`:**
    -   Update the documentation to reflect the new, comprehensive QA Gate system, replacing the description of the old linter.
