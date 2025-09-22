# Code File Index

This document serves as the canonical registry of all code files in the Zotify API repository. Its purpose is to aid in developer discovery, navigation, and long-term maintainability.

| Path | Type | Description | Status | Linked Docs | Notes |
|------|------|-------------|--------|-------------|-------|
| `Gonk/GonkCLI/main.py` | Script | Main entry point for the Gonk CLI. | Active | | |
| `Gonk/GonkCLI/modules/jwt_mock.py` | Core | Mock JWT generator for the Gonk tools. | Active | | |
| `Gonk/GonkCLI/tests/test_jwt_mock.py` | Test | Tests for the JWT mock generator. | Active | | |
| `Gonk/GonkUI/app.py` | Core | Main Flask application for the GonkUI. | Active | `../reference/source/APP.py.md` | |
| `Gonk/GonkUI/static/app.js` | Core | Frontend JavaScript for the GonkUI. | Active | `../reference/source/APP.js.md` | |
| `Gonk/GonkUI/views/jwt_ui.py` | Core | View logic for the GonkUI JWT features. | Active | | |
| `api/src/zotify_api/auth_state.py` | Core | Manages the state for the OAuth2 flow. | Active | `../reference/source/AUTH_STATE.py.md` | |
| `api/src/zotify_api/config.py` | Config | Application settings, secrets, and environment loading. | Active | `../reference/source/CONFIG.py.md` | |
| `api/src/zotify_api/globals.py` | Config | Global variables and application-wide constants. | Active | `../reference/source/GLOBALS.py.md` | |
| `api/src/zotify_api/logging_config.py` | Config | Configuration for the application's logging framework. | Active | `../reference/source/LOGGING_CONFIG.py.md` | |
| `api/src/zotify_api/main.py` | Core | Main FastAPI application entry point. | Active | `../reference/source/MAIN.py.md` | |
| `api/src/zotify_api/core/error_handler/config.py` | Config | Configuration for the error handling subsystem. | Active | `../reference/source/CONFIG.py.md` | |
| `api/src/zotify_api/core/error_handler/formatter.py` | Core | Formats error responses. | Active | `../reference/source/FORMATTER.py.md` | |
| `api/src/zotify_api/core/error_handler/hooks.py` | Core | Error handling hooks. | Active | `../reference/source/HOOKS.py.md` | |
| `api/src/zotify_api/core/error_handler/triggers.py` | Core | Error handling triggers. | Active | `../reference/source/TRIGGERS.py.md` | |
| `api/src/zotify_api/core/error_handler/actions/log_critical.py` | Core | Error handling action to log critical failures. | Active | `../reference/source/LOG_CRITICAL.py.md` | |
| `api/src/zotify_api/core/error_handler/actions/webhook.py` | Core | Error handling action to send a webhook on failure. | Active | `../reference/source/WEBHOOK.py.md` | |
| `api/src/zotify_api/core/logging_framework/filters.py` | Core | Custom filters for the logging framework. | Active | `../reference/source/FILTERS.py.md` | |
| `api/src/zotify_api/core/logging_framework/schemas.py` | Model | Pydantic schemas for logging. | Active | `../reference/source/SCHEMAS.py.md` | |
| `api/src/zotify_api/core/logging_framework/service.py` | Core | Core service for the logging framework. | Active | `../reference/source/SERVICE.py.md` | |
| `api/src/zotify_api/core/logging_handlers/base.py` | Core | Base class for logging handlers. | Active | `../reference/source/BASE.py.md` | |
| `api/src/zotify_api/core/logging_handlers/console_handler.py` | Core | Logging handler for console output. | Active | `../reference/source/CONSOLE_HANDLER.py.md` | |
| `api/src/zotify_api/core/logging_handlers/database_job_handler.py` | Core | Logging handler for database job logging. | Active | `../reference/source/DATABASE_JOB_HANDLER.py.md` | |
| `api/src/zotify_api/core/logging_handlers/json_audit_handler.py` | Core | Logging handler for JSON audit logs. | Active | `../reference/source/JSON_AUDIT_HANDLER.py.md` | |
| `api/src/zotify_api/database/crud.py` | Core | Create, Read, Update, Delete database operations. | Active | `../reference/source/CRUD.py.md` | |
| `api/src/zotify_api/database/models.py` | Model | Defines the SQLAlchemy models for the database. | Active | `../reference/source/MODELS.py.md` | |
| `api/src/zotify_api/database/session.py` | Core | Manages the SQLAlchemy database session. | Active | `../reference/source/SESSION.py.md` | |
| `api/src/zotify_api/middleware/request_id.py` | Core | Middleware to add a unique request ID to each request. | Active | `../reference/source/REQUEST_ID.py.md` | |
| `api/src/zotify_api/models/config_models.py` | Model | Pydantic models for configuration. | Active | `../reference/source/CONFIG_MODELS.py.md` | |
| `api/src/zotify_api/models/sync.py` | Model | Pydantic models for synchronization. | Active | `../reference/source/SYNC.py.md` | |
| `api/src/zotify_api/providers/base.py` | Core | Abstract base class for music providers. | Active | `../reference/source/BASE.py.md` | |
| `api/src/zotify_api/providers/spotify_connector.py` | Core | Connector for the Spotify API. | Active | `../reference/source/SPOTIFY_CONNECTOR.py.md` | |
| `api/src/zotify_api/routes/auth.py` | Route | Handles external Spotify OAuth2 login flow. | Active | `../reference/source/AUTH.py.md` | |
| `api/src/zotify_api/routes/cache.py` | Route | Endpoints for managing the application cache. | Active | `../reference/source/CACHE.py.md` | |
| `api/src/zotify_api/routes/config.py` | Route | Endpoints for managing application configuration. | Active | `../reference/source/CONFIG.py.md` | |
| `api/src/zotify_api/routes/downloads.py` | Route | Endpoints for managing track downloads. | Active | `../reference/source/DOWNLOADS.py.md` | |
| `api/src/zotify_api/routes/jwt_auth.py` | Route | Handles local user JWT registration and login. | Active | | Protects user-specific endpoints. |
| `api/src/zotify_api/routes/network.py` | Route | Endpoints for network-related operations. | Active | `../reference/source/NETWORK.py.md` | |
| `api/src/zotify_api/routes/notifications.py` | Route | Endpoints for managing notifications. | Active | `../reference/source/NOTIFICATIONS.py.md` | |
| `api/src/zotify_api/routes/playlists.py` | Route | Endpoints for managing playlists. | Active | `../reference/source/PLAYLISTS.py.md` | |
| `api/src/zotify_api/routes/search.py` | Route | Endpoint for searching tracks. | Active | `../reference/source/SEARCH.py.md` | |
| `api/src/zotify_api/routes/sync.py` | Route | Endpoints for synchronization. | Active | `../reference/source/SYNC.py.md` | |
| `api/src/zotify_api/routes/system.py` | Route | Endpoints for system status and operations. | Active | `../reference/source/SYSTEM.py.md` | |
| `api/src/zotify_api/routes/tracks.py` | Route | Endpoints for managing tracks. | Active | `../reference/source/TRACKS.py.md` | |
| `api/src/zotify_api/routes/user.py` | Route | Endpoints for user profile and preferences. | Active | `../reference/source/USER.py.md` | Secured by JWT. |
| `api/src/zotify_api/routes/webhooks.py` | Route | Endpoints for managing webhooks. | Active | `../reference/source/WEBHOOKS.py.md` | |
| `api/src/zotify_api/schemas/auth.py` | Model | Pydantic schemas for authentication. | Active | `../reference/source/AUTH.py.md` | |
| `api/src/zotify_api/schemas/cache.py` | Model | Pydantic schemas for cache management. | Active | `../reference/source/CACHE.py.md` | |
| `api/src/zotify_api/schemas/download.py` | Model | Pydantic schemas for downloads. | Active | `../reference/source/DOWNLOAD.py.md` | |
| `api/src/zotify_api/schemas/generic.py` | Model | Generic Pydantic schemas. | Active | `../reference/source/GENERIC.py.md` | |
| `api/src/zotify_api/schemas/logging_schemas.py` | Model | Pydantic schemas for logging. | Active | `../reference/source/LOGGING_SCHEMAS.py.md` | |
| `api/src/zotify_api/schemas/metadata.py` | Model | Pydantic schemas for metadata. | Active | `../reference/source/METADATA.py.md` | |
| `api/src/zotify_api/schemas/network.py` | Model | Pydantic schemas for network operations. | Active | `../reference/source/NETWORK.py.md` | |
| `api/src/zotify_api/schemas/notifications.py` | Model | Pydantic schemas for notifications. | Active | `../reference/source/NOTIFICATIONS.py.md` | |
| `api/src/zotify_api/schemas/playlists.py` | Model | Pydantic schemas for playlists. | Active | `../reference/source/PLAYLISTS.py.md` | |
| `api/src/zotify_api/schemas/spotify.py` | Model | Pydantic schemas for Spotify objects. | Active | `../reference/source/SPOTIFY.py.md` | |
| `api/src/zotify_api/schemas/system.py` | Model | Pydantic schemas for system status. | Active | `../reference/source/SYSTEM.py.md` | |
| `api/src/zotify_api/schemas/tracks.py` | Model | Pydantic schemas for tracks. | Active | `../reference/source/TRACKS.py.md` | |
| `api/src/zotify_api/schemas/user.py` | Model | Pydantic schemas for users. | Active | `../reference/source/USER.py.md` | |
| `api/src/zotify_api/schemas/webhooks.py` | Model | Pydantic schemas for webhooks. | Active | `../reference/source/WEBHOOKS.py.md` | |
| `api/src/zotify_api/services/auth.py` | Core | Service for authentication logic. | Active | `../reference/source/AUTH.py.md` | |
| `api/src/zotify_api/services/cache_service.py` | Core | Service for cache management. | Active | `../reference/source/CACHE_SERVICE.py.md` | |
| `api/src/zotify_api/services/config_service.py` | Core | Service for configuration management. | Active | `../reference/source/CONFIG_SERVICE.py.md` | |
| `api/src/zotify_api/services/db.py` | Core | Service for database interactions. | Active | `../reference/source/DB.py.md` | |
| `api/src/zotify_api/services/deps.py` | Core | FastAPI dependencies. | Active | `../reference/source/DEPS.py.md` | |
| `api/src/zotify_api/services/download_service.py` | Core | Service for download management. | Active | `../reference/source/DOWNLOAD_SERVICE.py.md` | |
| `api/src/zotify_api/services/jwt_service.py` | Core | Service for JWT creation and validation. | Active | | |
| `api/src/zotify_api/services/logging_service.py` | Core | Service for logging. | Active | `../reference/source/LOGGING_SERVICE.py.md` | |
| `api/src/zotify_api/services/metadata_service.py` | Core | Service for metadata management. | Active | `../reference/source/METADATA_SERVICE.py.md` | |
| `api/src/zotify_api/services/network_service.py` | Core | Service for network operations. | Active | `../reference/source/NETWORK_SERVICE.py.md` | |
| `api/src/zotify_api/services/notifications_service.py` | Core | Service for notification management. | Active | `../reference/source/NOTIFICATIONS_SERVICE.py.md` | |
| `api/src/zotify_api/services/playlists_service.py` | Core | Service for playlist management. | Active | `../reference/source/PLAYLISTS_SERVICE.py.md` | |
| `api/src/zotify_api/services/search.py` | Core | Service for search operations. | Active | `../reference/source/SEARCH.py.md` | |
| `api/src/zotify_api/services/spoti_client.py` | Core | Client for Spotify API. | Active | `../reference/source/SPOTI_CLIENT.py.md` | |
| `api/src/zotify_api/services/sync_service.py` | Core | Service for synchronization. | Active | `../reference/source/SYNC_SERVICE.py.md` | |
| `api/src/zotify_api/services/tracks_service.py` | Core | Service for track management. | Active | `../reference/source/TRACKS_SERVICE.py.md` | |
| `api/src/zotify_api/services/user_service.py` | Core | Service for user management. | Active | `../reference/source/USER_SERVICE.py.md` | |
| `api/src/zotify_api/services/webhooks.py` | Core | Service for webhook management. | Active | `../reference/source/WEBHOOKS.py.md` | |
| `api/tests/conftest.py` | Test | Pytest configuration and fixtures. | Active | | |
| `api/tests/test_cache.py` | Test | Tests for the cache endpoints. | Active | | |
| `api/tests/test_config.py` | Test | Tests for the config endpoints. | Active | | |
| `api/tests/test_download.py` | Test | Tests for the download endpoints. | Active | | |
| `api/tests/test_network.py` | Test | Tests for the network endpoints. | Active | | |
| `api/tests/test_notifications.py` | Test | Tests for the notification endpoints. | Active | | |
| `api/tests/test_playlists.py` | Test | Tests for the playlist endpoints. | Active | | |
| `api/tests/test_system.py` | Test | Tests for the system endpoints. | Active | | |
| `api/tests/test_tracks.py` | Test | Tests for the track endpoints. | Active | | |
| `api/tests/test_user.py` | Test | Tests for the user endpoints. | Active | | |
| `api/tests/unit/test_auth.py` | Test | Tests the Spotify OAuth flow. | Active | `../reference/source/TEST_AUTH_FLOW.py.md` | |
| `api/tests/unit/test_cache_service.py` | Test | Unit tests for the cache service. | Active | | |
| `api/tests/unit/test_config.py` | Test | Unit tests for the config service. | Active | | |
| `api/tests/unit/test_crud.py` | Test | Unit tests for the CRUD operations. | Active | | |
| `api/tests/unit/test_deps.py` | Test | Unit tests for the FastAPI dependencies. | Active | | |
| `api/tests/unit/test_error_handler.py` | Test | Unit tests for the error handler. | Active | | |
| `api/tests/unit/test_error_handler_actions.py` | Test | Unit tests for the error handler actions. | Active | | |
| `api/tests/unit/test_flexible_logging.py` | Test | Unit tests for the flexible logging framework. | Active | | |
| `api/tests/unit/test_jwt_auth_db.py` | Test | Tests JWT registration/login and protected endpoints. | Active | | |
| `api/tests/unit/test_logging_config.py` | Test | Unit tests for the logging configuration. | Active | | |
| `api/tests/unit/test_metadata_service.py` | Test | Unit tests for the metadata service. | Active | | |
| `api/tests/unit/test_network_service.py` | Test | Unit tests for the network service. | Active | | |
| `api/tests/unit/test_new_logging_system.py` | Test | Unit tests for the new logging system. | Active | | |
| `api/tests/unit/test_notifications_service.py` | Test | Unit tests for the notifications service. | Active | | |
| `api/tests/unit/test_playlists_service.py` | Test | Unit tests for the playlists service. | Active | | |
| `api/tests/unit/test_search.py` | Test | Unit tests for the search service. | Active | | |
| `api/tests/unit/test_spoti_client.py` | Test | Unit tests for the Spotify client. | Active | | |
| `api/tests/unit/test_sync.py` | Test | Unit tests for the sync service. | Active | | |
| `api/tests/unit/test_tracks_service.py` | Test | Unit tests for the tracks service. | Active | | |
| `api/tests/unit/test_user_service.py` | Test | Unit tests for the user service. | Active | | |
| `api/tests/unit/test_user_service_db.py` | Test | Unit tests for the user service database interactions. | Active | | |
| `api/tests/unit/test_webhooks.py` | Test | Unit tests for the webhooks service. | Active | | |
| `api/tests/unit/providers/test_spotify_connector.py` | Test | Unit tests for the Spotify connector. | Active | | |
| `scripts/audit_api.py` | Script | Audits the API against its OpenAPI schema. | Active | `../reference/source/AUDIT_API.py.md` | |
| `scripts/audit_endpoints.py` | Script | Audits the API endpoints. | Active | `../reference/source/AUDIT_ENDPOINTS.py.md` | |
| `scripts/functional_test.py` | Script | Runs functional tests. | Active | `../reference/source/FUNCTIONAL_TEST.py.md` | |
| `scripts/generate_endpoints_doc.py` | Script | Generates `API_REFERENCE.md` from the OpenAPI schema. | Active | `../reference/source/GENERATE_ENDPOINTS_DOC.py.md` | |
| `scripts/generate_openapi.py` | Script | Builds the `openapi.json` schema from the FastAPI application. | Active | `../reference/source/GENERATE_OPENAPI.py.md` | |
| `scripts/linter.py` | Script | The unified project linter. | Active | `../reference/source/LINTER.py.md` | |
| `scripts/manage_docs_index.py` | Script | Manages the documentation index. | Active | | |
| `scripts/test_auth_flow.py` | Script | E2E test for the authentication flow. | Active | `../reference/source/TEST_AUTH_FLOW.py.md` | |
| `scripts/validate_code_index.py` | Script | Validates that all code files are registered in this index. | Active | | |
| `snitch/snitch.go` | Core | Main application file for the Snitch microservice. | Active | `../reference/source/SNITCH.go.md` | |
