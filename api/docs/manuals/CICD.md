# Portable CI/CD and Linter Guide

This document provides a comprehensive overview of the CI/CD and local linting infrastructure used in this project. It is designed to be a reusable template that can be adapted for other projects.

## Table of Contents
1.  [Philosophy](#1-philosophy)
2.  [CI/CD Pipeline (`ci.yml`)](#2-cicd-pipeline-ciyml)
3.  [Local Enforcement (Pre-commit)](#3-local-enforcement-pre-commit)
4.  [Custom Documentation Linter](#4-custom-documentation-linter)
5.  [How to Port to a New Project](#5-how-to-port-to-a-new-project)

---

## 1. Philosophy

This setup is built on two core principles:
-   **Catch Errors Early:** The `pre-commit` hooks provide immediate feedback to developers before code is even committed, catching simple errors and style issues locally.
-   **Comprehensive Centralized Validation:** The GitHub Actions CI/CD pipeline serves as the ultimate source of truth for project quality. It runs a more extensive suite of tests, type checks, and security scans that might be too slow for every commit.

By combining these two approaches, we achieve a fast local development loop while maintaining high quality standards for the main repository.

---

## 2. CI/CD Pipeline (`ci.yml`)

The full CI/CD pipeline is defined in `.github/workflows/ci.yml`. It is triggered on every push and pull request to the `main` branch and consists of several independent jobs:

-   `test`: Installs dependencies, creates a test environment, and runs the full `pytest` suite with coverage checks.
-   `lint`: Runs linters for different languages (`ruff` for Python, `golangci-lint` for Go) to enforce code style and catch common errors.
-   `type-check`: Runs `mypy` to perform static type checking on the Python codebase.
-   `security-scan`: Runs `bandit` for static application security testing and `safety` to check for known vulnerabilities in dependencies.
-   `doc-linter`: Runs our unified linter script (`scripts/linter.py`) to enforce all documentation policies and project standards.

---

## 3. Local Enforcement (Pre-commit)

To catch errors locally, we use the `pre-commit` framework.

### Setup

1.  **Install the tool:**
    ```bash
    pip install pre-commit
    ```
2.  **Install the hooks:** In the root of the repository, run:
    ```bash
    pre-commit install
    ```
    This command reads the `.pre-commit-config.yaml` file and installs the defined git hooks. From now on, the defined scripts will run on all staged files every time you run `git commit`.

### Configuration (`.pre-commit-config.yaml`)

The behavior is controlled by the `.pre-commit-config.yaml` file. This file defines which scripts to run. For this project, it is configured to run the custom documentation linter.

---

## 4. Unified Linter (`linter.py`)

The heart of our documentation-as-code policy is the unified linter script.

-   **Location:** `scripts/linter.py`
-   **Purpose:** To act as a single entrypoint for all documentation verification and work logging, ensuring that the project's "living documentation" stays synchronized with the code.
-   **Execution:** This script is intended to be run manually from the command line, not as a pre-commit hook.
-   **Logic & Modes:**
    1.  **Verification Mode (`python3 scripts/linter.py`):** When run without arguments, the script acts as an intelligent linter. It runs a suite of checks based on rules in `scripts/doc-lint-rules.yml`, such as verifying file registrations and ensuring code changes are reflected in the alignment matrix. It also conditionally runs tests (`pytest`) and documentation builds (`mkdocs`) based on the files changed.
    2.  **Logging Mode (`python3 scripts/linter.py --log ...`):** When run with the `--log` flag, the script becomes a standardized logging utility. It takes structured arguments and updates the three "Trinity" logs (`ACTIVITY.md`, `SESSION_LOG.md`, `CURRENT_STATE.md`) automatically.

---

## 5. How to Port to a New Project

To use this CI/CD and linting setup in a new project, follow these steps:

1.  **Copy the Core Files:**
    Copy the following files and directories from this project to your new project's root:
    -   `.github/workflows/ci.yml`
    -   `scripts/linter.py`
    -   `scripts/doc-lint-rules.yml`
    -   `.pre-commit-config.yaml`
    -   This `CICD.md` guide itself (from `templates/`).

2.  **Adapt `ci.yml`:**
    -   Review each job in `ci.yml`.
    -   Remove any jobs that are not relevant to your new project (e.g., if your new project doesn't use Go, remove the `golangci-lint` steps).
    -   Update paths and installation commands to match your new project's structure.

3.  **Adapt `doc-lint-rules.yml`:**
    -   Open the `scripts/doc-lint-rules.yml` file.
    -   Update the file paths and rules to match the directory structure and policies of your new project.

4.  **Follow the Setup:**
    -   Follow the setup instructions in Section 3 of this guide to activate the pre-commit hooks in your new project.
