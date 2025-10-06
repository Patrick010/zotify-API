# Alignment Matrix (Living Document)

**Purpose:**
This document maintains a live mapping between strategic goals, design documents (HLD/LLD), implementation, and reference documentation. It is the single source of truth for project traceability and must be updated with every feature, refactor, or documentation change.

---

## 1. Roadmap to Execution Plan Traceability

| Roadmap Theme | Execution Phases | Deliverables / Notes |
|---|---|---|
| **Phase 1-5: Core Stability & Hardening** | Phases 0-5, 7, 11 | **Aligned.** These roadmap phases correspond to the foundational setup, core API implementation, developer tooling, and initial Spotify integration work. Phase 5 concluded with a major governance refactoring, which consolidated traceability documents and enhanced linter enforcement. |
| **Phase 6: Platform Extensibility** | Phase 8: Extensibility & Automation | **Aligned.** The roadmap theme maps directly to the corresponding execution phase. |
| **Phase 7: Snitch Module Hardening** | Phase 2 (Snitch Plan) | **Aligned.** The work is detailed in the `snitch/docs/PROJECT_PLAN.md`. |
| **Phase 8: Administrative & Fork-Specific Enhancements** | Phases 6 & 9 | **Aligned.** This roadmap theme groups the operational tasks for admin APIs and fork-specific features. |
| **Phase 9: Release Readiness** | Phase 10: Finalization & Release Readiness | **Aligned.** This roadmap theme maps directly to the final release readiness phase in the execution plan. |
| **Future Vision** | N/A | **Intentional Omission.** The "Future Vision" items are tracked in `FUTURE_ENHANCEMENTS.md`. |

---

## 2. Core System & Component Alignment

