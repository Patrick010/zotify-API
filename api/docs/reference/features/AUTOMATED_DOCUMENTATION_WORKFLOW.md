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
This feature consists of a single, unified script (`scripts/linter.py`) that serves as the entry point for all documentation workflow and logging tasks. It operates in two primary modes:

*   **Verification Mode (The Enforcer):**
    *   When run without arguments (`python3 scripts/linter.py`), the script acts as a powerful, intelligent linter.
    *   It runs a suite of checks based on the rules defined in `scripts/doc-lint-rules.yml` to enforce documentation policies, such as ensuring new files are registered and that code changes are reflected in the alignment matrix.
    *   It conditionally runs the `pytest` test suite if it detects changes to source code files.
    *   It conditionally runs the `mkdocs build` command if it detects changes to documentation files.
    *   This command must be run manually before submitting work for review.

*   **Logging Mode (The Scribe):**
    *   When run with the `--log` flag, the script acts as a standardized work-logging utility.
    *   It takes structured inputs (e.g., `--summary`, `--findings`) and correctly appends them to the three "Trinity" logs: `project/logs/ACTIVITY.md`, `project/logs/SESSION_LOG.md`, and `project/logs/CURRENT_STATE.md`.
    *   This removes the need for developers to manually edit these files, preventing formatting errors and ensuring each log receives the semantically correct information.

**5. Technical Details:**
*   The script's behavior is controlled by rules defined in `scripts/doc-lint-rules.yml`.
*   Due to a global git policy, it is not possible to run this script as an automated pre-commit hook. It must be run manually.

**6. Associated Endpoints or Functions:**
*   This is a developer tooling feature and has no API endpoints.
*   Key Script: `scripts/linter.py`
*   Configuration: `scripts/doc-lint-rules.yml`

**7. Inputs:**
*   Verification Mode: Reads changed file paths from Git (or from a file with `--from-file`).
*   Logging Mode: Takes string inputs from the command line (e.g., `--summary`).

**8. Outputs:**
*   Verification Mode: Prints success or failure messages to the console.
*   Logging Mode: Modifies the three log files in `project/logs/`.

**9. Dependencies:**
*   External Libraries: `pyyaml`

**10. Testing & Validation Notes:**
*   The workflow is validated by its successful execution during the development process. The linter's failure on non-compliant changes and the successful update of logs serve as validation.

**11. Related Documentation:**
*   `AGENTS.md` (provides instructions on using the tool)
*   `api/docs/manuals/API_DEVELOPER_GUIDE.md` (documents the workflow for contributors)
*   `project/PROJECT_REGISTRY.md` (registers the script and this spec)
*   `project/PID.md` (incorporates the workflow into project controls)
