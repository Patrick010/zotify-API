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

Follow these steps for every contribution:

1.  **Create an Issue:** Before starting work, ensure there is a GitHub issue describing the bug or feature.
2.  **Create a Branch:** Create a new feature branch from `main`.
3.  **Implement Changes:** Write your code and the corresponding documentation updates.
4.  **Run Quality Checks:** Ensure all quality checks (see section below) pass before committing.
5.  **Update Logs:** Add entries to `project/logs/ACTIVITY.md` and `project/logs/SESSION_LOG.md` detailing the work.
6.  **Follow the `TASK_CHECKLIST.md`:** Manually go through the checklist to ensure all project standards have been met.
7.  **Submit a Pull Request:** Create a pull request linking to the original issue.

---

## 3. Running Quality Checks

For a comprehensive overview of the project's CI/CD pipeline and local quality checks, please refer to the main [`CICD.md`](../../../project/CICD.md) guide.

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
    bandit -c api/bandit.yml -r api
    ```
-   **Documentation Linter (CI Only):**
    The documentation linter runs automatically in the CI/CD pipeline. It checks that code changes are accompanied by corresponding documentation changes. See the dedicated section below for more details.

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

## 6. Documentation Linter

To automatically enforce the "living documentation" principle, the project includes a custom linter that runs in the CI pipeline. This linter ensures that code changes are accompanied by corresponding documentation updates.

### How It Works

The linter's logic is based on a "module" system, which is inferred from the top-level directory structure. The primary modules are `api`, `snitch`, and `gonk-testUI`.

The rule is as follows:

> If a pull request contains changes to source code or tests within a module (e.g., `api/src` or `api/tests`), it **must** also contain changes to a documentation file.

### What Counts as a Documentation Change?

A documentation change can be one of two things:

1.  **A change to a document within the same module.** For example, a change to `api/src/main.py` can be accompanied by a change to `api/docs/USER_MANUAL.md`.
2.  **A change to any document in the top-level `project/` directory.** This allows high-level design documents (like `project/HIGH_LEVEL_DESIGN.md`) or logs to serve as valid documentation for a code change in any module.

If this rule is violated, the `doc-linter` job in the CI pipeline will fail, blocking the pull request until a valid documentation change is added.
