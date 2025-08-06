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
- Update relevant guides (`developer_guide.md`, `operator_guide.md`) for new features.
- Add a **CHANGELOG** entry for the version bump.

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
