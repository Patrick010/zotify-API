# Low-Level Design (LLD) – 18-Step Refactor Plan

## Purpose
This LLD describes the specific work items for the current 18-step service-layer refactor, with detailed guidance per step to ensure uniformity and completeness.

## Refactor Standards
For each subsystem:
- Move business logic from `routes/` to `services/` as `<name>_service.py`.
- Create matching Pydantic schemas in `schemas/<name>.py`.
- Use FastAPI dependency injection for services/config/external APIs.
- Unit tests for the service layer go in `tests/unit/test_<name>_service.py`.
- Integration tests in `tests/test_<name>.py` must be updated accordingly.
- Documentation under `docs/` must be updated (API reference, developer guides, examples, CHANGELOG).

## Step Breakdown (Completed → Remaining)
### Completed:
1. Search subsystem → Service layer
2. Sync subsystem → Service layer
3. Config subsystem → Service layer
4. Playlists subsystem → Service layer
5. Tracks subsystem → Service layer
6. Downloads subsystem → Service layer
7. Logging subsystem → Service layer
8. Cache subsystem → Service layer
9. Network subsystem → Service layer
10. Metadata subsystem → Service layer
11. Playlists subsystem → Service layer

### Remaining:
12. Step 15: Authentication & Admin Controls
13. Step 16: Spotify Integration Refinement
14. Step 17: System Info & Health Endpoints
15. Step 18: Final QA Pass & Cleanup

---

## Step Template (to be used for all remaining steps)
### 1. Scope
- Extract business logic from routes to service file.
- Create/extend schema file with Pydantic models.
- Apply DI for dependencies.
- Remove all business logic from routes.

### 2. Testing
- Unit tests for all service methods.
- Integration tests for all route endpoints.
- Coverage for success, failure, edge cases.

### 3. Documentation
- Update **all relevant docs in `docs/`**:
  - API reference pages for request/response formats.
  - Developer guides showing usage.
  - Example API calls/responses.
  - Changelog entry for new version.

### 4. Deliverables
- Green test suite (`pytest --maxfail=1 --disable-warnings -q`).
- Commit with clear message referencing step number.
- Summary of changes for service file, schema, route, tests, docs.

### 5. Security
A comprehensive overview of the security architecture, principles, and roadmap for the Zotify API project is available in the [Zotify API Security](./security.md) document. This document serves as the definitive security reference for the project.

---

## Security Roadmap

### Phase 1: Foundations (Current)
- **Policy and Documentation:** Establish a formal security policy and create comprehensive security documentation.
- **Admin API Key Mitigation:** Replace the static admin API key with a dynamic, auto-generated key system.
- **Development Environment Security:** Ensure that development and testing environments are configured securely.

### Phase 2: Authentication & Secrets Management
- **OAuth2:** Implement OAuth2 for user-level authentication and authorization.
- **2FA (Two-Factor Authentication):** Add support for 2FA to provide an extra layer of security for user accounts.
- **Secret Rotation:** Implement a mechanism for automatically rotating secrets, such as the admin API key and database credentials.

### Phase 3: Monitoring & Protection
- **Audit Logging:** Implement a comprehensive audit logging system to track all security-sensitive events.
- **TLS Hardening:** Harden the TLS configuration to protect against common attacks.
- **Web Application Firewall (WAF):** Deploy a WAF to protect the API from common web application attacks.

### Phase 4: Documentation & Compliance
- **Security Guides:** Create detailed security guides for developers and operators.
- **Security Audits:** Conduct regular security audits to identify and address vulnerabilities.
- **Compliance:** Ensure that the API complies with all relevant security standards and regulations.

## Multi-Phase Plan Beyond Step 18
### Phase 1 — Service Layer Completion (Steps 1–18)
Goal: All subsystems fully modular, testable, documented.

### Phase 2 — Core Enhancements
- Implement JWT-based authentication.
- Add role-based access control for admin endpoints.
- Enhance Spotify API integration (full feature parity).

### Phase 3 — Performance & Scalability
- Add Redis caching for metadata & search.
- Async DB operations.
- Pagination optimizations.

### Phase 4 — Developer & CI/CD Improvements
- Add codegen for API docs.
- Lint/test in CI with coverage thresholds.
- PR doc-update enforcement.

### Phase 5 — Release Candidate
- Freeze features.
- Full regression test.
- Publish docs & changelog for v1.0.0.
