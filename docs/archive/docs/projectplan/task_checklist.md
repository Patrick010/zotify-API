# Apply the Task Execution Checklist from docs/projectplan/task_checklist.md, ensuring all applicable points are fully covered for this task, including documentation updates across all `.md` files outside excluded directories.


# Task Execution Checklist

**Purpose**
This checklist must be followed for *every* development task before it is marked complete. It ensures security-by-design, privacy compliance, documentation maintenance, testing discipline, and overall project hygiene.

---

## 1. Security
- Review code changes for **security risks**: injection, data leaks, improper authentication, unsafe file handling.
- Ensure **admin API key handling** complies with `docs/projectplan/admin_api_key_mitigation.md`.
- Confirm **least-privilege principle** is applied for endpoints, data access, and dependencies.
- Add or update **`docs/projectplan/security.md`** with any new security considerations.
- Verify any new dependencies or third-party components are vetted for security and properly licensed.

## 2. Privacy
- Review code changes for **privacy compliance** (GDPR, CCPA, or other applicable regulations).
- Confirm sensitive data is **minimized**, **encrypted** where needed, and **never logged in plain text**.
- Update **`docs/projectplan/privacy_compliance.md`** reflecting new privacy impacts and controls.
- Enforce user data rights: consent capture, data export, deletion, correction, and withdrawal mechanisms.
- Extend audit logging to track all personal data access and changes securely.
- Integrate privacy by design and default into the task's implementation.

## 3. Documentation — **Mandatory & Verifiable**

The task is **not complete** until every item below is satisfied and evidence is committed.

- **HLD & LLD**:
  - Update or create high-level and low-level design docs if implementation deviates from specs.
  - Include clear architectural change summaries.

- **Roadmap**:
  - Update `docs/roadmap.md` or equivalent if timelines, scope, or priorities change.

- **Audit References**:
  - Update relevant audit documents (e.g., `docs/projectplan/spotify_capability_audit.md`) if impacted.

- **User & Operator Guides**:
  - Update `developer_guide.md`, `operator_guide.md`, and related manuals for all functional changes, including API examples.

- **CHANGELOG**:
  - Add entries reflecting **all** functional changes: new/modified/removed endpoints, param changes, behavioral changes.

- **Task Completion Report**:
  - Produce a detailed report in `docs/projectplan/reports/<taskname>.md` that includes:
    - Summary of code and architectural changes.
    - **Documentation review log**: A table listing every file from the Documentation Review File List with a “Changed” or “No Change” mark plus commit references.
    - Explicit statement on API documentation updates.

- **Reports Index**:
  - Update `docs/projectplan/reports/README.md` to reference the new report.

- **Full `.md` File Sweep**:
  - **Carefully review every file on the Documentation Review File List for needed updates** related to the task.
  - Apply updates wherever necessary.
  - Mark each file in the documentation review log regardless of change status.

- **Functional Change Documentation**:
  - Document all functional changes in every relevant doc: API reference, developer/operator guides, README if user-facing.
  - Include before/after request/response examples and behavior notes.

- **Verification**:
  - Task is incomplete without all above deliverables committed and verified.

---

### Documentation Review File List
*(Add new `.md` files here as they appear. Do not remove existing entries.)*

./README.md
./api/docs/CHANGELOG.md
./api/docs/CONTRIBUTING.md
./api/docs/DATABASE.md
./api/docs/INSTALLATION.md
./api/docs/MANUAL.md
./api/docs/full_api_reference.md
./docs/INTEGRATION_CHECKLIST.md
./docs/developer_guide.md
./docs/operator_guide.md
./docs/roadmap.md
./docs/zotify-api-manual.md
./docs/projectplan/HLD_Zotify_API.md
./docs/projectplan/LLD_18step_plan_Zotify_API.md
./docs/projectplan/admin_api_key_mitigation.md
./docs/projectplan/admin_api_key_security_risk.md
./docs/projectplan/doc_maintenance.md
./docs/projectplan/next_steps_and_phases.md
./docs/projectplan/privacy_compliance.md
./docs/projectplan/roadmap.md
./docs/projectplan/security.md
./docs/projectplan/spotify_capability_audit.md
./docs/projectplan/spotify_fullstack_capability_blueprint.md
./docs/projectplan/spotify_gap_alignment_report.md
./docs/projectplan/task_checklist.md
./docs/projectplan/reports/20250807-doc-clarification-completion-report.md
./docs/projectplan/reports/20250807-spotify-blueprint-completion-report.md
./docs/projectplan/reports/20250808-comprehensive-auth-and-docs-update-report.md
./docs/projectplan/reports/20250808-oauth-unification-completion-report.md
./docs/projectplan/reports/20250809-api-endpoints-completion-report.md
./docs/projectplan/reports/20250809-phase5-endpoint-refactor-report.md
./docs/projectplan/reports/README.md
./docs/snitch/PHASE_2_SECURE_CALLBACK.md
./docs/snitch/TEST_RUNBOOK.md
./docs/snitch/phase5-ipc.md
./snitch/README.md
./snitch/docs/INSTALLATION.md
./snitch/docs/MILESTONES.md
./snitch/docs/MODULES.md
./snitch/docs/PHASES.md
./snitch/docs/PROJECT_PLAN.md
./snitch/docs/ROADMAP.md
./snitch/docs/STATUS.md
./snitch/docs/TASKS.md
./snitch/docs/TEST_RUNBOOK.md


## 4. Tests
- Write or update **unit tests** covering all new or changed logic, including edge cases and failure modes.
- Update **integration tests** to reflect new API endpoints, flows, or behavioral changes.
- Ensure **all tests pass** in continuous integration (CI) and locally before marking task complete.
- For security- or privacy-sensitive features, write **negative tests** simulating invalid inputs, unauthorized access, or malformed data.
- Automate running linting, static analysis, security scans, and documentation build tests as part of CI where applicable.

## 5. Code Quality
- Follow established **naming conventions**, directory structures, and coding style guides strictly.
- Maintain strict **modularity** — separate concerns cleanly, avoid cross-layer leakage (e.g., CLI logic leaking into API layer).
- Ensure complete and correct **type hints** and **docstrings** for all functions, classes, and modules.
- Perform **code reviews** with a focus on readability, maintainability, performance, and security.
- Use automated **linters** and **formatters** to enforce consistent style.
- Where feasible, use static code analysis tools to detect potential bugs or anti-patterns.
- Consider efficiency, scalability, and resource usage when writing or modifying code.
- Refactor legacy or autogenerated code as needed to meet these quality standards.

## 6. Automation and Workflow
- Integrate **explicit approval steps** (code reviews, security/privacy sign-offs) if your project workflow requires them.
- Include **automated checks** like linting, security scans, and documentation builds as part of task completion validation.
- Follow a **clear branching and release process** if it can be fully automated as part of the task execution.
- If the task is fully automatable and no manual review is needed, document this clearly and proceed with direct commits/pushes accordingly.

---

**Enforcement:**
No task is considered complete unless all applicable checklist items have been addressed. This file is authoritative and version-controlled.

---

### Notes on Privacy Compliance (Integrated)
Privacy compliance is an integral part of every task, not a separate addendum. Ensure:
- User consent is captured and stored where relevant.
- API endpoints exposing personal data enforce RBAC and access controls.
- Data minimization, encryption, and audit logging are applied consistently.
- User rights such as data export, deletion, and correction are implemented and tested.
- All privacy-related documentation is updated as part of normal doc maintenance.

---

**Usage:**
Include the full content of this checklist as part of your prompt or task instructions to ensure all aspects of security, privacy, documentation, testing, and code quality are covered before task completion.
