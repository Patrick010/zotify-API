# HLD/LLD Traceability Matrix

**Purpose:** This document tracks the alignment between the features and architectural principles described in the `HIGH_LEVEL_DESIGN.md` and `LOW_LEVEL_DESIGN.md` documents and the actual state of the codebase.

| Feature / Component | Exists? | Matches Design? | Priority | Notes on Deviations & Context |
| :--- | :--- | :--- | :--- | :--- |
| **Authentication & Authorization** | | | | |
| Admin Endpoint Security | Y | Y | High | **Context:** The design documents (specifically `security.md`) have been updated to reflect the current reality, which is that security is handled by a static admin API key. **Gap:** None. The aspirational features are now documented as future enhancements. |
| JWT for API Authentication | N | Y (Deferred) | Low | **Status:** Planned — Deferred. This feature is tracked in project/FUTURE_ENHANCEMENTS.md. It will not appear in HLD/LLD until promoted to an active roadmap phase. |
| Role-Based Access Control (RBAC) | N | N | Low | **Context:** Planned for multi-user environments, but current model is single-user. Deferred until multi-user support is prioritized. |
| **Spotify Integration** | | | | |
| OAuth2 for Spotify Integration | Y | Y (partial) | Medium | **Context:** The design documents (`LOW_LEVEL_DESIGN.md`) have been updated to reflect the current reality, which is that the integration supports authentication and full playlist CRUD, but not write-sync or full library management. **Gap:** None from a documentation perspective. The unimplemented features are now tracked in `FUTURE_ENHANCEMENTS.md`. |
| Webhook/Event System | N | Y (Deferred) | Low | **Status:** Planned — Deferred. This feature is tracked in `project/FUTURE_ENHANCEMENTS.md`. It will not appear in HLD/LLD until promoted to an active roadmap phase. |
| **Core Subsystems** | | | | |
| Provider Abstraction Layer | Y | Y | Critical | **Context:** A new provider-agnostic abstraction layer has been implemented. Spotify has been refactored into a connector for this layer. **Gap:** None. |
| Unified Database System | Y | Y | Critical | **Context:** A new backend-agnostic database layer using SQLAlchemy has been implemented. It handles all data persistence for the application. **Gap:** None. |
| Downloads Subsystem | Y | Y | High | **Context:** The download queue is now managed by the unified database system, making it fully persistent and production-ready. **Gap:** None. |
| Spotify Integration | Y | Y | Medium | **Context:** The storage for OAuth tokens and synced playlists has been migrated to the unified database system. **Gap:** None. |
| System Info & Health Endpoints | Y | Y | Medium | **Context:** The design documents (`LOW_LEVEL_DESIGN.md`) have been updated to reflect the current reality, which is that only basic `/uptime` and `/env` endpoints are implemented. **Gap:** None. The more advanced checks are now documented as future enhancements. |
| Error Handling & Logging | Y | Y | Medium | **Context:** The design documents (`LOW_LEVEL_DESIGN.md`) have been updated to reflect the current reality, which is that error handling and logging are implemented in an ad-hoc, inconsistent manner. **Gap:** None. The aspirational features (consistent schemas, etc.) are now documented as future enhancements. |
| Config Management via API | Y | Y | Medium | **Context:** The design documents (`LOW_LEVEL_DESIGN.md`) have been updated to reflect the current reality: there are two config systems. Core settings are startup-only, but a separate `ConfigService` handles mutable application settings at runtime via a JSON file and the `/api/config` endpoints. The aspirational goal of a single, unified config system is now tracked in `FUTURE_ENHANCEMENTS.md`. **Gap:** None. |
| **General Processes & Security** | | | | |
| Documentation Practices | Y | Y | High | **Context:** The `HIGH_LEVEL_DESIGN.md` has been updated to reflect the current, pragmatic "living documentation" process. The aspirational "docs-first" approach is preserved as a potential future-phase goal. **Gap:** None. |
| Security Enhancements | N | Y (Deferred) | Low | **Status:** Planned — Deferred. This feature is tracked in project/FUTURE_ENHANCEMENTS.md. |
| Test Coverage > 90% & Gating | Y | Y | Medium | **Context:** Test coverage has been increased to 90.01%. A new CI workflow at `.github/workflows/ci.yml` enforces a minimum of 85% coverage on all pull requests. **Gap:** None. |
