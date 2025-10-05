# Code File Index

This document serves as the canonical registry of all code files in the Zotify API repository. Its purpose is to aid in developer discovery, navigation, and long-term maintainability.

| Path | Type | Description | Status | Linked Docs | Notes |
|------|------|-------------|--------|-------------|-------|
|`Gonk/GonkCLI/main.py`|Script| Main entry point for the Gonk command-line tool. |Active|||
|`Gonk/GonkCLI/modules/jwt_mock.py`|Core| A mock JWT generator for testing purposes. |Active|||
|`Gonk/GonkCLI/tests/test_jwt_mock.py`|Test| Unit tests for the mock JWT generator. |Active|||
|`Gonk/GonkUI/app.py`|Core| Main Flask application file for the Gonk Web UI. |Active|`../reference/source/APP.py.md`||
|`Gonk/GonkUI/static/app.js`|Core| JavaScript for the Gonk Web UI frontend. |Active|`../reference/source/APP.js.md`||
|`Gonk/GonkUI/views/jwt_ui.py`|Core| Flask view for the JWT generation UI. |Active|||
|`api/src/zotify_api/auth_state.py`|Core| Manages the state of user authentication. |Active|`../reference/source/AUTH_STATE.py.md`||
|`api/src/zotify_api/config.py`|Config| Handles application configuration loading and management. |Active|`../reference/source/CONFIG.py.md`||
|`api/src/zotify_api/globals.py`|Config| Defines global variables and constants. |Active|`../reference/source/GLOBALS.py.md`||
|`api/src/zotify_api/logging_config.py`|Config| Configures the application's logging. |Active|`../reference/source/LOGGING_CONFIG.py.md`||
|`api/src/zotify_api/main.py`|Core| Main entry point for the FastAPI application. |Active|`../reference/source/MAIN.py.md`||
|`api/src/zotify_api/core/error_handler/config.py`|Config| Configuration for the error handling system. |Active|`../reference/source/CONFIG.py.md`||
|`api/src/zotify_api/core/error_handler/formatter.py`|Core| Formatter for error messages. |Active|`../reference/source/FORMATTER.py.md`||
|`api/src/zotify_api/core/error_handler/hooks.py`|Core| Hooks for the error handling system. |Active|`../reference/source/HOOKS.py.md`||
|`api/src/zotify_api/core/error_handler/triggers.py`|Core| Triggers for the error handling system. |Active|`../reference/source/TRIGGERS.py.md`||
|`api/src/zotify_api/core/error_handler/actions/log_critical.py`|Core| Error handler action to log critical errors. |Active|`../reference/source/LOG_CRITICAL.py.md`||
|`api/src/zotify_api/core/error_handler/actions/webhook.py`|Core| Error handler action to send a webhook notification. |Active|`../reference/source/WEBHOOK.py.md`||
|`api/src/zotify_api/core/logging_framework/filters.py`|Core| Custom filters for the logging framework. |Active|`../reference/source/FILTERS.py.md`||
|`api/src/zotify_api/core/logging_framework/schemas.py`|Model| Pydantic schemas for the logging framework. |Active|`../reference/source/SCHEMAS.py.md`||
|`api/src/zotify_api/core/logging_framework/service.py`|Core| Service for the flexible logging framework. |Active|`../reference/source/SERVICE.py.md`||
|`api/src/zotify_api/core/logging_handlers/base.py`|Core| Base class for logging handlers. |Active|`../reference/source/BASE.py.md`||
|`api/src/zotify_api/core/logging_handlers/console_handler.py`|Core| Logging handler for console output. |Active|`../reference/source/CONSOLE_HANDLER.py.md`||
|`api/src/zotify_api/core/logging_handlers/database_job_handler.py`|Core| Logging handler for database jobs. |Active|`../reference/source/DATABASE_JOB_HANDLER.py.md`||
|`api/src/zotify_api/core/logging_handlers/json_audit_handler.py`|Core| Logging handler for JSON audit logs. |Active|`../reference/source/JSON_AUDIT_HANDLER.py.md`||
|`api/src/zotify_api/database/crud.py`|Core| Implements CRUD (Create, Read, Update, Delete) database operations. |Active|`../reference/source/CRUD.py.md`||
|`api/src/zotify_api/database/models.py`|Model| Defines SQLAlchemy database models. |Active|`../reference/source/MODELS.py.md`||
|`api/src/zotify_api/database/session.py`|Core| Manages database sessions. |Active|`../reference/source/SESSION.py.md`||
|`api/src/zotify_api/middleware/request_id.py`|Core| Middleware to add a unique request ID to each request. |Active|`../reference/source/REQUEST_ID.py.md`||
|`api/src/zotify_api/models/config_models.py`|Model| Pydantic models for application configuration. |Active|`../reference/source/CONFIG_MODELS.py.md`||
|`api/src/zotify_api/models/sync.py`|Model| Pydantic models related to the sync functionality. |Active|`../reference/source/SYNC.py.md`||
|`api/src/zotify_api/providers/base.py`|Core| Base class for music provider connectors. |Active|`../reference/source/BASE.py.md`||
|`api/src/zotify_api/providers/spotify_connector.py`|Core| Connector for the Spotify API. |Active|`../reference/source/SPOTIFY_CONNECTOR.py.md`||
|`api/src/zotify_api/routes/auth.py`|Route| Defines authentication-related API endpoints. |Active|`../reference/source/AUTH.py.md`||
|`api/src/zotify_api/routes/cache.py`|Route| Defines cache management API endpoints. |Active|`../reference/source/CACHE.py.md`||
|`api/src/zotify_api/routes/config.py`|Route| Defines configuration management API endpoints. |Active|`../reference/source/CONFIG.py.md`||
|`api/src/zotify_api/routes/downloads.py`|Route| Defines download-related API endpoints. |Active|`../reference/source/DOWNLOADS.py.md`||
|`api/src/zotify_api/routes/jwt_auth.py`|Route| Defines JWT-based authentication endpoints. |Active||Protects user-specific endpoints.|
|`api/src/zotify_api/routes/network.py`|Route| Defines network-related API endpoints. |Active|`../reference/source/NETWORK.py.md`||
|`api/src/zotify_api/routes/notifications.py`|Route| Defines notification-related API endpoints. |Active|`../reference/source/NOTIFICATIONS.py.md`||
|`api/src/zotify_api/routes/playlists.py`|Route| Defines playlist-related API endpoints. |Active|`../reference/source/PLAYLISTS.py.md`||
|`api/src/zotify_api/routes/search.py`|Route| Defines search-related API endpoints. |Active|`../reference/source/SEARCH.py.md`||
|`api/src/zotify_api/routes/sync.py`|Route| Defines sync-related API endpoints. |Active|`../reference/source/SYNC.py.md`||
|`api/src/zotify_api/routes/system.py`|Route| Defines system-related API endpoints. |Active|`../reference/source/SYSTEM.py.md`||
|`api/src/zotify_api/routes/tracks.py`|Route| Defines track-related API endpoints. |Active|`../reference/source/TRACKS.py.md`||
|`api/src/zotify_api/routes/user.py`|Route| Defines user-related API endpoints. |Active|`../reference/source/USER.py.md`|Secured by JWT.|
|`api/src/zotify_api/routes/webhooks.py`|Route| Defines webhook-related API endpoints. |Active|`../reference/source/WEBHOOKS.py.md`||
|`api/src/zotify_api/schemas/auth.py`|Model| Pydantic models for authentication requests and responses. |Active|`../reference/source/AUTH.py.md`||
|`api/src/zotify_api/schemas/cache.py`|Model| Pydantic models for cache management. |Active|`../reference/source/CACHE.py.md`||
|`api/src/zotify_api/schemas/download.py`|Model| Pydantic models for download requests and responses. |Active|`../reference/source/DOWNLOAD.py.md`||
|`api/src/zotify_api/schemas/generic.py`|Model| Generic Pydantic models used across the API. |Active|`../reference/source/GENERIC.py.md`||
|`api/src/zotify_api/schemas/logging_schemas.py`|Model| Pydantic models for logging. |Active|`../reference/source/LOGGING_SCHEMAS.py.md`||
|`api/src/zotify_api/schemas/metadata.py`|Model| Pydantic models for metadata. |Active|`../reference/source/METADATA.py.md`||
|`api/src/zotify_api/schemas/network.py`|Model| Pydantic models for network-related data. |Active|`../reference/source/NETWORK.py.md`||
|`api/src/zotify_api/schemas/notifications.py`|Model| Pydantic models for notifications. |Active|`../reference/source/NOTIFICATIONS.py.md`||
|`api/src/zotify_api/schemas/playlists.py`|Model| Pydantic models for playlists. |Active|`../reference/source/PLAYLISTS.py.md`||
|`api/src/zotify_api/schemas/spotify.py`|Model| Pydantic models for Spotify-specific data. |Active|`../reference/source/SPOTIFY.py.md`||
|`api/src/zotify_api/schemas/system.py`|Model| Pydantic models for system-related data. |Active|`../reference/source/SYSTEM.py.md`||
|`api/src/zotify_api/schemas/tracks.py`|Model| Pydantic models for tracks. |Active|`../reference/source/TRACKS.py.md`||
|`api/src/zotify_api/schemas/user.py`|Model| Pydantic models for user data. |Active|`../reference/source/USER.py.md`||
|`api/src/zotify_api/schemas/webhooks.py`|Model| Pydantic models for webhooks. |Active|`../reference/source/WEBHOOKS.py.md`||
|`api/src/zotify_api/services/auth.py`|Core| Handles authentication logic and user management. |Active|`../reference/source/AUTH.py.md`||
|`api/src/zotify_api/services/cache_service.py`|Core| Provides caching services for the application. |Active|`../reference/source/CACHE_SERVICE.py.md`||
|`api/src/zotify_api/services/config_service.py`|Core| Provides configuration management services. |Active|`../reference/source/CONFIG_SERVICE.py.md`||
|`api/src/zotify_api/services/db.py`|Core| Provides database-related services. |Active|`../reference/source/DB.py.md`||
|`api/src/zotify_api/services/deps.py`|Core| Defines FastAPI dependencies. |Active|`../reference/source/DEPS.py.md`||
|`api/src/zotify_api/services/download_service.py`|Core| Handles download logic. |Active|`../reference/source/DOWNLOAD_SERVICE.py.md`||
|`api/src/zotify_api/services/jwt_service.py`|Core| Handles JWT creation and validation. |Active|||
|`api/src/zotify_api/services/logging_service.py`|Core| Provides logging services. |Active|`../reference/source/LOGGING_SERVICE.py.md`||
|`api/src/zotify_api/services/metadata_service.py`|Core| Handles metadata retrieval and processing. |Active|`../reference/source/METADATA_SERVICE.py.md`||
|`api/src/zotify_api/services/network_service.py`|Core| Provides network-related services. |Active|`../reference/source/NETWORK_SERVICE.py.md`||
|`api/src/zotify_api/services/notifications_service.py`|Core| Handles sending notifications. |Active|`../reference/source/NOTIFICATIONS_SERVICE.py.md`||
|`api/src/zotify_api/services/playlists_service.py`|Core| Handles playlist management. |Active|`../reference/source/PLAYLISTS_SERVICE.py.md`||
|`api/src/zotify_api/services/search.py`|Core| Handles search queries. |Active|`../reference/source/SEARCH.py.md`||
|`api/src/zotify_api/services/spoti_client.py`|Core| Client for interacting with the Spotify API. |Active|`../reference/source/SPOTI_CLIENT.py.md`||
|`api/src/zotify_api/services/sync_service.py`|Core| Handles synchronization logic. |Active|`../reference/source/SYNC_SERVICE.py.md`||
|`api/src/zotify_api/services/tracks_service.py`|Core| Handles track management. |Active|`../reference/source/TRACKS_SERVICE.py.md`||
|`api/src/zotify_api/services/user_service.py`|Core| Handles user management. |Active|`../reference/source/USER_SERVICE.py.md`||
|`api/src/zotify_api/services/webhooks.py`|Core| Handles webhook logic. |Active|`../reference/source/WEBHOOKS.py.md`||
|`api/tests/conftest.py`|Test| Pytest configuration and fixtures for the test suite. |Active|||
|`api/tests/test_cache.py`|Test| Functional tests for the cache API endpoints. |Active|||
|`api/tests/test_config.py`|Test| Functional tests for the config API endpoints. |Active|||
|`api/tests/test_download.py`|Test| Functional tests for the download API endpoints. |Active|||
|`api/tests/test_network.py`|Test| Functional tests for the network API endpoints. |Active|||
|`api/tests/test_notifications.py`|Test| Functional tests for the notifications API endpoints. |Active|||
|`api/tests/test_playlists.py`|Test| Functional tests for the playlists API endpoints. |Active|||
|`api/tests/test_system.py`|Test| Functional tests for the system API endpoints. |Active|||
|`api/tests/test_tracks.py`|Test| Functional tests for the tracks API endpoints. |Active|||
|`api/tests/test_user.py`|Test| Functional tests for the user API endpoints. |Active|||
|`api/tests/unit/test_auth.py`|Test| Unit tests for the authentication service. |Active|`../reference/source/TEST_AUTH_FLOW.py.md`||
|`api/tests/unit/test_cache_service.py`|Test| Unit tests for the cache service. |Active|||
|`api/tests/unit/test_config.py`|Test| Unit tests for the configuration service. |Active|||
|`api/tests/unit/test_crud.py`|Test| Unit tests for the database CRUD operations. |Active|||
|`api/tests/unit/test_deps.py`|Test| Unit tests for FastAPI dependencies. |Active|||
|`api/tests/unit/test_error_handler.py`|Test| Unit tests for the error handling system. |Active|||
|`api/tests/unit/test_error_handler_actions.py`|Test| Unit tests for the error handler actions. |Active|||
|`api/tests/unit/test_flexible_logging.py`|Test| Unit tests for the flexible logging framework. |Active|||
|`api/tests/unit/test_jwt_auth_db.py`|Test| Unit tests for the JWT authentication with database. |Active|||
|`api/tests/unit/test_logging_config.py`|Test| Unit tests for the logging configuration. |Active|||
|`api/tests/unit/test_metadata_service.py`|Test| Unit tests for the metadata service. |Active|||
|`api/tests/unit/test_network_service.py`|Test| Unit tests for the network service. |Active|||
|`api/tests/unit/test_new_logging_system.py`|Test| Unit tests for the new logging system. |Active|||
|`api/tests/unit/test_notifications_service.py`|Test| Unit tests for the notifications service. |Active|||
|`api/tests/unit/test_playlists_service.py`|Test| Unit tests for the playlists service. |Active|||
|`api/tests/unit/test_search.py`|Test| Unit tests for the search service. |Active|||
|`api/tests/unit/test_spoti_client.py`|Test| Unit tests for the Spotify client. |Active|||
|`api/tests/unit/test_sync.py`|Test| Unit tests for the sync service. |Active|||
|`api/tests/unit/test_tracks_service.py`|Test| Unit tests for the tracks service. |Active|||
|`api/tests/unit/test_user_service.py`|Test| Unit tests for the user service. |Active|||
|`api/tests/unit/test_user_service_db.py`|Test| Unit tests for the user service with database. |Active|||
|`api/tests/unit/test_webhooks.py`|Test| Unit tests for the webhooks service. |Active|||
|`api/tests/unit/providers/test_spotify_connector.py`|Test| Unit tests for the Spotify provider connector. |Active|||
|`scripts/audit_api.py`|Script| A script to audit the API. |Active|`../reference/source/AUDIT_API.py.md`||
|`scripts/audit_endpoints.py`|Script| A script to audit the API endpoints. |Active|`../reference/source/AUDIT_ENDPOINTS.py.md`||
|`scripts/functional_test.py`|Script| A script for running functional tests. |Active|`../reference/source/FUNCTIONAL_TEST.py.md`||
|`scripts/generate_endpoints_doc.py`|Script| A script to generate documentation for the API endpoints. |Active|`../reference/source/GENERATE_ENDPOINTS_DOC.py.md`||
|`scripts/generate_openapi.py`|Script| A script to generate the OpenAPI specification. |Active|`../reference/source/GENERATE_OPENAPI.py.md`||
|`scripts/linter.py`|Script| The main linter script. |Active|`../reference/source/LINTER.py.md`||
|`scripts/manage_docs_index.py`|Script| A script to manage the documentation index. |Active|||
|`scripts/test_auth_flow.py`|Script| A script to test the authentication flow. |Active|`../reference/source/TEST_AUTH_FLOW.py.md`||
|`scripts/validate_code_index.py`|Script| A script to validate the code index. |Active|||
|`snitch/snitch.go`|Core| The main Go source file for the snitch module. |Active|`../reference/source/SNITCH.go.md`||
|`.github/workflows/ci.yml`|Config| Defines the Continuous Integration (CI) pipeline for running tests, linting, and security scans. |Active||Auto-generated to fix audit|
|`.github/workflows/pushmirror.yml`|Config| GitHub Actions workflow to mirror the repository to another location on merge. |Active||Auto-generated to fix audit|
|`Gonk/GonkCLI/__init__.py`|Code| Initializes the GonkCLI Python package. |Active||Auto-generated to fix audit|
|`Gonk/GonkCLI/modules/__init__.py`|Code| Initializes the modules for the GonkCLI. |Active||Auto-generated to fix audit|
|`Gonk/GonkCLI/tests/__init__.py`|Code| Initializes the test suite for the GonkCLI. |Active||Auto-generated to fix audit|
|`Gonk/GonkUI/views/__init__.py`|Code| Initializes the views module for the Gonk Web UI. |Active||Auto-generated to fix audit|
| `TRACE_INDEX.yml` | Config | TBD | Active | | Auto-generated to fix audit |
|`api/alembic/env.py`|Code| Alembic environment script, configures and runs migrations. |Active||Auto-generated to fix audit|
|`api/alembic/versions/5f96175ff7c9_add_notifications_enabled_to_.py`|Code| Alembic migration script to add notification settings to users. |Active||Auto-generated to fix audit|
|`api/api_dumps/cache.json`|Config| JSON dump of the API cache for debugging or analysis. |Active||Auto-generated to fix audit|
|`api/api_dumps/downloads.json`|Config| JSON dump of the downloads endpoint for debugging or analysis. |Active||Auto-generated to fix audit|
|`api/api_dumps/logging.json`|Config| JSON dump of the logging endpoint for debugging or analysis. |Active||Auto-generated to fix audit|
|`api/api_dumps/metadata.json`|Config| JSON dump of the metadata endpoint for debugging or analysis. |Active||Auto-generated to fix audit|
|`api/api_dumps/network.json`|Config| JSON dump of the network endpoint for debugging or analysis. |Active||Auto-generated to fix audit|
|`api/api_dumps/playlist.json`|Config| JSON dump of the playlist endpoint for debugging or analysis. |Active||Auto-generated to fix audit|
|`api/api_dumps/spotify.json`|Config| JSON dump of the spotify endpoint for debugging or analysis. |Active||Auto-generated to fix audit|
|`api/api_dumps/stubs.json`|Config| JSON dump of API stubs for testing or development. |Active||Auto-generated to fix audit|
|`api/api_dumps/sync.json`|Config| JSON dump of the sync endpoint for debugging or analysis. |Active||Auto-generated to fix audit|
|`api/api_dumps/system.json`|Config| JSON dump of the system endpoint for debugging or analysis. |Active||Auto-generated to fix audit|
|`api/api_dumps/tracks.json`|Config| JSON dump of the tracks endpoint for debugging or analysis. |Active||Auto-generated to fix audit|
|`api/api_dumps/user.json`|Config| JSON dump of the user endpoint for debugging or analysis. |Active||Auto-generated to fix audit|
|`api/docs/system/zotify-openapi-external-v1.json`|Config| External OpenAPI (v1) specification in JSON format. |Active||Auto-generated to fix audit|
|`api/docs/system/zotify-openapi-external-v1.yaml`|Config| External OpenAPI (v1) specification in YAML format. |Active||Auto-generated to fix audit|
|`api/logging_config.yml`|Config| Configuration file for the legacy logging system. |Active||Auto-generated to fix audit|
|`api/logging_framework.yml`|Config| Configuration for the flexible logging framework. |Active||Auto-generated to fix audit|
|`api/src/storage/spotify_tokens.json`|Config| Storage file for Spotify API tokens. |Active||Auto-generated to fix audit|
|`api/src/zotify_api/core/error_handler/__init__.py`|Code| Initializes the error handler module. |Active||Auto-generated to fix audit|
|`api/src/zotify_api/core/error_handler/actions/__init__.py`|Code| Initializes the error handler actions module. |Active||Auto-generated to fix audit|
|`api/src/zotify_api/core/logging_framework/__init__.py`|Code| Initializes the flexible logging framework. |Active||Auto-generated to fix audit|
|`api/src/zotify_api/core/logging_handlers/__init__.py`|Code| Initializes the logging handlers module. |Active||Auto-generated to fix audit|
|`api/src/zotify_api/database/__init__.py`|Code| Initializes the database module. |Active||Auto-generated to fix audit|
|`api/src/zotify_api/providers/__init__.py`|Code| Initializes the music providers module. |Active||Auto-generated to fix audit|
|`api/src/zotify_api/routes/__init__.py`|Code| Initializes the API routes module. |Active||Auto-generated to fix audit|
|`api/src/zotify_api/services/__init__.py`|Code| Initializes the services module. |Active||Auto-generated to fix audit|
|`api/src/zotify_api/storage/user_data.json`|Config| Storage file for user data. |Active||Auto-generated to fix audit|
|`api/tests/__init__.py`|Code| Initializes the tests module. |Active||Auto-generated to fix audit|
|`project/api/endpoints.yaml`|Config| A list of API endpoints. |Active||Auto-generated to fix audit|
|`scripts/doc-lint-rules.yml`|Config| A set of rules for the documentation linter. |Active||Auto-generated to fix audit|
|`scripts/make_manifest.py`|Code| A script to create a manifest of all project files. |Active||Auto-generated to fix audit|
|`scripts/repo_inventory_and_governance.py`|Code| A script to manage the repository inventory and governance. |Active||Auto-generated to fix audit|
|`scripts/run_e2e_auth_test.sh`|Script| A script to run the end-to-end authentication tests. |Active||Auto-generated to fix audit|
|`scripts/start.sh`|Script| A script to start the application. |Active||Auto-generated to fix audit|
|`scripts/test_single_config.sh`|Script| A script to test a single configuration. |Active||Auto-generated to fix audit|
|`api/src/zotify_api/temp_violation.py`|| Temporary file to test linter violations. |Active|||
