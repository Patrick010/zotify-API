# [Project Name]: Contributor's Guide

This document is for developers who wish to contribute directly to the [Project Name] codebase. It outlines the development workflow, architectural patterns, and quality standards required for all contributions.

For information on how to consume or integrate with the API, please see the `SYSTEM_INTEGRATION_GUIDE.md`.

## Table of Contents
1.  [Core Principles](#1-core-principles)
2.  [Development Workflow](#2-development-workflow)
3.  [Running Quality Checks](#3-running-quality-checks)
4.  [How to Add a New Provider](#4-how-to-add-a-new-provider)
5.  [Proposing Architectural Changes](#5-proposing-architectural-changes)
6.  [Documentation Linter](#6-documentation-linter)

---

## 1. Core Principles

This project operates under a strict **"living documentation"** model.
-   **Reality First:** The codebase is the single source of truth. All documentation must reflect the actual, verified behavior of the application.
-   **Continuous Alignment:** All code changes **must** be accompanied by corresponding documentation updates in the same commit.
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

For a comprehensive overview of the project's CI/CD pipeline and local quality checks, please refer to the main `CICD.md` guide.

Before committing, you must run the following checks from the project root.
-   **Linter:** `[linter command]`
-   **Type Checking:** `[type checker command]`
-   **Security Scan:** `[security scan command]`

---

## 4. How to Add a New Provider (Example)

This section should be adapted for your project's specific extension points.

The API is designed to be extensible with new providers. To add one, you must implement the `BaseProvider` interface.

1.  **Create a New Connector File:**
    -   Create a new file in `src/providers/`, for example, `my_new_connector.py`.

2.  **Implement the `BaseProvider` Interface:**
    -   Your new class must inherit from `BaseProvider` and implement all its abstract methods.

---

## 5. Proposing Architectural Changes

For significant architectural changes, a formal proposal is required.

1.  **Create a Proposal Document:**
    -   Create a new markdown file in `project/proposals/`.
2.  **Update High-Level Documentation:**
    -   The proposal must be referenced in `project/HIGH_LEVEL_DESIGN.md`.
3.  **Update Project Registry:**
    -   The new proposal document must be added to `project/PROJECT_REGISTRY.md`.
4.  **Seek Approval:**
    -   Submit the changes for review and approval before beginning implementation.

---

## 6. Documentation Linter

To automatically enforce the "living documentation" principle, the project includes a custom linter.

### How It Works

The linter's logic is based on a "module" system, inferred from the top-level directory structure.

> If a pull request contains changes to source code or tests within a module, it **must** also contain changes to a documentation file.

A documentation change can be within the same module's `docs` directory or in the top-level `project/` directory. If this rule is violated, the `doc-linter` job in the CI pipeline will fail.
