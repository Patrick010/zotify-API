# HLD/LLD Traceability Matrix

**Purpose:** This document tracks the alignment between the features and architectural principles described in the `HIGH_LEVEL_DESIGN.md` and `LOW_LEVEL_DESIGN.md` documents and the actual state of the codebase.

| Feature / Component | Exists? | Matches Design? | Priority | Notes on Deviations & Context |
| :--- | :--- | :--- | :--- | :--- |
| **Authentication & Authorization** | | | | |
| Admin Endpoint Security | Y | Y | High | **Context:** The design documents (specifically `security.md`) have been updated to reflect the current reality, which is that security is handled by a static admin API key. **Gap:** None. The aspirational features are now documented as future enhancements. |
| JWT for API Authentication | N | N | Medium | **Context:** Core design requirement for user-level auth. Not implemented. |
| Role-Based Access Control (RBAC) | N | N | Low | **Context:** Planned for multi-user environments, but current model is single-user. Deferred until multi-user support is prioritized. |
| **Spotify Integration** | | | | |
| OAuth2 for Spotify Integration | Y | N | Medium | **Context:** Post-auth features were deferred to focus on a working auth flow first. **Gap:** Design aims for full CRUD/sync; write-sync and full library management are incomplete. |
| Webhook/Event System | N | N | Low | **Context:** Deferred as no downstream consumers exist yet. **Gap:** Design specifies an outbound event system for state changes (downloads, syncs) that is not implemented. |
| **Core Subsystems** | | | | |
| Downloads Subsystem | Y | Y (partial) | High | **Context:** The in-memory job queue is now functional, with logic to process jobs and update their status. **Gap:** The system still lacks a persistent job queue (e.g., using a database or Redis), which is required for production readiness. |
| System Info & Health Endpoints | Y | Y | Medium | **Context:** The design documents (`LOW_LEVEL_DESIGN.md`) have been updated to reflect the current reality, which is that only basic `/uptime` and `/env` endpoints are implemented. **Gap:** None. The more advanced checks are now documented as future enhancements. |
| Error Handling & Logging | Y | N | Medium | **Context:** Grew organically during iterative development without early enforcement. **Gap:** Design specifies consistent error schemas and audit trails; current implementation is inconsistent. |
| Config Management via API | N | N | Medium | **Context:** Deferred to avoid complexity while config schema was evolving. **Gap:** Design includes runtime config updates via API; current code only reads config at startup. |
| **General Processes & Security** | | | | |
| Documentation Practices | Y | N | High | **Context:** Docs lagged significantly during rapid development. **Gap:** Design mandates a docs-first workflow which was not followed. This is the focus of the current audit/realignment. |
| Security Enhancements | N | N | Medium | **Context:** Deferred as not critical for internal-only MVP. **Gap:** Features like secret rotation and TLS hardening are in the design but not implemented. |
| Test Coverage > 90% & Gating | N | N | Medium | **Context:** Basic tests exist, but coverage is not enforced in CI. **Gap:** HLD requires >90% coverage and CI gating, which is not implemented. |
