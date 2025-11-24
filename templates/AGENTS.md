# Agent Instructions & Automated Workflow System

**Version:** 2.0
**Status:** Active

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

### Step 1: Code and Document
This is the primary development task. When you make changes to the code, you are responsible for updating all corresponding documentation.

To identify which documents are relevant for a given change, you **must** consult the `project/project_registry.md`. This file is the single source of truth for all project documents.

### Step 2: Log Your Work
At the completion of any significant action, you **must** log the work using the `log-work` script.

*   **Command:** `python scripts/log_work.py --task "A clear, concise summary of the action taken."`
*   **Automation:** This command automatically updates `project/logs/ACTIVITY.md` and `project/logs/SESSION_LOG.md`.

### Step 3: Assess Quality and Update Index
To ensure a high standard of quality, all code and documentation changes must be assessed.

1.  **Assess Your Changes:** Review your modified files against the scoring rubric defined in the `API_DEVELOPER_GUIDE.md`.
2.  **Update the Index:** Add or update the corresponding entries in the `CODE_QUALITY_INDEX.md` file. This is a mandatory step.

### Step 4: Pre-Submission Verification
Before submitting your work for review, you **must** run the following tools to verify compliance.

1.  **Run Tests:**
    *   **Command:** `bash scripts/run_lint.sh.sh`
    *   **Purpose:** This script runs the full `pytest` suite to ensure your changes have not introduced any regressions. You must resolve any test failures.

2.  **Run Documentation Linter:**
    *   **Command:** `python scripts/lint-docs.py`
    *   **Purpose:** This is the core enforcement tool for the Living Documentation policy. It uses the "documentation matrix" defined in `scripts/doc-lint-rules.yml` to check that all required documentation has been updated. You must resolve any errors it reports.

3.  **Build Documentation Site:**
    *   **Command:** `mkdocs build`
    *   **Purpose:** This command builds the static documentation website into the `site/` directory. This mandatory step catches syntax errors in documentation and ensures the final product is valid. The site can be previewed locally by running `mkdocs serve`.

---

## 4. Key Policy Documents (Reference)

This automated workflow is designed to fulfill the rules defined in the following core documents. Refer to them if you need more context on the *why* behind the rules.

*   `project/PID.md`
*   `project/HIGH_LEVEL_DESIGN.md`
*   `project/TASK_CHECKLIST.md`
