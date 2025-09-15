# QA Gate Manual

**Status:** Live Document

## 1. Purpose and Scope
This document describes the project's professional-level **QA Gate**, a comprehensive quality assurance script located at `scripts/qa_gate.py`.

The QA Gate is designed to be run at the end of major project phases or before significant releases. It performs a deep analysis of the codebase, going beyond the lightweight, pre-commit checks performed by the standard `linter.py` script. Its purpose is to provide a final, definitive quality report on the entire repository.

## 2. Python-Specific Checks (Phase 1)
The initial phase of the QA Gate focuses on a deep analysis of the Python codebase, primarily within the `api/` directory. The following tools are integrated:

### 2.1. `ruff`
- **Purpose:** Baseline linting for style, correctness, and best practices.
- **Command:** `ruff check api/src`
- **Threshold:** The script will fail if `ruff` reports any errors.

### 2.2. `pytest`
- **Purpose:** To run the full unit and integration test suite and enforce a minimum code coverage.
- **Command:** `pytest --cov=api/src --cov-fail-under=85 api/tests/`
- **Threshold:** The script will fail if the test coverage for the `api/src` module is below **85%**.

### 2.3. `radon`
- **Purpose:** To analyze code for complexity and maintainability.
- **Commands:**
    - `radon cc -s -a -nb api/src` (Cyclomatic Complexity)
    - `radon mi -s -a -nb api/src` (Maintainability Index)
- **Thresholds:**
    - The script will fail if the average cyclomatic complexity of any file is greater than **5.0**.
    - The script will fail if the average maintainability index of any file is less than **80.0**.

### 2.4. `mutmut`
- **Purpose:** To perform mutation testing, which checks the quality and effectiveness of the test suite.
- **Commands:**
    - `mutmut run`
    - `mutmut results`
- **Threshold:** The script will fail if the mutation score is less than **90%**.

## 3. Future Phases
The QA Gate is designed to be extensible. Future phases will include:
- Documentation quality checks (Phase 2)
- Integration with Go and JavaScript/TypeScript quality tools (Phase 3)
- Full integration into the CI/CD pipeline (Phase 4)
