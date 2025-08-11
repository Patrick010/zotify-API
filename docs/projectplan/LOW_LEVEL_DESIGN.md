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
12. User Profiles and Preferences → Service layer
13. Notifications Subsystem → Service layer

14. Step 15: Authentication & Admin Controls ✅ (Completed)
15. Step 16: Spotify Integration Refinement ✅ (Completed)
16. Step 17: System Info & Health Endpoints ✅ (Completed)
17. Step 18: Final QA Pass & Cleanup ✅ (Completed)

### All steps completed.

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
A comprehensive overview of the security architecture, principles, and roadmap for the Zotify API project is available in the [Zotify API Security](./SECURITY.md) document. This document serves as the definitive security reference for the project.

---

### Task Workflow / Checklist Enforcement

Every task described in this LLD must be executed in compliance with the Task Execution Checklist at `docs/projectplan/task_checklist.md`. This ensures that implementation details remain aligned with high-level requirements, and that tests, documentation, security and privacy checks are performed before completion.

Any deviation from the LLD requires an explicit update to both the LLD and HLD and must reference the checklist steps that were followed.

## Security Roadmap

> Note: This roadmap outlines high-level security goals. For a more detailed and up-to-date list of planned features and product vision, please see the [`FUTURE_ENHANCEMENTS.md`](./FUTURE_ENHANCEMENTS.md) document.

### Phase 1: Foundations (Current)
- **Policy and Documentation:** Establish a formal security policy and create comprehensive security documentation.
- **Admin API Key Mitigation:** Replace the static admin API key with a dynamic, auto-generated key system.
- **Development Environment Security:** Ensure that development and testing environments are configured securely.

### Phase 3: Authentication, Security & Privacy (In Progress)
- **Spotify Capability Audit:** Audit the Spotify capabilities available through the Zotify stack to inform future development. This is a blocking task for Phase 4.

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

> Note: This multi-phase plan represents a high-level sketch of potential future work. For a more detailed and up-to-date list of planned features and product vision, please see the [`FUTURE_ENHANCEMENTS.md`](./FUTURE_ENHANCEMENTS.md) document.

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

---

## Spotify Integration Design

**Goal:** To provide a robust integration with the Spotify Web API for authentication, playlist management, and library synchronization.

**Current Implementation:**
The current integration provides the following capabilities:
- **Authentication:** A full OAuth2 PKCE flow for authenticating the application with a user's Spotify account.
- **Playlist Management:** Full CRUD (Create, Read, Update, Delete) functionality for user playlists and the tracks within them. This is exposed via a comprehensive set of API endpoints.
- **Read-Only Sync:** A one-way synchronization feature (`/sync_playlists`) that fetches all of a user's playlists from Spotify and saves them to a local file.

**Future Enhancements:**
- As noted in the `TRACEABILITY_MATRIX.md`, the full design for this subsystem includes more advanced synchronization and library management features. These are now tracked in the [`FUTURE_ENHANCEMENTS.md`](./FUTURE_ENHANCEMENTS.md) document and include:
  - Two-way ("write") synchronization for playlists.
  - Full library management (saved albums, liked songs, etc.).

---

## Error Handling & Logging Design

**Goal:** To document the current, ad-hoc approach to error handling and logging in the application.

**Current Implementation - Error Handling:**
- **API Layer:** Errors are returned to the client using FastAPI's `HTTPException`.
- **Status Codes & Messages:** The use of HTTP status codes and the content of the `detail` messages are inconsistent across different endpoints. Some errors return a generic `500` status, while others use more specific codes like `401`, `404`, or `503`. Detail messages are often the direct string representation of an internal exception.
- **Service Layer:** Some services, like `spoti_client.py`, raise `HTTPException`s directly, coupling them to the web framework. Other services may raise standard Python exceptions that are caught in the route layer.

