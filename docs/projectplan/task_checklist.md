# Apply the Task Execution Checklist from docs/projectplan/task_checklist.md, ensuring all applicable points are fully covered for this task, including documentation updates across all `.md` files outside excluded directories.


# Task Execution Checklist

**Purpose**
This checklist must be followed for *every* development task before it is marked complete. It ensures security-by-design, privacy compliance, documentation maintenance, testing discipline, and professional code quality.

---

## 1. Security
- Review code changes for **security risks**: injection vulnerabilities, data leaks, improper authentication, unsafe file handling, privilege escalation.
- Ensure **admin API key handling** follows `docs/projectplan/admin_api_key_mitigation.md`.
- Confirm **least-privilege principle** is applied for endpoints, data access, and dependencies.
- Add/update **`docs/projectplan/security.md`** if any new security considerations arise.

## 2. Privacy
- Review code changes for **privacy compliance** (GDPR, CCPA, or applicable regulations).
- Confirm sensitive data is **minimized**, **encrypted** where needed, and **not logged** in plain text.
- Implement and enforce **privacy-by-design principles** in new features.
- Capture explicit **user consent** where applicable.
- Implement RBAC and access control for personal data.
- Extend audit logging for all personal data access and changes.
- Support user rights: data export, correction, and deletion.
- Update **`docs/projectplan/privacy_compliance.md`** with any new privacy impacts and compliance steps.

## 3. Documentation
- Update **all relevant documentation** (`*.md` files across the project, excluding zotify/ directory), reviewing filenames and contents to verify updates are consistent with task scope.
- This includes but is not limited to HLD, LLD, roadmaps, guides, capability audits, changelogs, and project plans.
- Add a **CHANGELOG** entry reflecting the version bump and task summary.
- Generate and save a **Task Completion Report** in `docs/projectplan/reports/` for every major task completion.
- Update `reports/README.md` with an index of new reports.
- Link relevant reports in changelogs or documentation as appropriate.

## 4. Tests
- Write **unit tests** for new or changed logic.
- Update **integration tests** to reflect new API behavior.
- Ensure **all tests pass** locally and in CI pipelines.
- For security or privacy-sensitive features, write **negative tests** covering invalid or malicious inputs.
- Confirm test coverage is sufficient to protect critical code paths.

## 5. Code Quality and Code Review
- Follow established **naming conventions**, project architecture, and folder structure.
- Maintain strict **modularity** — no leaking of unrelated concerns across layers.
- Ensure **type hints** and comprehensive **docstrings** are accurate and clear.
- Write **clean, readable, idiomatic code** consistent with project language and style.
- Avoid unnecessary complexity or premature optimization but remove obvious inefficiencies or anti-patterns.
- **Review for security and safety** beyond functionality—identify unsafe patterns or risky operations.
- Ensure **proper error handling and input validation** throughout.
- Use **efficient algorithms and data structures** appropriate for the task.
- Run and pass **automated formatting, linting, and static analysis** tools to catch common issues.
- Conduct a **manual code review focused on maintainability, readability, and technical debt**.
- Refactor to improve clarity and reduce duplication or fragility.
- Verify **dependencies are minimal, necessary, and up-to-date**.
- Confirm **test coverage** adequately covers complex or critical paths.

## 6. Automation and Process Compliance
- Confirm **automated checks** (linting, security scans, documentation build/tests) run successfully on this code.
- Confirm the task complies with the **branching and release process** if fully automated as part of this task.
- Include explicit review or approval steps (code reviews, security/privacy signoffs) where automatable as part of the task workflow.

---

**Enforcement:**
No task is considered complete unless *all* applicable checklist items have been addressed.
This file is authoritative and version-controlled.
