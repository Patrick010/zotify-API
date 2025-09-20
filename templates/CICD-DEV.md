# Portable CI/CD and Linter Guide (For Developers)

This document provides a comprehensive technical overview of the CI/CD and local linting infrastructure. It is designed to be a reusable template that can be adapted for other projects.

For a high-level overview of the CI/CD philosophy and quality gates, please see the `cicd-proj.md` template.

## Table of Contents
1.  [CI/CD Pipeline (`ci.yml`)](#1-cicd-pipeline-ciyml)
2.  [Local Enforcement (Pre-commit)](#2-local-enforcement-pre-commit)
3.  [Custom Documentation Linter](#3-custom-documentation-linter)
4.  [How to Port to a New Project](#4-how-to-port-to-a-new-project)

---

## 1. CI/CD Pipeline (`ci.yml`)

The full CI/CD pipeline is defined in `.github/workflows/ci.yml`. It consists of several independent jobs:

-   `test`: Installs dependencies and runs the `pytest` suite with coverage checks.
-   `lint`: Runs linters like `ruff` and `golangci-lint` to enforce code style.
-   `type-check`: Runs `mypy` for static type checking.
-   `security-scan`: Runs `bandit` and `safety` to find security vulnerabilities.
-   `doc-linter`: Runs the custom documentation linter.

---

## 2. Local Enforcement (Pre-commit)

We use the `pre-commit` framework to run local checks before commits.

### Setup

1.  **Install the tool:** `pip install pre-commit`
2.  **Install the hooks:** `pre-commit install`

This reads the `.pre-commit-config.yaml` file and activates the hooks.

### Configuration (`.pre-commit-config.yaml`)

This file defines which scripts to run. For this project, it is configured to run the custom documentation linter.

---

## 3. Custom Documentation Linter

-   **Location:** `scripts/lint-docs.py`
-   **Purpose:** To ensure that when code is modified, documentation is also modified.
-   **Logic:**
    1.  The script identifies all files staged for a commit.
    2.  It categorizes each file into a "module" based on its path.
    3.  **The Rule:** If a code/test file in a module is staged, a documentation file must also be staged.
    4.  **Flexibility:** A doc change can be in the module's `docs` directory or in the main `project/` directory.
    5.  **Outcome:** If the rule is broken, the script fails and prevents the commit.

---

## 4. How to Port to a New Project

1.  **Copy Core Files:**
    -   `.github/workflows/ci.yml`
    -   `scripts/lint-docs.py`
    -   `.pre-commit-config.yaml`
    -   This `cicd-dev.md` guide and its `cicd-proj.md` counterpart.

2.  **Adapt `ci.yml`:**
    -   Review and remove irrelevant jobs.
    -   Update paths and installation commands.

3.  **Adapt `lint-docs.py`:**
    -   Update the `..._PREFIXES` variables at the top of the file to match your new project's directory structure.

4.  **Follow Setup:**
    -   Follow the setup instructions in Section 2 of this guide.
