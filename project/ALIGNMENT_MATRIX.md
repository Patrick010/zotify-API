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
| AR-004 | Unified Persistence (SQLAlchemy) | | ✅ | [Persistence Layer](HIGH_LEVEL_DESIGN.md#hld-persistence-layer) | [Unified Database Architecture](LOW_LEVEL_DESIGN.md#lld-unified-database-architecture) | `api/src/zotify_api/database/` | ✅ | `project/LOW_LEVEL_DESIGN.md#lld-unified-database-architecture` | |
| AR-005 | Provider Abstraction | SYS-04 | ✅ | [Provider Abstraction](HIGH_LEVEL_DESIGN.md#hld-provider-abstraction-layer) | [Provider Abstraction Layer](LOW_LEVEL_DESIGN.md#lld-provider-abstraction-layer) | `api/src/zotify_api/providers/` | N/A | `project/proposals/DYNAMIC_PLUGIN_PROPOSAL.md` | Provider model allows for extension. |
| AR-006 | Centralized Configuration | FE-09 | 🟡 | [Config Layer](HIGH_LEVEL_DESIGN.md#hld-config-layer) | [Configuration Management](LOW_LEVEL_DESIGN.md#lld-configuration-management) | `api/src/zotify_api/config.py`, `api/src/zotify_api/services/config_service.py` | 🔍 | `project/LOW_LEVEL_DESIGN.md#lld-configuration-management` | Dual system exists, not unified. |
| **API Routes & Services** | | | | | | | | | |
| AR-007 | Auth Routes & Provider-Agnostic Flow | SYS-07 | ✅ | [Auth Provider Interface](HIGH_LEVEL_DESIGN.md#hld-authentication-provider-interface) | [Spotify Integration Design](LOW_LEVEL_DESIGN.md#lld-spotify-integration-design) | `api/src/zotify_api/routes/auth.py`, `api/src/zotify_api/providers/` | ✅ | `project/api/endpoints.yaml` | Handles OAuth2 callbacks generically in the provider layer. |
| AR-008 | Cache Routes | | ✅ | `N/A` | `N/A` | `api/src/zotify_api/routes/cache.py` | ✅ | `project/api/endpoints.yaml` | |
| AR-009 | Config Routes | FE-09 | 🟡 | [Config Layer](HIGH_LEVEL_DESIGN.md#hld-config-layer) | [Configuration Management](LOW_LEVEL_DESIGN.md#lld-configuration-management) | `api/src/zotify_api/routes/config.py` | ✅ | `project/api/endpoints.yaml` | |
| AR-010 | Downloads Routes & Service | UC-04 | 🟡 | `N/A` | [Downloads Subsystem Design](LOW_LEVEL_DESIGN.md#lld-downloads-subsystem-design) | `api/src/zotify_api/routes/downloads.py` | 🔍 | `project/api/endpoints.yaml` | Lacks automation and file management. |
| AR-011 | Network Routes | | ✅ | `N/A` | `N/A` | `api/src/zotify_api/routes/network.py` | ✅ | `project/api/endpoints.yaml` | |
| AR-012 | Notifications Routes | | ✅ | `N/A` | `N/A` | `api/src/zotify_api/routes/notifications.py` | ✅ | `project/api/endpoints.yaml` | |
| AR-013 | Playlists Routes | | ✅ | `N/A` | `N/A` | `api/src/zotify_api/routes/playlists.py` | ✅ | `project/api/endpoints.yaml` | |
| AR-014 | Search Routes | | ✅ | `N/A` | `N/A` | `api/src/zotify_api/routes/search.py` | ✅ | `project/api/endpoints.yaml` | |
| AR-015 | Sync Routes | | ✅ | `N/A` | `N/A` | `api/src/zotify_api/routes/sync.py` | ✅ | `project/api/endpoints.yaml` | |
| AR-016 | System Routes & Health Checks | FE-08 | 🟡 | `N/A` | `N/A` | `api/src/zotify_api/routes/system.py` | 🔍 | `project/api/endpoints.yaml` | Only basic uptime/env endpoints exist. |
| AR-017 | Tracks Routes | | ✅ | `N/A` | `N/A` | `api/src/zotify_api/routes/tracks.py` | ✅ | `project/api/endpoints.yaml` | |
| AR-018 | User Routes | | ✅ | `N/A` | `N/A` | `api/src/zotify_api/routes/user.py` | ✅ | `project/api/endpoints.yaml` | |
| AR-019 | Webhooks Routes | | ✅ | `N/A` | `N/A` | `api/src/zotify_api/routes/webhooks.py` | ✅ | `project/api/endpoints.yaml` | |
| **Cross-Cutting Concerns** | | | | | | | | | |
| AR-021 | Generic Error Handling | FE-07 | ✅ | [Error Handling Layer](HIGH_LEVEL_DESIGN.md#hld-generic-error-handling-layer) | [Generic Error Handling Module](LOW_LEVEL_DESIGN.md#lld-generic-error-handling-module) | `api/src/zotify_api/core/error_handler/` | ✅ | `api/docs/system/ERROR_HANDLING_STRATEGY.md` | Centralized error handling module is complete and integrated. |
| AR-022 | Flexible Logging Framework | FE-07a | ✅ | [Logging Layer](HIGH_LEVEL_DESIGN.md#hld-logging-layer) | [Flexible Logging Framework](LOW_LEVEL_DESIGN.md#lld-flexible-logging-framework) | `api/src/zotify_api/core/logging_framework/` | ✅ | `api/docs/system/LOGGING_FRAMEWORK.md`, `docs/manuals/LOGGING_GUIDE.md` | Core framework is complete. |
| AR-023 | API Middleware | SYS-05 | ✅ | `N/A` | [API Middleware](LOW_LEVEL_DESIGN.md#lld-api-middleware) | `api/src/zotify_api/middleware/` | N/A | `project/LOW_LEVEL_DESIGN.md#lld-api-middleware` | Permissive CORS policy for Web UI. |
| **Supporting Modules** | | | | | | | | | |
| AR-024 | Gonk-TestUI | | ✅ | [Supporting Modules](HIGH_LEVEL_DESIGN.md#hld-supporting-modules) | [Gonk-TestUI](LOW_LEVEL_DESIGN.md#lld-gonk-testui) | `Gonk/GonkUI/` | | `Gonk/GonkUI/README.md` | |
| AR-025 | Snitch | SYS-06 | 🟡 | [Supporting Modules](HIGH_LEVEL_DESIGN.md#hld-supporting-modules) | [Snitch](LOW_LEVEL_DESIGN.md#lld-snitch) | `snitch/` | ✅ | `snitch/docs/PROJECT_PLAN.md` | Zero Trust model with end-to-end payload encryption. |
| **Infrastructure & Tooling** | | | | | | | | | |
| AR-026 | CI/CD Pipeline | | ✅ | [Deployment Model](HIGH_LEVEL_DESIGN.md#hld-deployment-model) | `N/A` | `.github/workflows/ci.yml` | | `project/CICD.md` | |
| AR-027 | Unified Linter & Logger | | ✅ | [Doc Governance](HIGH_LEVEL_DESIGN.md#hld-documentation-governance) | [Ongoing Maintenance](LOW_LEVEL_DESIGN.md#lld-ongoing-maintenance) | `scripts/linter.py` | N/A | `AGENTS.md` | Merged `log-work.py` into `linter.py`. |
| AR-028 | Code Index Validator | | ✅ | [Doc Governance](HIGH_LEVEL_DESIGN.md#hld-documentation-governance) | | `scripts/validate_code_index.py` | N/A | `project/QA_GOVERNANCE.md` | New script to enforce `CODE_FILE_INDEX.md` completeness. |
| **Privacy & Security** | | | | | | | | | |
| AR-029 | GDPR Compliance Subsystem | FE-14 | ❌ | [Security Model](HIGH_LEVEL_DESIGN.md#hld-security-model) | [Privacy Subsystem](LOW_LEVEL_DESIGN.md#lld-privacy-subsystem) | `api/src/zotify_api/routes/privacy.py` | N/A | `api/docs/system/PRIVACY_COMPLIANCE.md` | Endpoints for data export and deletion. |
| **Project Governance** | | | | | | | | | |
| AR-030 | Task & Doc Hygiene | | ✅ | [Doc Governance](HIGH_LEVEL_DESIGN.md#hld-documentation-governance) | [Ongoing Maintenance](LOW_LEVEL_DESIGN.md#lld-ongoing-maintenance) | `scripts/linter.py` | | `project/TASK_CHECKLIST.md` | Enforced by linter. |
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
