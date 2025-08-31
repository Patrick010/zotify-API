# Feature Spec: Automated Documentation Workflow

**Status:** Implemented & Live

---

**1. Feature Name:**
Automated Documentation Workflow & Logging

**2. Module/Component:**
Developer Tooling & Project Scripts

**3. Purpose / Business Value:**
To enforce and streamline the project's core "living documentation" policy. This system ensures that all code changes are accompanied by corresponding documentation updates and that all work is logged in a consistent, structured manner. It reduces manual overhead for developers and guarantees that the project's documentation stays synchronized with its implementation.

**4. Description of Functionality:**
This feature consists of two primary, interconnected components: a documentation linter (`lint-docs.py`) and a work-logging utility (`log-work.py`).

*   **`lint-docs.py` (The Enforcer):**
    *   A script that runs as a `pre-commit` hook to enforce documentation standards. It has two main rules:
    *   **1. Registry Completeness Check:** The script first scans the entire repository for all `.md` files and helper scripts (`scripts/*`). It compares this list against all the file paths linked in the `project/PROJECT_REGISTRY.md`. If it finds any files that are not registered, the commit will fail. This ensures the project registry remains a true single source of truth.
    *   **2. Documentation-with-Code Check:** It inspects all files staged for a commit. If any source code or test files have been modified, it requires that at least one documentation file is also staged in the same commit. This makes the "docs-as-code" policy mandatory.
    *   **Configuration:** The script's behavior is controlled by rules defined in `scripts/doc-lint-rules.yml`. This allows for project-specific customization, such as defining which files are considered "documentation" and which files are "forbidden" from being modified (e.g., `HANDOVER_BRIEF.md`).

*   **`log-work.py` (The Scribe):**
    *   A command-line utility designed to simplify and standardize the process of logging work.
    *   It takes structured inputs and correctly appends them to the three "Trinity" logs: `project/logs/ACTIVITY.md`, `project/logs/SESSION_LOG.md`, and `project/logs/CURRENT_STATE.md`.
    *   This removes the need for developers to manually edit these files, preventing formatting errors and ensuring each log receives the semantically correct information.

**5. Technical Details:**
*   `lint-docs.py` determines file categories (source, test, docs) based on path prefixes defined within the script. It is designed to fail the commit if its rules are not met, providing clear feedback to the developer.
*   `log-work.py` uses command-line arguments (`--activity`, `--session`, `--state`, `--files`) to accept structured input for each of the logs.

**6. Associated Endpoints or Functions:**
*   This is a developer tooling feature and has no API endpoints.
*   Key Scripts: `scripts/lint-docs.py`, `scripts/log-work.py`
*   Configuration: `scripts/doc-lint-rules.yml`, `.pre-commit-config.yaml`

**7. Inputs:**
*   `lint-docs.py`: Reads staged file paths from Git.
*   `log-work.py`: Takes string inputs from the command line.

**8. Outputs:**
*   `lint-docs.py`: Prints success or failure messages to the console and returns a corresponding exit code to the pre-commit framework.
*   `log-work.py`: Modifies the three log files in `project/logs/`.

**9. Dependencies:**
*   External Libraries: `pyyaml` (for `lint-docs.py`)
*   Frameworks: `pre-commit`

**10. Testing & Validation Notes:**
*   The workflow is validated by its successful execution during the development process. The `pre-commit` hook's failure on non-compliant commits and the successful update of logs by `log-work.py` serve as validation.

**11. Related Documentation:**
*   `AGENTS.md` (provides instructions on using the tools)
*   `api/docs/manuals/API_DEVELOPER_GUIDE.md` (documents the workflow for contributors)
*   `project/PROJECT_REGISTRY.md` (registers the scripts and this spec)
*   `project/PID.md` (incorporates the workflow into project controls)