**Current Implementation - Logging:**
- **Framework:** The standard Python `logging` module is used.
- **Configuration:** A basic configuration is applied at startup via `logging.basicConfig(level=logging.INFO)`, which logs all messages of `INFO` level and above to the console with a default format.
- **Usage:** Loggers are instantiated per-module using `logging.getLogger(__name__)`. Naming conventions for the logger instance (`log` vs. `logger`) are inconsistent.

**Future Enhancements:**
- A comprehensive, standardized approach to error handling and logging is a required future enhancement. This includes creating a unified error response schema, refactoring services to use domain-specific exceptions, and establishing consistent logging formats. These items are tracked in the [`FUTURE_ENHANCEMENTS.md`](./FUTURE_ENHANCEMENTS.md) document.

---

## System Info & Health Endpoints Design

**Goal:** Provide basic endpoints for monitoring the system's status and environment.

**API Endpoints (`routes/system.py`):**
- `GET /api/system/uptime`: Returns the system's uptime.
- `GET /api/system/env`: Returns a list of environment variables.

**Service Layer (`services/system_service.py`):**
- The service provides simple methods to retrieve system information, currently limited to uptime and environment variables.

**Current Implementation:**
- The existing implementation provides basic information through the `/uptime` and `/env` endpoints.

**Future Enhancements:**
- As noted in the `TRACEABILITY_MATRIX.md`, the full design for this subsystem includes more comprehensive checks. These are now tracked in the [`FUTURE_ENHANCEMENTS.md`](./FUTURE_ENHANCEMENTS.md) document and include:
  - Process stats
  - Disk and network health
  - Dependency checks

---

## Downloads Subsystem Design

**Goal:** Implement a functional download management system that allows users to queue tracks for download and check the status of the queue.

**API Endpoints (`routes/downloads.py`):**
- `POST /api/download`: Accepts a list of track IDs, creates a download job for each, and adds them to a queue. Returns a job ID for tracking.
- `GET /api/downloads/status`: Returns the status of all jobs in the queue (pending, in-progress, completed, failed).
- `POST /api/downloads/retry`: Retries all failed jobs in the queue.
- `POST /api/downloads/process`: Manually processes one job from the queue.

**Service Layer (`services/download_service.py`):**
- The service uses a new `downloads_db.py` module to manage a persistent download queue in a SQLite database (`api/storage/downloads.db`).
- **`add_downloads_to_queue(track_ids: list)`**: Creates `DownloadJob` objects and adds them to the database.
- **`get_queue_status()`**: Retrieves all jobs from the database and returns a summary of their status.
- **`process_download_queue()`**: Fetches the oldest pending job from the database, simulates processing, and updates its status to `completed` or `failed`.
- **`retry_failed_jobs()`**: Resets the status of all failed jobs in the database to `pending`.

**Data Models (`schemas/downloads.py`):**
- **`DownloadJobStatus` (Enum):** `PENDING`, `IN_PROGRESS`, `COMPLETED`, `FAILED`.
- **`DownloadJob` (Pydantic Model):**
  - `job_id: str` # JULES-NOTE: To be implemented as a UUIDv4 string.
  - `track_id: str`
  - `status: DownloadJobStatus`
  - `progress: Optional[float] = None` # JULES-NOTE: Placeholder for future progress reporting (e.g., 0.0 to 1.0).
  - `created_at: datetime`
  - `error_message: Optional[str] = None`
- **`DownloadQueueStatus` (Pydantic Model):**
  - `total_jobs: int`
  - `pending: int`
  - `completed: int`
  - `failed: int`
  - `jobs: List[DownloadJob]`

**Data Persistence:**
- The download queue is now persistent and will survive server restarts. All job data is stored in a dedicated SQLite database located at `api/storage/downloads.db`. This fulfills the requirement for a persistent job queue.

---

## Ongoing Maintenance
All development tasks must follow the [Task Execution Checklist](./task_checklist.md) to ensure consistency, quality, and security.
