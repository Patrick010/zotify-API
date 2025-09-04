# Agent Instructions & Automated Workflow System

**Version:** 2.0
**Status:** Active

---

## 0. Fundamental Rules

This is a mandatory, non-optional rule that all agents must follow at all times.

    Do not approve your own tasks or plans. Do not make un-asked for changes. Do not start tasks or plans without approval.

---

## 1. About This System

### 1.1. Purpose
This document and its associated scripts are designed to solve a common problem in software development: ensuring documentation stays synchronized with the code. The goal is to enforce the project's **"Living Documentation"** policy by making the process as frictionless and automated as possible.

### 1.2. How It Works
The system consists of three main components:
1.  **This Document (`AGENTS.md`):** The central source of truth for the workflow. AI agents are programmed to read this file and follow its instructions.
2.  **Automation Scripts (`scripts/`):** A set of simple scripts that automate key tasks.
3.  **Configuration (`scripts/doc-lint-rules.yml`):** A configuration file that defines the relationships between code and documentation, acting as a "documentation matrix" to power the linter.

### 1.3. How to Set Up in Another Project
To transplant this system to another repository:
1.  **Copy Files:** Copy this `AGENTS.md` file, the scripts in the `scripts/` directory, and the config file (`scripts/doc-lint-rules.yml`).
2.  **Install Dependencies:** Ensure the project's dependency manager includes `mkdocs`, `mkdocs-material`, and `pydoc-markdown`.
3.  **Customize:** Edit `scripts/doc-lint-rules.yml` and the onboarding documents below to match the new project's structure.

---

## 2. Agent Onboarding

Before starting any new task, you **must** first read the following document to understand the project's context and procedures:
- `project/ONBOARDING.md`

---

## 3. The Automated Workflow

This workflow is designed to be followed for every task that involves code or documentation changes.

### Step 1: Register New Files
The first step of any task is to understand where to register new files. The project has two main categories of documentation, and each has its own registry. Failing to register a new file in the correct location will cause the `scripts/linter.py` verification script to fail.

*   **Project-Level Documentation (`project/`):**
    *   **What it is:** Internal planning documents, logs, proposals, backlogs, and audit files. Anything that lives in the `project/` directory.
    *   **Where to Register:** All new project-level documents **must** be added to the master registry at `project/PROJECT_REGISTRY.md`.

*   **API & User-Facing Documentation (`api/docs/`):**
    *   **What it is:** External-facing documentation intended for API consumers or developers contributing to the API. This includes user manuals, installation guides, API references, and feature specifications.
    *   **Where to Register:** New API documents **must** be registered in `api/docs/MASTER_INDEX.md`.

### Step 2: Code and Document
This is the primary development task. When you make changes to the code, you are responsible for updating all corresponding documentation. Use the registries mentioned in Step 1 to identify relevant documents.

### Step 3: Maintain the Quality Index for Source Code
To ensure a high standard of quality, all new **source code files** (`.py`, `.go`, `.js`) must be registered in the appropriate quality index. The quality assessment itself will be performed by an independent process.

1.  **Add New Files to Index:** When you create a new source file, you **must** add a corresponding entry to the consolidated `project/CODE_QUALITY_INDEX.md` file.
2.  **Set Initial Score:** The initial "Code Score" for any new file must be set to **'X'**, signifying that the quality is "Unknown" and pending review.

### Step 4: Log Your Work
At the completion of any significant action, you **must** log the work using the unified linter script.

*   **Command:** `python scripts/linter.py --log --summary "..." --objective "..." --outcome "..." --files ...`
*   **Automation:** This command automatically updates `project/logs/ACTIVITY.md`, `project/logs/CURRENT_STATE.md` and `project/logs/SESSION_LOG.md`.

> **Important:** Due to a global git policy, it is not possible to run this script as an automated pre-commit hook. Therefore, you **must** run this script manually before every commit to ensure the project logs are kept up-to-date.

### Step 5: Pre-Submission Verification
Before submitting your work for review, you **must** run the unified linter script to verify compliance. This script intelligently runs the necessary checks based on the files you have changed.

*   **Command:** `python3 scripts/linter.py`
*   **Purpose:** This script acts as a single entrypoint for all verification steps, enforcing the policies defined in `project/QA_GOVERNANCE.md`. It will:
    1.  **Run Documentation Linters:** It runs a suite of checks based on the rules in `doc-lint-rules.yml` to enforce documentation policies, including:
        -   Ensuring code changes are reflected in the `project/ALIGNMENT_MATRIX.md`.
        -   Ensuring new source files are added to the `project/CODE_QUALITY_INDEX.md`.
        -   Ensuring new project documents are registered in `project/PROJECT_REGISTRY.md`.
        -   Ensuring new API documents are registered in `api/docs/MASTER_INDEX.md`.
    2.  **Run Tests:** Conditionally runs the `pytest` test suite if it detects changes to source code files (`.py`, `.go`).
    3.  **Build Docs:** Conditionally runs the `mkdocs build` command if it detects changes to the documentation files in `api/docs/`.
*   You must resolve any errors reported by the script before submitting.

---

## 4. Key Policy Documents (Reference)

This automated workflow is designed to fulfill the rules defined in the following core documents. Refer to them if you need more context on the *why* behind the rules.

*   `project/PID.md`
*   `project/HIGH_LEVEL_DESIGN.md`
*   `project/TASK_CHECKLIST.md`
*   `project/QA_GOVERNANCE.md`
