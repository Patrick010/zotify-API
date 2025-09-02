# Alignment Matrix (Living Document)

**Purpose:**
This matrix maintains a live mapping between high-level design (HLD), low-level design (LLD), implementation, and reference documentation.
It must be updated with every feature, refactor, or documentation change.

---

| Feature / Component | Audit Ref | HLD Reference | LLD Reference | Code Path(s) | Documentation |
| --- | --- | --- | --- | --- | --- |
| **Core API Architecture** | | | | | |
| API Routes Layer | AR-001 | [Routes Layer](HIGH_LEVEL_DESIGN.md#hld-routes-layer) | [API Endpoint Baseline](LOW_LEVEL_DESIGN.md#lld-api-endpoint-baseline) | `api/src/zotify_api/routes/` | `project/api/endpoints.yaml` |
| Business Logic Service Layer | AR-002 | [Service Layer](HIGH_LEVEL_DESIGN.md#hld-service-layer) | `N/A` | `api/src/zotify_api/services/` | `api/docs/reference/API_REFERENCE.md` |
| Pydantic Schema Layer | AR-003 | [Schema Layer](HIGH_LEVEL_DESIGN.md#hld-schema-layer) | `N/A` | `api/src/zotify_api/schemas/` | `api/docs/reference/API_REFERENCE.md` |
| Unified Persistence (SQLAlchemy) | AR-004 | [Persistence Layer](HIGH_LEVEL_DESIGN.md#hld-persistence-layer) | [Unified Database Architecture](LOW_LEVEL_DESIGN.md#lld-unified-database-architecture) | `api/src/zotify_api/database/` | `project/LOW_LEVEL_DESIGN.md#lld-unified-database-architecture` |
| Provider Abstraction | AR-005 | [Provider Abstraction](HIGH_LEVEL_DESIGN.md#hld-provider-abstraction-layer) | [Provider Abstraction Layer](LOW_LEVEL_DESIGN.md#lld-provider-abstraction-layer) | `api/src/zotify_api/providers/` | `project/proposals/DYNAMIC_PLUGIN_PROPOSAL.md` |
| Centralized Configuration | AR-006 | [Config Layer](HIGH_LEVEL_DESIGN.md#hld-config-layer) | [Configuration Management](LOW_LEVEL_DESIGN.md#lld-configuration-management) | `api/src/zotify_api/config.py`, `api/src/zotify_api/services/config_service.py` | `project/LOW_LEVEL_DESIGN.md#lld-configuration-management` |
| **API Routes & Services** | | | | | |
| Auth Routes | AR-007 | [Auth Provider Interface](HIGH_LEVEL_DESIGN.md#hld-authentication-provider-interface) | [Spotify Integration Design](LOW_LEVEL_DESIGN.md#lld-spotify-integration-design) | `api/src/zotify_api/routes/auth.py` | `project/api/endpoints.yaml` |
| Cache Routes | AR-008 | `N/A` | `N/A` | `api/src/zotify_api/routes/cache.py` | `project/api/endpoints.yaml` |
| Config Routes | AR-009 | [Config Layer](HIGH_LEVEL_DESIGN.md#hld-config-layer) | [Configuration Management](LOW_LEVEL_DESIGN.md#lld-configuration-management) | `api/src/zotify_api/routes/config.py` | `project/api/endpoints.yaml` |
| Downloads Routes | AR-010 | `N/A` | [Downloads Subsystem Design](LOW_LEVEL_DESIGN.md#lld-downloads-subsystem-design) | `api/src/zotify_api/routes/downloads.py` | `project/api/endpoints.yaml` |
| Network Routes | AR-011 | `N/A` | `N/A` | `api/src/zotify_api/routes/network.py` | `project/api/endpoints.yaml` |
| Notifications Routes | AR-012 | `N/A` | `N/A` | `api/src/zotify_api/routes/notifications.py` | `project/api/endpoints.yaml` |
| Playlists Routes | AR-013 | `N/A` | `N/A` | `api/src/zotify_api/routes/playlists.py` | `project/api/endpoints.yaml` |
| Search Routes | AR-014 | `N/A` | `N/A` | `api/src/zotify_api/routes/search.py` | `project/api/endpoints.yaml` |
| Sync Routes | AR-015 | `N/A` | `N/A` | `api/src/zotify_api/routes/sync.py` | `project/api/endpoints.yaml` |
| System Routes | AR-016 | `N/A` | `N/A` | `api/src/zotify_api/routes/system.py` | `project/api/endpoints.yaml` |
| Tracks Routes | AR-017 | `N/A` | `N/A` | `api/src/zotify_api/routes/tracks.py` | `project/api/endpoints.yaml` |
| User Routes | AR-018 | `N/A` | `N/A` | `api/src/zotify_api/routes/user.py` | `project/api/endpoints.yaml` |
| Webhooks Routes | AR-019 | `N/A` | `N/A` | `api/src/zotify_api/routes/webhooks.py` | `project/api/endpoints.yaml` |
| **Database Models** | | | | | |
| All DB Models | AR-020 | [Persistence Layer](HIGH_LEVEL_DESIGN.md#hld-persistence-layer) | [Unified Database Architecture](LOW_LEVEL_DESIGN.md#lld-unified-database-architecture) | `api/src/zotify_api/database/models.py` | `project/LOW_LEVEL_DESIGN.md#lld-unified-database-architecture` |
| **Cross-Cutting Concerns** | | | | | |
| Generic Error Handling | AR-021 | [Error Handling Layer](HIGH_LEVEL_DESIGN.md#hld-generic-error-handling-layer) | [Generic Error Handling Module](LOW_LEVEL_DESIGN.md#lld-generic-error-handling-module) | `api/src/zotify_api/core/error_handler/` | `api/docs/system/ERROR_HANDLING_STRATEGY.md` |
| Flexible Logging Framework | AR-022 | [Logging Layer](HIGH_LEVEL_DESIGN.md#hld-logging-layer) | [Flexible Logging Framework](LOW_LEVEL_DESIGN.md#lld-flexible-logging-framework) | `api/src/zotify_api/core/logging_framework/` | `api/docs/system/LOGGING_FRAMEWORK.md` |
| API Middleware | AR-023 | `N/A` | [API Middleware](LOW_LEVEL_DESIGN.md#lld-api-middleware) | `api/src/zotify_api/middleware/` | `project/LOW_LEVEL_DESIGN.md#lld-api-middleware` |
| **Supporting Modules** | | | | | |
| Gonk-TestUI | AR-024 | [Supporting Modules](HIGH_LEVEL_DESIGN.md#hld-supporting-modules) | [Gonk-TestUI](LOW_LEVEL_DESIGN.md#lld-gonk-testui) | `gonk-testUI/` | `gonk-testUI/README.md` |
| Snitch | AR-025 | [Supporting Modules](HIGH_LEVEL_DESIGN.md#hld-supporting-modules) | [Snitch](LOW_LEVEL_DESIGN.md#lld-snitch) | `snitch/` | `snitch/docs/PROJECT_PLAN.md` |
| **Infrastructure & Tooling** | | | | | |
| CI/CD Pipeline | AR-026 | [Deployment Model](HIGH_LEVEL_DESIGN.md#hld-deployment-model) | `N/A` | `.github/workflows/ci.yml` | `project/CICD.md` |
| Documentation Linter | AR-027 | [Doc Governance](HIGH_LEVEL_DESIGN.md#hld-documentation-governance) | [Ongoing Maintenance](LOW_LEVEL_DESIGN.md#lld-ongoing-maintenance) | `scripts/lint-docs.py` | `AGENTS.md` |
| Work Logging Script | AR-028 | [Doc Governance](HIGH_LEVEL_DESIGN.md#hld-documentation-governance) | [Ongoing Maintenance](LOW_LEVEL_DESIGN.md#lld-ongoing-maintenance) | `scripts/log-work.py` | `AGENTS.md` |
| **Privacy & Security** | | | | | |
| GDPR Compliance Subsystem | AR-029 | [Security Model](HIGH_LEVEL_DESIGN.md#hld-security-model) | [Privacy Subsystem](LOW_LEVEL_DESIGN.md#lld-privacy-subsystem) | `api/src/zotify_api/routes/privacy.py` | `api/docs/system/PRIVACY_COMPLIANCE.md` |
| **Project Governance** | | | | | |
| Task & Doc Hygiene | AR-030 | [Doc Governance](HIGH_LEVEL_DESIGN.md#hld-documentation-governance) | [Ongoing Maintenance](LOW_LEVEL_DESIGN.md#lld-ongoing-maintenance) | `scripts/lint-docs.py` | `project/TASK_CHECKLIST.md` |

---

**Maintenance Rule:**
Whenever code under `api/src/zotify_api/`, `snitch/`, `gonk-testUI/`, or `scripts/` changes, this matrix must be updated to reflect the change. The linter enforces this as of Phase 5.
