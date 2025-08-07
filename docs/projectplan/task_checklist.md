# Task Execution Checklist

**Purpose**
This checklist must be followed for *every* development task before it is marked complete. It ensures security-by-design, privacy compliance, documentation maintenance, and testing discipline.

---

## 1. Security
- Review code changes for **security risks** (injection, data leaks, improper authentication, unsafe file handling).
- Ensure **admin API key handling** follows `docs/projectplan/admin_api_key_mitigation.md`.
- Confirm **least-privilege principle** is applied for endpoints, data access, and dependencies.
- Add/update **`docs/projectplan/security.md`** if any new security considerations arise.

## 2. Privacy
- Review code changes for **privacy compliance** (GDPR, CCPA, or applicable regulations).
- Confirm sensitive data is **minimized**, **encrypted** where needed, and **not logged** in plain text.
- Update **`docs/projectplan/privacy_compliance.md`** with any new privacy impacts.

## 3. Documentation
- Update **HLD** and **LLD** if the design or implementation deviates from current specs.
- Update **roadmap.md** if this affects timelines, scope, or priorities.
- Reference the **Spotify Capability Audit** (`docs/projectplan/spotify_capability_audit.md`) for any tasks related to Spotify integration.
- Update relevant guides (`developer_guide.md`, `operator_guide.md`) for new features.
- Add a **CHANGELOG** entry for the version bump.
- Generate and save a **Task Completion Report** in `docs/projectplan/reports/` for every major task completion.
- Update the `reports/README.md` with an index of new reports.
- Link relevant reports in changelogs or documentation as appropriate.

## 4. Tests
- Write **unit tests** for new or changed logic.
- Update **integration tests** to reflect new API behavior.
- Ensure **all tests pass** in CI and locally.
- For features with security or privacy implications, write **negative tests** (invalid credentials, malicious inputs, etc.).

## 5. Code Quality
- Follow established **naming conventions** and folder structure.
- Maintain strict **modularity** — no leaking CLI code into API layer.
- Ensure **type hints** and docstrings are complete and correct.

---

**Enforcement:**
No task is considered complete unless all applicable checklist items have been addressed.
This file is authoritative and version-controlled.

### Step 19 — Privacy Compliance Integration

- Implement explicit user consent capture and storage.
- Add user privacy endpoints:
  - GET /privacy/data (export user data)
  - DELETE /privacy/data (delete user data)
- Enforce data minimization in storage and API responses.
- Implement RBAC and access control for personal data.
- Extend audit logging for all personal data access and changes.
- Support user rights (data correction, consent withdrawal).
- Ensure all API endpoints comply with GDPR and the project’s User Privacy Compliance Statement, including:
  - Lawful and transparent processing.
  - Privacy by design and default principles.
  - Regular data protection impact assessments.
- Perform security reviews and patch identified issues.
- Write unit and integration tests covering privacy features and GDPR compliance.
- Update all relevant documentation with privacy compliance info.
