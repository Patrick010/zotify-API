# Zotify API: Contributor's Guide

This document is for developers who wish to contribute directly to the Zotify API codebase. It outlines the development workflow, architectural patterns, and quality standards required for all contributions.

For information on how to consume or integrate with the API, please see the [`SYSTEM_INTEGRATION_GUIDE.md`](./SYSTEM_INTEGRATION_GUIDE.md).

## Table of Contents
1.  [Core Principles](#1-core-principles)
2.  [Development Workflow](#2-development-workflow)
3.  [Running Quality Checks](#3-running-quality-checks)
4.  [How to Add a New Provider](#4-how-to-add-a-new-provider)
5.  [Proposing Architectural Changes](#5-proposing-architectural-changes)

---

## 1. Core Principles

This project operates under a strict **"living documentation"** model.
-   **Reality First:** The codebase is the single source of truth. All documentation must reflect the actual, verified behavior of the application.
-   **Continuous Alignment:** All code changes **must** be accompanied by corresponding documentation updates in the same commit. This includes design documents, user guides, and changelogs.
-   **Mandatory Checklist:** All changes must follow the steps outlined in `project/TASK_CHECKLIST.md` to be considered "Done".

---

## 2. Development Workflow

To enforce the "living documentation" model, this project uses a unified linter script (`scripts/linter.py`) that handles both pre-submission verification and work logging. Follow this workflow for all contributions:

1.  **Create an Issue & Branch:** Before starting work, ensure there is a GitHub issue and create a new feature branch.
2.  **Implement Changes:** Write your code and the corresponding documentation updates.
3.  **Run Quality Checks:** Before committing, run all the quality checks detailed in Section 3. Most importantly, run the unified linter in verification mode to ensure your changes are compliant:
    ```bash
    python3 scripts/linter.py
    ```
4.  **Commit Your Work:** Once all checks pass, commit your changes.
5.  **Log Your Work:** After committing, you must log your work using the linter's logging mode. This updates the project's "Trinity" logs (`ACTIVITY.md`, `SESSION_LOG.md`, and `CURRENT_STATE.md`). See `AGENTS.md` for full instructions.
    ```bash
    python3 scripts/linter.py --log --summary "Your one-line summary" --findings "Detailed findings..." --next-steps "Next steps..." --files file1.md file2.py
    ```
6.  **Follow the `TASK_CHECKLIST.md`:** Manually go through the checklist to ensure all project standards have been met.
7.  **Submit a Pull Request:** Create a pull request linking to the original issue.

---

## 3. Running Quality Checks

For a comprehensive overview of the project's CI/CD pipeline and local quality checks, please see the embedded guide below.

--8<-- "project/CICD.md"

Before committing, you must run the following checks from the project root.

-   **Linter (`ruff`):**
    ```bash
    ruff check . --fix
    ruff format .
    ```

-   **Type Checking (`mypy`):**
    ```bash
    # Run from the project root
    mypy api/src
    ```

-   **Security Scan (`bandit`):**
    ```bash
    # Run from the project root
    bandit -c bandit.yml -r api
    ```
-   **Unified Linter (Verification Mode):**
    The unified linter should be run locally before committing to ensure documentation is up-to-date. It uses the rules defined in `scripts/doc-lint-rules.yml`.
    ```bash
    # Run in pre-commit mode to check staged files
    PRE_COMMIT=1 python scripts/linter.py
    ```

---

## 4. How to Add a New Provider

The API is designed to be extensible with new music providers. To add a new one, you must implement the `BaseProvider` interface.

1.  **Create a New Connector File:**
    -   Create a new file in `api/src/zotify_api/providers/`, for example, `my_music_connector.py`.

2.  **Implement the `BaseProvider` Interface:**
    -   Your new class must inherit from `BaseProvider` and implement all its abstract methods.
    -   The required interface is defined in `api/src/zotify_api/providers/base.py`:
        ```python
        from abc import ABC, abstractmethod
        from typing import Any, Dict, List, Optional, Tuple

        class BaseProvider(ABC):
            @abstractmethod
            async def search(self, q: str, type: str, limit: int, offset: int) -> Tuple[List[Dict[str, Any]], int]:
                pass

            @abstractmethod
            async def get_playlist(self, playlist_id: str) -> Dict[str, Any]:
                pass

            @abstractmethod
            async def get_playlist_tracks(self, playlist_id: str, limit: int, offset: int) -> Dict[str, Any]:
                pass

            @abstractmethod
            async def sync_playlists(self) -> Dict[str, Any]:
                pass

            @abstractmethod
            async def get_oauth_login_url(self, state: str) -> str:
                pass

            @abstractmethod
            async def handle_oauth_callback(self, code: Optional[str], error: Optional[str], state: str) -> str:
                pass
        ```

3.  **Update Provider Factory:**
    -   (This step is a future enhancement. Currently, providers are hardcoded. A future refactor will introduce a factory function to dynamically load providers.)

---

## 5. Proposing Architectural Changes

For significant architectural changes (e.g., adding a new major component, changing a core data flow), a formal proposal is required.

1.  **Create a Proposal Document:**
    -   Create a new markdown file in `project/proposals/`.
    -   Use existing proposals like `DYNAMIC_PLUGIN_PROPOSAL.md` as a template.
    -   The proposal should clearly state the problem, the proposed solution, and the impact on other systems.
2.  **Update High-Level Documentation:**
    -   The proposal must be referenced in `project/HIGH_LEVEL_DESIGN.md` and `project/FUTURE_ENHANCEMENTS.md`.
3.  **Update Project Registry:**
    -   The new proposal document must be added to `project/PROJECT_REGISTRY.md`.
4.  **Seek Approval:**
    -   Submit the changes for review and approval before beginning implementation.

---

## 6. Code Quality Index

This project uses a quality scoring system to track the overall quality of all source code files. The goal is to ensure all code is understandable, maintainable, and well-tested.

### 6.1. Scoring Rubric

Each file is assigned two independent quality scores: one for **Documentation (`Doc Score`)** and one for **Code (`Code Score`)**.

#### Documentation Score
This score assesses the quality, completeness, and clarity of comments and docstrings.

| Grade | Criteria |
| :---: | --- |
| **A** | **Excellent:** Comprehensive module, class, and function docstrings are all present and follow a consistent style. All public methods are documented. Complex logic, algorithms, and business rules are explained with inline comments. |
| **B** | **Good:** Most public methods have docstrings, but they may lack detail or consistency. Some complex logic is commented, but not all. |
| **C** | **Needs Improvement:** Docstrings are sparse or missing for many methods. Little to no inline comments to explain complex sections. A new developer would struggle to understand the file's purpose without reading the code. |
| **D** | **Poor:** Only a few, minimal docstrings or comments exist. The file is effectively undocumented. |
| **F** | **Unacceptable:** No docstrings or comments whatsoever. |

#### Code Quality Score
This score assesses the implementation's clarity, efficiency, structure, and testability.

| Grade | Criteria |
| :---: | --- |
| **A** | **Excellent:** Code is clear, efficient, and well-structured, following established design patterns. It has high, meaningful unit test coverage (>90%). Logic is simple and easy to follow. |
| **B** | **Good:** Code is functional but could be improved. It might be slightly inefficient, have some overly complex functions, or have only moderate test coverage (50-90%). |
| **C** | **Needs Improvement:** Code is difficult to understand, contains significant technical debt (e.g., large functions, deep nesting, magic numbers), or has low test coverage (<50%). |
| **D** | **Poor:** Code is highly inefficient, convoluted, or buggy. It may have little to no test coverage and poses a maintenance risk. |
| **F** | **Unacceptable:** Code is non-functional, contains critical bugs, or is a direct copy-paste from another source without adaptation. |

### 6.2. Code Quality Index File

A complete inventory of all source code files and their current quality scores is maintained in the **Code Quality Index**. Developers should consult this index to identify areas that need improvement and to update the scores after improving a file's quality.

-   **[View the API Code Quality Index](../reference/CODE_QUALITY_INDEX.md)**
