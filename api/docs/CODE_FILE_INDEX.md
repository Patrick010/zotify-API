# Code File Index

This file is auto-generated. Do not edit manually.

| Path | Description |
|------|-------------|
| `api/alembic/env.py` | Alembic environment script, configures and runs migrations. |
| `api/alembic/versions/5f96175ff7c9_add_notifications_enabled_to_.py` | Alembic migration script to add notification settings to users. |
| `api/logging_config.yml` | Configuration file for the legacy logging system. |
| `api/logging_framework.yml` | Configuration for the flexible logging framework. |
| `api/src/zotify_api/auth_state.py` | Manages the state of user authentication. |
| `api/src/zotify_api/config.py` | Handles application configuration loading and management. |
| `api/src/zotify_api/core/error_handler/__init__.py` | Initializes the error handler module. |
| `api/src/zotify_api/core/error_handler/actions/__init__.py` | Initializes the error handler actions module. |
| `api/src/zotify_api/core/error_handler/actions/log_critical.py` | Error handler action to log critical errors. |
| `api/src/zotify_api/core/error_handler/actions/webhook.py` | Error handler action to send a webhook notification. |
| `api/src/zotify_api/core/error_handler/config.py` | Configuration for the error handling system. |
| `api/src/zotify_api/core/error_handler/formatter.py` | Formatter for error messages. |
| `api/src/zotify_api/core/error_handler/hooks.py` | Hooks for the error handling system. |
| `api/src/zotify_api/core/error_handler/triggers.py` | Triggers for the error handling system. |
| `api/src/zotify_api/core/logging_framework/__init__.py` | Initializes the flexible logging framework. |
| `api/src/zotify_api/core/logging_framework/filters.py` | Custom filters for the logging framework. |
| `api/src/zotify_api/core/logging_framework/schemas.py` | Pydantic schemas for the logging framework. |
| `api/src/zotify_api/core/logging_framework/service.py` | Service for the flexible logging framework. |
| `api/src/zotify_api/core/logging_handlers/__init__.py` | Initializes the logging handlers module. |
| `api/src/zotify_api/core/logging_handlers/base.py` | Base class for logging handlers. |
| `api/src/zotify_api/core/logging_handlers/console_handler.py` | Logging handler for console output. |
| `api/src/zotify_api/core/logging_handlers/database_job_handler.py` | Logging handler for database jobs. |
| `api/src/zotify_api/core/logging_handlers/json_audit_handler.py` | Logging handler for JSON audit logs. |
| `api/src/zotify_api/database/__init__.py` | Initializes the database module. |
| `api/src/zotify_api/database/crud.py` | Implements CRUD (Create, Read, Update, Delete) database operations. |
| `api/src/zotify_api/database/models.py` | Defines SQLAlchemy database models. |
| `api/src/zotify_api/database/session.py` | Manages database sessions. |
| `api/src/zotify_api/globals.py` | Defines global variables and constants. |
| `api/src/zotify_api/logging_config.py` | Configures the application's logging. |
| `api/src/zotify_api/main.py` | Main entry point for the FastAPI application. |
| `api/src/zotify_api/middleware/request_id.py` | Middleware to add a unique request ID to each request. |
| `api/src/zotify_api/models/config_models.py` | Pydantic models for application configuration. |
| `api/src/zotify_api/models/sync.py` | Pydantic models related to the sync functionality. |
| `api/src/zotify_api/providers/__init__.py` | Initializes the music providers module. |
| `api/src/zotify_api/providers/base.py` | Base class for music provider connectors. |
| `api/src/zotify_api/providers/spotify_connector.py` | Connector for the Spotify API. |
| `api/src/zotify_api/routes/__init__.py` | Initializes the API routes module. |
| `api/src/zotify_api/routes/auth.py` | Defines authentication-related API endpoints. |
| `api/src/zotify_api/routes/cache.py` | Defines cache management API endpoints. |
| `api/src/zotify_api/routes/config.py` | Defines configuration management API endpoints. |
| `api/src/zotify_api/routes/downloads.py` | Defines download-related API endpoints. |
| `api/src/zotify_api/routes/jwt_auth.py` | Defines JWT-based authentication endpoints. |
| `api/src/zotify_api/routes/network.py` | Defines network-related API endpoints. |
| `api/src/zotify_api/routes/notifications.py` | Defines notification-related API endpoints. |
| `api/src/zotify_api/routes/playlists.py` | Defines playlist-related API endpoints. |
| `api/src/zotify_api/routes/search.py` | Defines search-related API endpoints. |
| `api/src/zotify_api/routes/sync.py` | Defines sync-related API endpoints. |
| `api/src/zotify_api/routes/system.py` | Defines system-related API endpoints. |
| `api/src/zotify_api/routes/tracks.py` | Defines track-related API endpoints. |
| `api/src/zotify_api/routes/user.py` | Defines user-related API endpoints. |
| `api/src/zotify_api/routes/webhooks.py` | Defines webhook-related API endpoints. |
| `api/src/zotify_api/schemas/auth.py` | Pydantic models for authentication requests and responses. |
| `api/src/zotify_api/schemas/cache.py` | Pydantic models for cache management. |
| `api/src/zotify_api/schemas/download.py` | Pydantic models for download requests and responses. |
| `api/src/zotify_api/schemas/generic.py` | Generic Pydantic models used across the API. |
| `api/src/zotify_api/schemas/logging_schemas.py` | Pydantic models for logging. |
| `api/src/zotify_api/schemas/metadata.py` | Pydantic models for metadata. |
| `api/src/zotify_api/schemas/network.py` | Pydantic models for network-related data. |
| `api/src/zotify_api/schemas/notifications.py` | Pydantic models for notifications. |
| `api/src/zotify_api/schemas/playlists.py` | Pydantic models for playlists. |
| `api/src/zotify_api/schemas/spotify.py` | Pydantic models for Spotify-specific data. |
| `api/src/zotify_api/schemas/system.py` | Pydantic models for system-related data. |
| `api/src/zotify_api/schemas/tracks.py` | Pydantic models for tracks. |
| `api/src/zotify_api/schemas/user.py` | Pydantic models for user data. |
| `api/src/zotify_api/schemas/webhooks.py` | Pydantic models for webhooks. |
| `api/src/zotify_api/services/__init__.py` | Initializes the services module. |
| `api/src/zotify_api/services/auth.py` | Handles authentication logic and user management. |
| `api/src/zotify_api/services/cache_service.py` | Provides caching services for the application. |
| `api/src/zotify_api/services/config_service.py` | Provides configuration management services. |
| `api/src/zotify_api/services/db.py` | Provides database-related services. |
| `api/src/zotify_api/services/deps.py` | Defines FastAPI dependencies. |
| `api/src/zotify_api/services/download_service.py` | Handles download logic. |
| `api/src/zotify_api/services/jwt_service.py` | Handles JWT creation and validation. |
| `api/src/zotify_api/services/logging_service.py` | Provides logging services. |
| `api/src/zotify_api/services/metadata_service.py` | Handles metadata retrieval and processing. |
| `api/src/zotify_api/services/network_service.py` | Provides network-related services. |
| `api/src/zotify_api/services/notifications_service.py` | Handles sending notifications. |
| `api/src/zotify_api/services/playlists_service.py` | Handles playlist management. |
| `api/src/zotify_api/services/search.py` | Handles search queries. |
| `api/src/zotify_api/services/spoti_client.py` | Client for interacting with the Spotify API. |
| `api/src/zotify_api/services/sync_service.py` | Handles synchronization logic. |
| `api/src/zotify_api/services/tracks_service.py` | Handles track management. |
| `api/src/zotify_api/services/user_service.py` | Handles user management. |
| `api/src/zotify_api/services/webhooks.py` | Handles webhook logic. |
| `api/src/zotify_api/temp_violation.py` | Temporary file to test linter violations. |
| `api/tests/__init__.py` | Initializes the tests module. |
| `api/tests/conftest.py` | Pytest configuration and fixtures for the test suite. |
| `api/tests/test_cache.py` | Functional tests for the cache API endpoints. |
| `api/tests/test_config.py` | Functional tests for the config API endpoints. |
| `api/tests/test_download.py` | Functional tests for the download API endpoints. |
| `api/tests/test_network.py` | Functional tests for the network API endpoints. |
| `api/tests/test_notifications.py` | Functional tests for the notifications API endpoints. |
| `api/tests/test_playlists.py` | Functional tests for the playlists API endpoints. |
| `api/tests/test_system.py` | Functional tests for the system API endpoints. |
| `api/tests/test_tracks.py` | Functional tests for the tracks API endpoints. |
| `api/tests/test_user.py` | Functional tests for the user API endpoints. |
| `api/tests/unit/providers/test_spotify_connector.py` | Unit tests for the Spotify provider connector. |
| `api/tests/unit/test_auth.py` | Unit tests for the authentication service. |
| `api/tests/unit/test_cache_service.py` | Unit tests for the cache service. |
| `api/tests/unit/test_config.py` | Unit tests for the configuration service. |
| `api/tests/unit/test_crud.py` | Unit tests for the database CRUD operations. |
| `api/tests/unit/test_deps.py` | Unit tests for FastAPI dependencies. |
| `api/tests/unit/test_error_handler.py` | Unit tests for the error handling system. |
| `api/tests/unit/test_error_handler_actions.py` | Unit tests for the error handler actions. |
| `api/tests/unit/test_flexible_logging.py` | Unit tests for the flexible logging framework. |
| `api/tests/unit/test_jwt_auth_db.py` | Unit tests for the JWT authentication with database. |
| `api/tests/unit/test_logging_config.py` | Unit tests for the logging configuration. |
| `api/tests/unit/test_metadata_service.py` | Unit tests for the metadata service. |
| `api/tests/unit/test_network_service.py` | Unit tests for the network service. |
| `api/tests/unit/test_new_logging_system.py` | Unit tests for the new logging system. |
| `api/tests/unit/test_notifications_service.py` | Unit tests for the notifications service. |
| `api/tests/unit/test_playlists_service.py` | Unit tests for the playlists service. |
| `api/tests/unit/test_search.py` | Unit tests for the search service. |
| `api/tests/unit/test_spoti_client.py` | Unit tests for the Spotify client. |
| `api/tests/unit/test_sync.py` | Unit tests for the sync service. |
| `api/tests/unit/test_tracks_service.py` | Unit tests for the tracks service. |
| `api/tests/unit/test_user_service.py` | Unit tests for the user service. |
| `api/tests/unit/test_user_service_db.py` | Unit tests for the user service with database. |
| `api/tests/unit/test_webhooks.py` | Unit tests for the webhooks service. |
