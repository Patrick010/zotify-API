# Audit Phase 5: Repository Organization and Linter Enhancement

**Date:** 2025-08-27
---
### Task: Relocate Linter Config and Implement Conditional Linter

*   **Reason & Goal:** Based on user feedback, the `lint-rules.yml` file should be located in `project/` for better organization. This task is to implement the conditional linter with the rules file in the correct path.
*   **Status:** 📝 In Progress
*   **NOTE on Environment:** The agent's `git` environment is persistently corrupted and stuck in a "detached HEAD" state that multiple `reset_all` calls could not fix. All file modifications are being made on the filesystem directly. Testing will be performed via workarounds.
*   **Summary of Activities:**
    *   [ ] Create `project/lint-rules.yml` to store the conditional rules.
    *   [ ] Update `scripts/lint-docs.py` to parse the YAML file from its new location and enforce the rules.
    *   [ ] Manually test the new linter to ensure it functions as expected.
*   **Outcome:** TBD.