| Audit Ref | Feature / Component | Requirement ID | Status | HLD Reference | LLD Reference | Code Path(s) | Test Coverage | Documentation | Notes / Source Doc |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Core API Architecture** | | | | | | | | | |
| AR-001 | API Routes Layer | | ✅ | [Routes Layer](HIGH_LEVEL_DESIGN.md#hld-routes-layer) | [API Endpoint Baseline](LOW_LEVEL_DESIGN.md#lld-api-endpoint-baseline) | `api/src/zotify_api/routes/` | ✅ | `project/api/endpoints.yaml` | |
| AR-002 | Business Logic Service Layer | | ✅ | [Service Layer](HIGH_LEVEL_DESIGN.md#hld-service-layer) | `N/A` | `api/src/zotify_api/services/` | ✅ | `api/docs/reference/API_REFERENCE.md` | |
| AR-003 | Pydantic Schema Layer | | ✅ | [Schema Layer](HIGH_LEVEL_DESIGN.md#hld-schema-layer) | `N/A` | `api/src/zotify_api/schemas/` | ✅ | `api/docs/reference/API_REFERENCE.md` | |
| AR-004 | Unified Persistence (SQLAlchemy) | FEAT-ZOTIFY-DATABASE-01 | ✅ | [Persistence Layer](HIGH_LEVEL_DESIGN.md#hld-persistence-layer) | [Unified Database Architecture](LOW_LEVEL_DESIGN.md#lld-unified-database-architecture) | `api/src/zotify_api/database/`, `api/alembic/` | ✅ | `project/LOW_LEVEL_DESIGN.md#lld-unified-database-architecture` | Retrospectively aligned via [FEAT-ZOTIFY-DATABASE-01](BACKLOG.md#feat-zotify-database-01). |
| AR-005 | Provider Abstraction | SYS-04 | ✅ | [Provider Abstraction](HIGH_LEVEL_DESIGN.md#hld-provider-abstraction-layer) | [Provider Abstraction Layer](LOW_LEVEL_DESIGN.md#lld-provider-abstraction-layer) | `api/src/zotify_api/providers/` | N/A | `project/proposals/DYNAMIC_PLUGIN_PROPOSAL.md` | Provider model allows for extension. |
| AR-006 | Centralized Configuration | FE-09 | 🟡 | [Config Layer](HIGH_LEVEL_DESIGN.md#hld-config-layer) | [Configuration Management](LOW_LEVEL_DESIGN.md#lld-configuration-management) | `api/src/zotify_api/config.py`, `api/src/zotify_api/services/config_service.py` | 🔍 | `project/LOW_LEVEL_DESIGN.md#lld-configuration-management` | Dual system exists, not unified. |
| **API Routes & Services** | | | | | | | | | |
| AR-007 | Auth Routes & Provider-Agnostic Flow | SYS-07 | ✅ | [Auth Provider Interface](HIGH_LEVEL_DESIGN.md#hld-authentication-provider-interface) | [Spotify Integration Design](LOW_LEVEL_DESIGN.md#lld-spotify-integration-design) | `api/src/zotify_api/routes/auth.py`, `api/src/zotify_api/providers/` | ✅ | `project/api/endpoints.yaml` | Handles OAuth2 callbacks generically in the provider layer. |
| AR-008 | Cache Routes & Service | FEAT-ZOTIFY-CACHE-01 | ✅ | [Service Layer](HIGH_LEVEL_DESIGN.md#hld-service-layer) | [Cache Service](LOW_LEVEL_DESIGN.md#lld-cache-service) | `api/src/zotify_api/routes/cache.py`, `api/src/zotify_api/services/cache_service.py` | ✅ | `project/api/endpoints.yaml` | Retrospectively aligned via [FEAT-ZOTIFY-CACHE-01](BACKLOG.md#feat-zotify-cache-01). |
| AR-009 | Config Routes | FE-09 | 🟡 | [Config Layer](HIGH_LEVEL_DESIGN.md#hld-config-layer) | [Configuration Management](LOW_LEVEL_DESIGN.md#lld-configuration-management) | `api/src/zotify_api/routes/config.py` | ✅ | `project/api/endpoints.yaml` | |
| AR-010 | Downloads Routes & Service | UC-04 | 🟡 | `N/A` | [Downloads Subsystem Design](LOW_LEVEL_DESIGN.md#lld-downloads-subsystem-design) | `api/src/zotify_api/routes/downloads.py` | 🔍 | `project/api/endpoints.yaml` | Lacks automation and file management. |
| AR-011 | Network Routes & Service | FEAT-ZOTIFY-NETWORK-01 | ✅ | [Service Layer](HIGH_LEVEL_DESIGN.md#hld-service-layer) | [Network Service](LOW_LEVEL_DESIGN.md#lld-network-service) | `api/src/zotify_api/routes/network.py`, `api/src/zotify_api/services/network_service.py` | ✅ | `project/api/endpoints.yaml` | Retrospectively aligned via [FEAT-ZOTIFY-NETWORK-01](BACKLOG.md#feat-zotify-network-01). |
| AR-012 | Notifications Routes & Service | FEAT-ZOTIFY-NOTIFICATIONS-01 | ✅ | [Service Layer](HIGH_LEVEL_DESIGN.md#hld-service-layer) | [Notifications Service](LOW_LEVEL_DESIGN.md#lld-notifications-service) | `api/src/zotify_api/routes/notifications.py`, `api/src/zotify_api/services/notifications_service.py` | ✅ | `project/api/endpoints.yaml` | Retrospectively aligned via [FEAT-ZOTIFY-NOTIFICATIONS-01](BACKLOG.md#feat-zotify-notifications-01). |
| AR-013 | Playlists Routes & Service | FEAT-ZOTIFY-PLAYLISTS-01 | ✅ | [Service Layer](HIGH_LEVEL_DESIGN.md#hld-service-layer) | [Playlist Service](LOW_LEVEL_DESIGN.md#lld-playlist-service) | `api/src/zotify_api/routes/playlists.py`, `api/src/zotify_api/services/playlists_service.py` | ✅ | `project/api/endpoints.yaml` | Retrospectively aligned via [FEAT-ZOTIFY-PLAYLISTS-01](BACKLOG.md#feat-zotify-playlists-01). |
| AR-014 | Search Routes & Service | FEAT-ZOTIFY-SEARCH-01 | ✅ | [Service Layer](HIGH_LEVEL_DESIGN.md#hld-service-layer) | [Search Service](LOW_LEVEL_DESIGN.md#lld-search-service) | `api/src/zotify_api/routes/search.py`, `api/src/zotify_api/services/search.py` | ✅ | `project/api/endpoints.yaml` | Retrospectively aligned via [FEAT-ZOTIFY-SEARCH-01](BACKLOG.md#feat-zotify-search-01). |
| AR-015 | Sync Routes & Service | FEAT-ZOTIFY-SYNC-01 | ✅ | [Service Layer](HIGH_LEVEL_DESIGN.md#hld-service-layer) | [Sync Service](LOW_LEVEL_DESIGN.md#lld-sync-service) | `api/src/zotify_api/routes/sync.py`, `api/src/zotify_api/services/sync_service.py` | ✅ | `project/api/endpoints.yaml` | Retrospectively aligned via [FEAT-ZOTIFY-SYNC-01](BACKLOG.md#feat-zotify-sync-01). |
| AR-016 | System Routes & Health Checks | FE-08 | 🟡 | `N/A` | `N/A` | `api/src/zotify_api/routes/system.py` | 🔍 | `project/api/endpoints.yaml` | Only basic uptime/env endpoints exist. |
| AR-017 | Tracks Routes & Service | FEAT-ZOTIFY-TRACKS-01 | ✅ | [Service Layer](HIGH_LEVEL_DESIGN.md#hld-service-layer) | [Track Service](LOW_LEVEL_DESIGN.md#lld-track-service) | `api/src/zotify_api/routes/tracks.py`, `api/src/zotify_api/services/tracks_service.py` | ✅ | `project/api/endpoints.yaml` | Retrospectively aligned via [FEAT-ZOTIFY-TRACKS-01](BACKLOG.md#feat-zotify-tracks-01). |
| AR-018 | User Routes & Service | FEAT-ZOTIFY-USER-01 | ✅ | [Service Layer](HIGH_LEVEL_DESIGN.md#hld-service-layer) | [User Service](LOW_LEVEL_DESIGN.md#lld-user-service) | `api/src/zotify_api/routes/user.py`, `api/src/zotify_api/services/user_service.py` | ✅ | `project/api/endpoints.yaml` | Retrospectively aligned via [FEAT-ZOTIFY-USER-01](BACKLOG.md#feat-zotify-user-01). |
| AR-019 | Webhooks Routes & Service | FEAT-ZOTIFY-WEBHOOKS-01 | ✅ | [Service Layer](HIGH_LEVEL_DESIGN.md#hld-service-layer) | [Webhooks Service](LOW_LEVEL_DESIGN.md#lld-webhooks-service) | `api/src/zotify_api/routes/webhooks.py`, `api/src/zotify_api/services/webhooks.py` | ✅ | `project/api/endpoints.yaml` | Retrospectively aligned via [FEAT-ZOTIFY-WEBHOOKS-01](BACKLOG.md#feat-zotify-webhooks-01). |
| **Cross-Cutting Concerns** | | | | | | | | | |
| AR-021 | Generic Error Handling | FE-07 | ✅ | [Error Handling Layer](HIGH_LEVEL_DESIGN.md#hld-generic-error-handling-layer) | [Generic Error Handling Module](LOW_LEVEL_DESIGN.md#lld-generic-error-handling-module) | `api/src/zotify_api/core/error_handler/` | ✅ | `api/docs/system/ERROR_HANDLING_STRATEGY.md` | Centralized error handling module is complete and integrated. |
| AR-022 | Flexible Logging Framework | FE-07a | ✅ | [Logging Layer](HIGH_LEVEL_DESIGN.md#hld-logging-layer) | [Flexible Logging Framework](LOW_LEVEL_DESIGN.md#lld-flexible-logging-framework) | `api/src/zotify_api/core/logging_framework/` | ✅ | `api/docs/system/LOGGING_FRAMEWORK.md`, `docs/manuals/LOGGING_GUIDE.md` | Core framework is complete. |
| AR-023 | API Middleware | SYS-05 | ✅ | `N/A` | [API Middleware](LOW_LEVEL_DESIGN.md#lld-api-middleware) | `api/src/zotify_api/middleware/` | N/A | `project/LOW_LEVEL_DESIGN.md#lld-api-middleware` | Permissive CORS policy for Web UI. |
| **Supporting Modules** | | | | | | | | | |
| AR-024 | Gonk-TestUI | FEAT-ZOTIFY-GONK-01 | ✅ | [Supporting Modules](HIGH_LEVEL_DESIGN.md#hld-supporting-modules) | [Gonk-TestUI](LOW_LEVEL_DESIGN.md#lld-gonk-testui) | `Gonk/` | ✅ | `Gonk/GonkUI/README.md` | Retrospectively aligned via [FEAT-ZOTIFY-GONK-01](BACKLOG.md#feat-zotify-gonk-01). |
| AR-025 | Snitch | FEAT-ZOTIFY-SNITCH-01 | ✅ | [Supporting Modules](HIGH_LEVEL_DESIGN.md#hld-supporting-modules) | [Snitch](LOW_LEVEL_DESIGN.md#lld-snitch) | `snitch/` | ✅ | `snitch/docs/PROJECT_PLAN.md` | Retrospectively aligned via [FEAT-ZOTIFY-SNITCH-01](BACKLOG.md#feat-zotify-snitch-01). |
| **Infrastructure & Tooling** | | | | | | | | | |
| AR-026 | CI/CD Pipeline | | ✅ | [Deployment Model](HIGH_LEVEL_DESIGN.md#hld-deployment-model) | `N/A` | `.github/workflows/ci.yml` | | `project/CICD.md` | |
| AR-066 | Core Project Governance | FEAT-ZOTIFY-GOVERNANCE-01 | ✅ | [Doc Governance](HIGH_LEVEL_DESIGN.md#hld-documentation-governance) | [Ongoing Maintenance](LOW_LEVEL_DESIGN.md#lld-ongoing-maintenance) | `AGENTS.md`, `project/QA_GOVERNANCE.md`, `scripts/linter.py`, `scripts/repo_inventory_and_governance.py` | N/A | `AGENTS.md`, `project/QA_GOVERNANCE.md` | Consolidated governance framework. Retrospectively aligned via [FEAT-ZOTIFY-GOVERNANCE-01](BACKLOG.md#feat-zotify-governance-01). |
| AR-028 | Code Index Validator | | ✅ | [Doc Governance](HIGH_LEVEL_DESIGN.md#hld-documentation-governance) | | `scripts/validate_code_index.py` | N/A | `project/QA_GOVERNANCE.md` | New script to enforce `CODE_FILE_INDEX.md` completeness. |
| **Privacy & Security** | | | | | | | | | |
| AR-029 | GDPR Compliance Subsystem | FE-14 | ❌ | [Security Model](HIGH_LEVEL_DESIGN.md#hld-security-model) | [Privacy Subsystem](LOW_LEVEL_DESIGN.md#lld-privacy-subsystem) | `api/src/zotify_api/routes/privacy.py` | N/A | `api/docs/system/PRIVACY_COMPLIANCE.md` | Endpoints for data export and deletion. |
| **System Requirements (NFRs)** | | | | | | | | | |
| AR-031 | Test Coverage >90% | SYS-01 | ❌ | [Testing NFR](HIGH_LEVEL_DESIGN.md#hld-non-functional-requirements) | | `pytest --cov` | | | CI gating not implemented |
| AR-032 | Performance <200ms | SYS-02 | 🔍 | [Performance NFR](HIGH_LEVEL_DESIGN.md#hld-non-functional-requirements) | | | | | No performance benchmarks exist |
| AR-033 | Security (Admin Auth) | SYS-03 | ✅ | [Security Model](HIGH_LEVEL_DESIGN.md#hld-security-model) | | | 🔍 | | Basic API key auth is implemented |
---

## 3. Use Case & Feature Traceability

| Audit Ref | Requirement ID | Feature / Component | Status | Source Doc | Notes |
|---|---|---|---|---|---|
| AR-034 | UC-01 | Merge and sync local `.m3u` playlists with Spotify playlists | ❌ | USECASES.md | Dependent on Spotify playlist write support |
| AR-035 | UC-02 | Remote playlist rebuild based on metadata filters | ❌ | USECASES.md | — |
| AR-036 | UC-03 | Upload local tracks to Spotify library | ❌ | USECASES.md | |
| AR-037 | UC-05 | Collaborative playlist version history | ❌ | USECASES.md | |
| AR-038 | UC-06 | Bulk playlist re-tagging for events | ❌ | USECASES.md | |
| AR-039 | UC-07 | Multi-format/quality audio library | 🟡 | USECASES.md | Lacks multi-format and quality control |
| AR-040 | UC-08 | Fine-grained conversion settings | ❌ | USECASES.md | |
| AR-041 | UC-09 | Flexible codec support | ❌ | USECASES.md | |
| AR-042 | UC-10 | Automated downmixing for devices | ❌ | USECASES.md | |
| AR-043 | UC-11 | Size-constrained batch conversion | ❌ | USECASES.md | |
| AR-044 | UC-12 | Quality upgrade watchdog | ❌ | USECASES.md | |
| AR-045 | FE-01 | Advanced Admin Endpoint Security | ❌ | FUTURE_ENHANCEMENTS.md | e.g., JWT, rate limiting |
| AR-046 | FE-02 | Persistent & Distributed Job Queue | 🟡 | FUTURE_ENHANCEMENTS.md | Currently in-memory DB queue |
| AR-047 | FE-03 | Full Spotify OAuth2 & Library Sync | 🟡 | FUTURE_ENHANCEMENTS.md | Lacks write-sync and full library management. |
| AR-048 | FE-04 | Enhanced Download & Job Management | ❌ | FUTURE_ENHANCEMENTS.md | e.g., progress reporting, notifications |
| AR-049 | FE-05 | API Governance | ❌ | FUTURE_ENHANCEMENTS.md | e.g., rate limiting, quotas |
| AR-050 | FE-06 | Observability | 🟡 | FUTURE_ENHANCEMENTS.md | Lacks detailed audit trails. |
| AR-051 | FE-10 | Dynamic Logging Plugin System | ❌ | DYNAMIC_PLUGIN_PROPOSAL.md | |
| AR-052 | FE-11 | Low-Code Platform Integration | ❌ | LOW_CODE_PROPOSAL.md | |
| AR-053 | FE-12 | Home Automation Integration | ❌ | HOME_AUTOMATION_PROPOSAL.md | |
| AR-054 | FE-13 | Plugin-Driven Metadata System | ❌ | MULTI_SOURCE_METADATA_PROPOSAL.md | |
| AR-063 | FE-15 | Dynamic dbstudio Plugin | ❌ | [DBSTUDIO_PLUGIN.md](./proposals/DBSTUDIO_PLUGIN.md) | New proposal for a modular database browser. |
| AR-064 | FE-16 | Dynamic GonkUI Plugin | ❌ | [GONKUI_PLUGIN.md](./proposals/GONKUI_PLUGIN.md) | New proposal to replace the Flask-based UI with a modular plugin. |

---

## 4. Logging System Traceability

| Audit Ref | Requirement | Source Doc | Status |
|---|---|---|---|
| AR-055 | Central LoggingService with async pipeline | LOGGING_SYSTEM_DESIGN.md | ✅ |
| AR-056 | Developer API with per-module log control | LOGGING_SYSTEM_DESIGN.md | ✅ |
| AR-057 | Multi-sink destinations | LOGGING_SYSTEM_DESIGN.md | 🟡 |
| AR-058 | Runtime triggers with hot reload | LOGGING_SYSTEM_DESIGN.md | 🟡 |
| AR-059 | Observability integration | LOGGING_SYSTEM_DESIGN.md | ❌ |
| AR-060 | Security & Compliance audit stream | LOGGING_SYSTEM_DESIGN.md | ❌ |
| AR-061 | Extensibility framework for custom adapters | LOGGING_SYSTEM_DESIGN.md | ❌ |
| AR-062 | Full observability suite | LOGGING_SYSTEM_DESIGN.md | ❌ |

---

**Maintenance Rule:**
Whenever code under `api/src/zotify_api/`, `snitch/`, `Gonk/GonkUI/`, or `scripts/` changes, this matrix must be updated to reflect the change. The linter enforces this.

---

## 5. Artifact-to-Requirement Traceability

This table provides a granular mapping of individual files to their corresponding requirements or architectural components, ensuring that no artifact is an orphan.

| Artifact Path | Linked To Requirement/Component | Notes |
|---|---|---|
| `Gonk/GonkUI/docs/ARCHITECTURE.md` | `AR-024` (Gonk-TestUI) | Architectural overview for the Gonk testing UI. |
| `Gonk/GonkUI/docs/CHANGELOG.md` | `AR-024` (Gonk-TestUI) | Changelog for the Gonk testing UI. |
| `Gonk/GonkUI/docs/CONTRIBUTING.md` | `AR-024` (Gonk-TestUI) | Contribution guidelines for the Gonk testing UI. |
| `Gonk/GonkUI/docs/USER_MANUAL.md` | `AR-024` (Gonk-TestUI) | User manual for the Gonk testing UI. |
| `snitch/docs/ARCHITECTURE.md` | `AR-025` (Snitch) | Architectural overview for the Snitch microservice. |
| `snitch/docs/INSTALLATION.md` | `AR-025` (Snitch) | Installation instructions for Snitch. |
| `snitch/docs/MILESTONES.md` | `AR-025` (Snitch) | Development milestones for Snitch. |
| `snitch/docs/MODULES.md` | `AR-025` (Snitch) | Module breakdown for Snitch. |
| `snitch/docs/PHASES.md` | `AR-025` (Snitch) | Development phases for Snitch. |
| `snitch/docs/PHASE_2_SECURE_CALLBACK.md`| `AR-025` (Snitch) | Design for the secure callback mechanism in Snitch. |
| `snitch/docs/PHASE_2_ZERO_TRUST_DESIGN.md`| `AR-025` (Snitch) | Zero Trust security model design for Snitch. |
| `snitch/docs/PROJECT_PLAN.md` | `AR-025` (Snitch) | Project plan for the Snitch microservice. |
| `snitch/docs/ROADMAP.md` | `AR-025` (Snitch) | Development roadmap for Snitch. |
| `snitch/docs/STATUS.md` | `AR-025` (Snitch) | Status report for the Snitch microservice. |
| `snitch/docs/TASKS.md` | `AR-025` (Snitch) | Task list for the Snitch microservice. |
| `snitch/docs/TEST_RUNBOOK.md` | `AR-025` (Snitch) | Test runbook for the Snitch microservice. |
| `snitch/docs/USER_MANUAL.md` | `AR-025` (Snitch) | User manual for the Snitch microservice. |
| `snitch/docs/phase5-ipc.md` | `AR-025` (Snitch) | Design for Inter-Process Communication in Snitch. |
| `Gonk/GonkCLI/__init__.py` | `AR-024` | GonkCLI package initializer. |
| `Gonk/GonkCLI/main.py` | `AR-024` | Main entry point for the Gonk command-line tool. |
| `Gonk/GonkCLI/modules/jwt_mock.py` | `AR-024` | Mock JWT generator for Gonk testing. |
| `Gonk/GonkCLI/tests/test_jwt_mock.py` | `AR-024` | Unit tests for the mock JWT generator. |
| `Gonk/GonkUI/app.py` | `AR-024` | Main Flask application for the GonkUI. |
| `Gonk/GonkUI/static/app.js` | `AR-024` | Frontend JavaScript for the GonkUI. |
| `Gonk/GonkUI/static/styles.css` | `AR-024` | CSS styles for the GonkUI. |
| `Gonk/GonkUI/views/jwt_ui.py` | `AR-024` | Flask view for the JWT generation UI. |
| `Gonk/GonkCLI/modules/__init__.py` | `AR-024` | GonkCLI modules initializer. |
| `Gonk/GonkCLI/tests/__init__.py` | `AR-024` | GonkCLI tests initializer. |
| `Gonk/GonkUI/views/__init__.py` | `AR-024` | GonkUI views initializer. |
| `api/docs/manuals/API_DEVELOPER_GUIDE.md` | `AR-001` (Core API Architecture) | Guide for developers building on the API. |
| `api/docs/manuals/CICD.md` | `AR-026` (CI/CD Pipeline) | Documentation for the CI/CD pipeline. |
| `api/docs/manuals/ERROR_HANDLING_GUIDE.md` | `AR-021` (Generic Error Handling) | Developer guide to the error handling framework. |
| `api/docs/manuals/LOGGING_GUIDE.md` | `AR-022` (Flexible Logging Framework) | Developer guide to the logging framework. |
| `api/docs/manuals/OPERATOR_MANUAL.md` | `AR-001` (Core API Architecture) | Manual for system operators. |
| `api/docs/manuals/SYSTEM_INTEGRATION_GUIDE.md`| `AR-001` (Core API Architecture) | Guide for integrating external systems. |
| `api/docs/manuals/USER_MANUAL.md` | `AR-001` (Core API Architecture) | Manual for end-users of the API. |
| `api/docs/providers/SPOTIFY.md` | `AR-005` (Provider Abstraction) | Documentation for the Spotify provider. |
| `api/docs/reference/API_REFERENCE.md` | `AR-001` (Core API Architecture) | Full API endpoint reference. |
| `api/docs/reference/FEATURE_SPECS.md` | `AR-001` (Core API Architecture) | Specifications for API features. |
| `api/docs/reference/features/AUTHENTICATION.md` | `AR-007` (Auth Routes & Provider-Agnostic Flow) | Detailed spec for the authentication feature. |
| `api/docs/reference/features/AUTOMATED_DOCUMENTATION_WORKFLOW.md`| `AR-066` (Automated Governance Linter) | Spec for the automated documentation workflow. |
| `api/docs/reference/features/DEVELOPER_FLEXIBLE_LOGGING_FRAMEWORK.md`| `AR-022` (Flexible Logging Framework) | Spec for the flexible logging framework. |
| `api/docs/reference/features/PROVIDER_AGNOSTIC_EXTENSIONS.md`| `AR-005` (Provider Abstraction) | Spec for provider-agnostic extensions. |
| `api/docs/reference/features/PROVIDER_OAUTH.md`| `AR-007` (Auth Routes & Provider-Agnostic Flow) | Spec for provider OAuth flow. |
| `api/docs/system/ERROR_HANDLING_DESIGN.md` | `AR-021` (Generic Error Handling) | High-level design for the error handling system. |
| `api/docs/system/INSTALLATION.md` | `AR-001` (Core API Architecture) | Installation instructions for the API. |
| `api/docs/system/PRIVACY_COMPLIANCE.md` | `AR-029` (GDPR Compliance Subsystem) | Documentation on privacy and GDPR compliance. |
| `api/docs/system/REQUIREMENTS.md` | `AR-001` (Core API Architecture) | System and software requirements for the API. |
| `api/docs/reference/source/ACTIONS____INIT__.py.md` | `AR-021` | Source documentation for the error handler actions module. |
| `api/docs/reference/source/APP.js.md` | `AR-024` | Source documentation for the GonkUI frontend. |
| `api/docs/reference/source/APP.py.md` | `AR-024` | Source documentation for the GonkUI backend. |
| `api/docs/reference/source/AUDIT_API.py.md` | `AR-066` | Source documentation for the API auditing script. |
| `api/docs/reference/source/AUDIT_ENDPOINTS.py.md` | `AR-066` | Source documentation for the endpoint auditing script. |
| `api/docs/reference/source/AUTH.py.md` | `AR-007` | Source documentation for authentication routes. |
| `api/docs/reference/source/AUTH_STATE.py.md` | `AR-007` | Source documentation for OAuth2 state management. |
| `api/docs/reference/source/BASE.py.md` | `AR-005` | Source documentation for the base provider class. |
| `api/docs/reference/source/CACHE.py.md` | `AR-008` | Source documentation for cache management routes. |
| `api/docs/reference/source/CACHE_SERVICE.py.md` | `AR-008` | Source documentation for the cache management service. |
| `api/docs/reference/source/CONFIG.py.md` | `AR-006` | Source documentation for configuration routes and services. |
| `api/docs/reference/source/CONFIG_MODELS.py.md` | `AR-006` | Source documentation for Pydantic configuration models. |
| `api/docs/reference/source/CONFIG_SERVICE.py.md` | `AR-006` | Source documentation for the configuration service. |
| `api/docs/reference/source/CONSOLE_HANDLER.py.md` | `AR-022` | Source documentation for the console logging handler. |
| `api/docs/reference/source/CRUD.py.md` | `AR-004` | Source documentation for database CRUD operations. |
| `api/docs/reference/source/DATABASE_JOB_HANDLER.py.md` | `AR-022` | Source documentation for the database job logging handler. |
| `api/docs/reference/source/DATABASE____INIT__.py.md` | `AR-004` | Source documentation for the database module. |
| `api/docs/reference/source/DB.py.md` | `AR-004` | Source documentation for the database service. |
| `api/docs/reference/source/DEPS.py.md` | `AR-001` | Source documentation for FastAPI dependencies. |
| `api/docs/reference/source/DOWNLOAD.py.md` | `AR-010` | Source documentation for download-related schemas. |
| `api/docs/reference/source/DOWNLOADS.py.md` | `AR-010` | Source documentation for download-related routes. |
| `api/docs/reference/source/DOWNLOAD_SERVICE.py.md` | `AR-010` | Source documentation for the download management service. |
| `api/docs/reference/source/ERROR_HANDLER____INIT__.py.md` | `AR-021` | Source documentation for the error handler module. |
| `api/docs/reference/source/FILTERS.py.md` | `AR-022` | Source documentation for logging filters. |
| `api/docs/reference/source/FORMATTER.py.md` | `AR-021` | Source documentation for the error handler formatter. |
| `api/docs/reference/source/FUNCTIONAL_TEST.py.md` | `AR-031` | Source documentation for the functional test script. |
| `api/docs/reference/source/GENERATE_ENDPOINTS_DOC.py.md` | `AR-066` | Source documentation for the endpoint documentation generator. |
| `api/docs/reference/source/GENERATE_OPENAPI.py.md` | `AR-066` | Source documentation for the OpenAPI generator. |
| `api/docs/reference/source/GENERATE_SOURCE_DOCS.py.md` | `AR-066` | Source documentation for the source documentation generator. |
| `api/docs/reference/source/GENERIC.py.md` | `AR-003` | Source documentation for generic schemas. |
| `api/docs/reference/source/GLOBALS.py.md` | `AR-001` | Source documentation for global variables. |
| `api/docs/reference/source/HOOKS.py.md` | `AR-021` | Source documentation for error handler hooks. |
| `api/docs/reference/source/JSON_AUDIT_HANDLER.py.md` | `AR-022` | Source documentation for the JSON audit logging handler. |
| `api/docs/reference/source/LINTER.py.md` | `AR-027` | Source documentation for the main linter script. |
| `api/docs/reference/source/LOGGING_CONFIG.py.md` | `AR-022` | Source documentation for the logging configuration module. |
| `api/docs/reference/source/LOGGING_FRAMEWORK____INIT__.py.md` | `AR-022` | Source documentation for the logging framework module. |
| `api/docs/reference/source/LOGGING_HANDLERS____INIT__.py.md` | `AR-022` | Source documentation for the logging handlers module. |
| `api/docs/reference/source/LOGGING_SCHEMAS.py.md` | `AR-022` | Source documentation for logging schemas. |
| `api/docs/reference/source/LOGGING_SERVICE.py.md` | `AR-022` | Source documentation for the logging service. |
| `api/docs/reference/source/LOG_CRITICAL.py.md` | `AR-021` | Source documentation for the critical log error handler action. |
| `api/docs/reference/source/MAIN.py.md` | `AR-001` | Source documentation for the main API entry point. |
| `api/docs/reference/source/METADATA.py.md` | `AR-003` | Source documentation for metadata schemas. |
| `api/docs/reference/source/METADATA_SERVICE.py.md` | `AR-002` | Source documentation for the metadata service. |
| `api/docs/reference/source/MODELS.py.md` | `AR-004` | Source documentation for database models. |
| `api/docs/reference/source/NETWORK.py.md` | `AR-011` | Source documentation for network routes. |
| `api/docs/reference/source/NETWORK_SERVICE.py.md` | `AR-011` | Source documentation for the network service. |
| `api/docs/reference/source/NOTIFICATIONS.py.md` | `AR-012` | Source documentation for notification routes. |
| `api/docs/reference/source/NOTIFICATIONS_SERVICE.py.md` | `AR-012` | Source documentation for the notification service. |
| `api/docs/reference/source/PLAYLISTS.py.md` | `AR-013` | Source documentation for playlist routes. |
| `api/docs/reference/source/PLAYLISTS_SERVICE.py.md` | `AR-013` | Source documentation for the playlist service. |
| `api/docs/reference/source/PROVIDERS____INIT__.py.md` | `AR-005` | Source documentation for the providers module. |
| `api/docs/reference/source/REQUEST_ID.py.md` | `AR-023` | Source documentation for the request ID middleware. |
| `api/docs/reference/source/ROUTES____INIT__.py.md` | `AR-001` | Source documentation for the routes module. |
| `api/docs/reference/source/SCHEMAS.py.md` | `AR-003` | Source documentation for the main schemas module. |
| `api/docs/reference/source/SEARCH.py.md` | `AR-014` | Source documentation for search routes. |
| `api/docs/reference/source/SERVICE.py.md` | `AR-002` | Source documentation for the base service class. |
| `api/docs/reference/source/SERVICES____INIT__.py.md` | `AR-002` | Source documentation for the services module. |
| `api/docs/reference/source/SESSION.py.md` | `AR-004` | Source documentation for database session management. |
| `api/docs/reference/source/SNITCH.go.md` | `AR-025` | Source documentation for the Snitch microservice. |
| `api/docs/reference/source/SPOTIFY.py.md` | `AR-005` | Source documentation for Spotify-specific schemas. |
| `api/docs/reference/source/SPOTIFY_CONNECTOR.py.md` | `AR-005` | Source documentation for the Spotify provider connector. |
| `api/docs/reference/source/SPOTI_CLIENT.py.md` | `AR-005` | Source documentation for the Spotify client. |
| `api/docs/reference/source/SYNC.py.md` | `AR-015` | Source documentation for sync routes. |
| `api/docs/reference/source/SYNC_SERVICE.py.md` | `AR-015` | Source documentation for the sync service. |
| `api/docs/reference/source/SYSTEM.py.md` | `AR-016` | Source documentation for system routes. |
| `api/docs/reference/source/TEST_AUTH_FLOW.py.md` | `AR-007` | Source documentation for the auth flow test script. |
| `api/docs/reference/source/TRACKS.py.md` | `AR-017` | Source documentation for track routes. |
| `api/docs/reference/source/TRACKS_SERVICE.py.md` | `AR-017` | Source documentation for the track service. |
| `api/docs/reference/source/TRIGGERS.py.md` | `AR-021` | Source documentation for error handler triggers. |
| `api/docs/reference/source/USER.py.md` | `AR-018` | Source documentation for user routes. |
| `api/docs/reference/source/USER_SERVICE.py.md` | `AR-018` | Source documentation for the user service. |
| `api/docs/reference/source/WEBHOOK.py.md` | `AR-019` | Source documentation for the webhook error handler action. |
| `api/docs/reference/source/WEBHOOKS.py.md` | `AR-019` | Source documentation for webhook routes. |
| `api/docs/CHANGELOG.md` | `AR-001` | Record of all notable changes to the API. |
| `api/docs/CODE_QUALITY_INDEX.md` | `AR-066` | Index of code quality metrics and reports. |
| `api/docs/DOCS_QUALITY_INDEX.md` | `AR-066` | Index of documentation quality metrics and reports. |
| `api/docs/MASTER_INDEX.md` | `AR-001` | Master index for all API documentation. |
| `api/logging_config.yml` | `AR-022` (Flexible Logging Framework) | Legacy logging configuration. |
| `api/logging_framework.yml` | `AR-022` (Flexible Logging Framework) | Configuration for the flexible logging framework. |
| `api/src/zotify_api/auth_state.py` | `AR-007` (Auth Routes & Provider-Agnostic Flow) | Manages OAuth2 state. |
| `api/src/zotify_api/config.py` | `AR-006` (Centralized Configuration) | Core application configuration. |
| `api/src/zotify_api/globals.py` | `AR-001` (Core API Architecture) | Global variables and constants. |
| `api/src/zotify_api/logging_config.py` | `AR-022` (Flexible Logging Framework) | Application logging configuration. |
| `api/src/zotify_api/main.py` | `AR-001` (Core API Architecture) | Main FastAPI application entry point. |
| `api/src/zotify_api/core/error_handler/` | `AR-021` (Generic Error Handling) | Centralized error handling module. |
| `api/src/zotify_api/core/logging_framework/` | `AR-022` (Flexible Logging Framework) | Core logging framework module. |
| `api/src/zotify_api/database/` | `AR-004` (Unified Persistence) | Database models, session, and CRUD operations. |
| `api/src/zotify_api/middleware/` | `AR-023` (API Middleware) | FastAPI middleware implementations. |
| `api/src/zotify_api/models/` | `AR-003` (Pydantic Schema Layer) | Pydantic models for data structures. |
| `api/src/zotify_api/providers/` | `AR-005` (Provider Abstraction) | Music provider abstraction layer. |
| `api/src/zotify_api/routes/` | `AR-001` (API Routes Layer) | All API endpoint definitions. |
| `api/src/zotify_api/schemas/` | `AR-003` (Pydantic Schema Layer) | Pydantic schemas for API requests and responses. |
| `api/src/zotify_api/services/` | `AR-002` (Business Logic Service Layer) | Core business logic services. |
| `api/tests/` | `AR-031` (Test Coverage >90%) | All functional and unit tests for the API. |
| `scripts/content_alignment_check.py` | `AR-066` | Script to check for content-level alignment. |
| `scripts/description_compliance_check.py` | `AR-066` | Script to check for description compliance. |
| `scripts/propagate_descriptions.py` | `AR-066` | Script to propagate descriptions to index files. |
| `scripts/build_project_registry.py` | `AR-065` | Script to build the project registry from `TRACE_INDEX.yml`. |
| `api/src/zotify_api/schemas/` | `AR-003` | All Pydantic schemas for data validation. |
| `api/src/zotify_api/services/` | `AR-002` | All business logic services. |
| `api/tests/` | `AR-031` | All functional and unit tests. |
| `Gonk/` | `AR-024` | All files related to the Gonk testing tool. |
| `snitch/` | `AR-025` | All files related to the Snitch microservice. |
| `api/MIGRATIONS.md` | `AR-004` | Documentation for database migrations. |
| `api/alembic/env.py` | `AR-004` | Alembic environment script. |
| `api/alembic/versions/5f96175ff7c9_add_notifications_enabled_to_.py` | `AR-004` | Alembic migration script. |
| `api/src/zotify_api/core/error_handler/__init__.py`| `AR-021` | Error handler module initializer. |
| `api/src/zotify_api/core/error_handler/actions/__init__.py`| `AR-021` | Error handler actions initializer. |
| `api/src/zotify_api/core/error_handler/actions/log_critical.py`| `AR-021` | Critical log error handler action. |
| `api/src/zotify_api/core/error_handler/actions/webhook.py`| `AR-021` | Webhook error handler action. |
| `api/src/zotify_api/core/error_handler/config.py`| `AR-021` | Error handler configuration. |
| `api/src/zotify_api/core/error_handler/formatter.py`| `AR-021` | Error handler formatter. |
| `api/src/zotify_api/core/error_handler/hooks.py`| `AR-021` | Error handler hooks. |
| `api/src/zotify_api/core/error_handler/triggers.py`| `AR-021` | Error handler triggers. |
| `api/src/zotify_api/core/logging_framework/__init__.py`| `AR-022` | Logging framework module initializer. |
| `api/src/zotify_api/core/logging_framework/filters.py`| `AR-022` | Logging filters. |
| `api/src/zotify_api/core/logging_framework/schemas.py`| `AR-022` | Logging schemas. |
| `api/src/zotify_api/core/logging_framework/service.py`| `AR-022` | Logging service. |
| `api/src/zotify_api/core/logging_handlers/__init__.py`| `AR-022` | Logging handlers initializer. |
| `api/src/zotify_api/core/logging_handlers/base.py`| `AR-022` | Base logging handler. |
| `api/src/zotify_api/core/logging_handlers/console_handler.py`| `AR-022` | Console logging handler. |
| `api/src/zotify_api/core/logging_handlers/database_job_handler.py`| `AR-022` | Database job logging handler. |
| `api/src/zotify_api/core/logging_handlers/json_audit_handler.py`| `AR-022` | JSON audit logging handler. |
| `api/src/zotify_api/database/__init__.py`| `AR-004` | Database module initializer. |
| `api/src/zotify_api/middleware/__init__.py`| `AR-023` | Middleware module initializer. |
| `api/src/zotify_api/models/__init__.py`| `AR-003` | Models module initializer. |
| `api/src/zotify_api/providers/__init__.py`| `AR-005` | Providers module initializer. |
| `api/src/zotify_api/routes/__init__.py`| `AR-001` | Routes module initializer. |
| `api/src/zotify_api/schemas/__init__.py`| `AR-003` | Schemas module initializer. |
| `api/src/zotify_api/services/__init__.py`| `AR-002` | Services module initializer. |
| `api/tests/__init__.py`| `AR-031` | Tests module initializer. |
| `snitch/snitch.go` | `AR-025` | Main Go source file for the Snitch microservice. |
