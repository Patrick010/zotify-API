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

### Remaining:
11. Step 15: Authentication & Admin Controls
12. Step 16: Spotify Integration Refinement
13. Step 17: System Info & Health Endpoints
14. Step 18: Final QA Pass & Cleanup

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

### 5. Admin API Key Usage and Risk Management
The current implementation uses a static admin API key for protecting administrative endpoints. This is a known security risk and is documented in the [Admin API Key Security Risk Analysis](./admin_api_key_security_risk.md) document.

**Implementation Details:**
- **Header Name:** `X-API-Key`
- **Configuration:** The API key is configured via the `ADMIN_API_KEY` environment variable.
- **Error Handling:**
  - If the `admin_api_key` is not configured, protected endpoints will return a `503 Service Unavailable` error.
  - If the key is configured but the header is missing or incorrect, a `401 Unauthorized` error is returned.
- **Test Mocking:** Tests use `monkeypatch` to set the `admin_api_key` in the settings for testing protected endpoints.

**Next Steps:**
Future phases of the project will replace the static admin API key with a more robust authentication mechanism, such as OAuth2 or JWT.

The security risk document and this section must be maintained alongside any future changes to authentication or admin key usage. Any changes related to authentication or this risk must also be documented in `docs/CHANGELOG.md`.

---

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
