# Zotify API Development Roadmap (Updated)

## Phase 1 — Foundation & Structure ✅ (Completed)

- **Setup project structure**
  - API code isolated under `/api` separate from core CLI.
  - Clear folder separation for routes, services, schemas, tests, docs.
- **Define Pydantic models** for all request/response payloads, even if initially minimal.
- **FastAPI app & placeholder routers** created for all major feature areas:
  - Search
  - Playlists
  - Downloads
  - Metadata
  - Cache
  - Sync
  - User & Auth
- **Basic logging, error handling, and config management** established.
- **HLD and LLD initialized** in `docs/projectplan/`, tracking the 18-step plan.

---

## Phase 2 — Core Integration & Service Layer ✅ (Completed)

- **`/api/services`** folder created for all business logic.
- **Spotify API client service (stubbed)**:
  - Authentication placeholders.
  - Method placeholders for search, playlist, and track retrieval.
- **Route → service wiring**:
  - Search endpoints call Spotify client stub.
  - Playlist endpoints scaffolded.
- **CLI wrappers**:
  - Stubs for download and metadata management.
- **Error handling** and consistent response shaping.
- **Dependency Injection**:
  - Used across all services for easy test overrides.

---

## Phase 3 — Authentication, Security & Privacy (In Progress)

- **Authentication strategy**:
  - Admin API key system implemented.
  - Dynamic key generation on startup with secure storage.
  - `.gitignore` protects key file.
  - Operator and developer documentation created.
- **Security-by-Design checklist**:
  - Added to all future prompts and steps.
  - Reviewed for each subsystem refactor (playlists, cache, etc.).
- **Planned additions**:
  - OAuth (Spotify & possibly other providers) in later phases.
  - Role-based access control (RBAC) for multi-user scenarios.
  - Rate limiting and abuse prevention.
  - Secure credential storage (encrypted at rest).
  - HTTPS/TLS enforcement in production.
- **Privacy compliance**:
  - `docs/projectplan/privacy_compliance.md` created.
  - GDPR/CCPA principles noted for user data handling.
  - Added as **Step 19** in the 18-step plan.
- **Testing**:
  - Security features covered by unit and integration tests.

---

## Phase 4 — Feature Completion & Polishing (Upcoming)

- Finish remaining endpoints and services:
  - Cache stats & clearing (with admin protection).
  - Sync operations.
  - Metadata management.
  - User profile and preference management.
- **Enhance validation & sanitization** for all inputs.
- Add **audit logging** for sensitive actions.
- Implement **metrics & monitoring hooks**.
- Expand API documentation with request/response examples and error codes.

---

## Phase 5 — Testing & Deployment

- 100% unit test coverage for all core services.
- Integration tests for all protected and public endpoints.
- Automated CI testing with Ruff, MyPy, Bandit, and Pytest.
- Docker image build & deploy scripts.
- Load testing and performance tuning.

---

## Phase 6 — Client & Extensibility Support

- Example clients (CLI, web UI).
- API versioning.
- Extension hooks for new modules.
- External developer guide for API consumption.

---

## Ongoing Maintenance

- Monitor logs, errors, and usage.
- Apply dependency updates regularly.
- Patch security issues quickly.
- Continue following **security-by-design** and **privacy-by-design** principles.

---

## Embedded Process Requirements

- **Every step** must:
  - Update `docs/projectplan/HLD.md` and `LLD_18step_plan_Zotify_API.md`.
  - Update or create relevant security/privacy documentation.
  - Review security checklist before marking as complete.
  - Add/Update unit & integration tests for all new or changed code.
- **No production deployment** without:
  - Privacy compliance checks.
  - Security validation pass.
  - Reviewed and signed-off HLD/LLD changes.
