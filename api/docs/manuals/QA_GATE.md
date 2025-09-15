# QA Gate Manual

## 1. Overview
This document describes the project's new, unified Quality Assurance (QA) Gate, located at `scripts/qa_gate.py`. This system is designed to replace the old, simpler linter with a robust, multi-language set of checks for code quality, documentation quality, and index consistency.

The QA Gate is designed to be the single entrypoint for all code and documentation verification, ensuring that all changes meet the project's quality standards before being submitted.

## 2. Phase 1: Python Code Quality
The first phase of the QA Gate implementation focuses on establishing a strong baseline for Python code quality. The following tools are integrated and run on every execution:

### 2.1. Ruff
- **Purpose:** Baseline linting and style checking.
- **Command:** `ruff check .`
- **Result:** Fails if any linting errors are found.

### 2.2. Pytest & Coverage
- **Purpose:** Ensures all unit tests pass and that test coverage meets the minimum threshold.
- **Command:** `pytest --cov=api/src/zotify_api --cov-fail-under=80 api/tests/`
- **Result:** Fails if any test fails or if code coverage drops below 80%.

### 2.3. Radon
- **Purpose:** Static analysis for code complexity and maintainability.
- **Checks:**
    - Cyclomatic Complexity: Must be `<= 10`.
    - Maintainability Index: Must be `>= 70`.
- **Status:** **Warning Only.** Due to environment-specific issues, the Radon check is currently bypassed. This will be addressed in a future update.

### 2.4. Mutmut
- **Purpose:** Mutation testing to ensure the quality and effectiveness of the test suite.
- **Check:** Mutation score must be `>= 70%`.
- **Status:** **Warning Only.** Due to environment-specific issues, the Mutmut check is currently bypassed. This will be addressed in a future update.

---

*This is a living document and will be updated as new phases of the QA Gate are implemented.*
