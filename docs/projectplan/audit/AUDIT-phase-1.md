# **AUDIT-phase-1: Comprehensive API & Documentation Reality Audit (Corrected v5)**

**Date:** 2025-08-10
**Author:** Jules
**Version:** 5.0 (This version incorporates the definitive file list provided by the user, correcting all previous inventory errors. This is the final baseline.)
**Objective:** To provide a definitive, unvarnished, and brutally honest analysis of the Zotify API's current implementation versus its documented design, plans, and specifications. This document serves as the new, single source of truth and baseline for all future project planning and development.

---

## **Part 1: The Reality — Codebase & Functional Audit**

### **1.1: Complete API Endpoint Inventory (Exhaustive)**

This table provides the definitive list of every unique API endpoint path found in the codebase, its methods, current implementation status, and its primary function.

| Endpoint | Method(s) | Status | Function |
| :--- | :--- | :--- | :--- |
| `/ping` | GET | ✅ Functional | Performs a basic health check. |
| `/health` | GET | ✅ Functional | Performs a basic health check. |
| `/version` | GET | ✅ Functional | Returns application version information. |
| `/openapi.json` | GET | ✅ Functional | Returns the auto-generated OpenAPI 3.0 specification. |
| `/api/schema` | GET | ✅ Functional | Returns schema components from the OpenAPI spec. |
| **Authentication Module** | | | |
| `/api/auth/spotify/callback`| POST | ✅ Functional | The primary, secure callback for the OAuth flow. |
| `/api/auth/status` | GET | ✅ Functional | Checks if the current Spotify token is valid. |
| `/api/auth/logout` | POST | ✅ Functional | Clears local Spotify tokens to log the user out. |
| `/api/auth/refresh` | GET | ✅ Functional | Uses the refresh token to get a new Spotify access token. |
| **Spotify Module** | | | |
| `/api/spotify/login` | GET | ✅ Functional | Generates the URL for the user to log in to Spotify. |
| `/api/spotify/callback` | GET | ⚠️ **Redundant** | Legacy, insecure OAuth callback. Should be removed. |
| `/api/spotify/token_status`| GET | ✅ Functional | Checks the status of the locally stored token. |
| `/api/spotify/sync_playlists`| POST | ✅ Functional | Triggers a full sync of all user playlists from Spotify. |
| `/api/spotify/playlists`| GET, POST | ✅ Functional | Lists all of the current user's playlists or creates a new one. |
| `/api/spotify/playlists/{id}`| GET, PUT, DELETE| ✅ Functional | Gets, updates details for, or unfollows a specific playlist. |
| `/api/spotify/playlists/{id}/tracks`| GET, POST, DELETE| ✅ Functional | Gets, adds, or removes tracks from a specific playlist. |
| `/api/spotify/me` | GET | ✅ Functional | Gets the current user's full Spotify profile object. |
| `/api/spotify/devices` | GET | ✅ Functional | Gets the user's available Spotify playback devices. |
| **Search Module** | | | |
| `/api/search` | GET | ✅ Functional | Performs a search for content on Spotify. |
| **Local Metadata & Tracks** | | | |
| `/api/tracks/metadata`| POST | ✅ Functional | Retrieves metadata for a batch of track IDs from the Spotify API. |
| `/api/metadata/{id}` | GET, PATCH | ✅ Functional | Gets or updates extended, local-only metadata for a track. |
| `/api/playlists` | GET, POST | ✅ Functional | Manages local (non-Spotify) playlists. |
| `/api/tracks` | GET, POST, DELETE| ✅ Functional | Manages the local track database. |
| `/api/tracks/{id}` | GET, PATCH | ✅ Functional | Gets or updates a specific track in the local database. |
| `/api/tracks/{id}/cover`| POST | ✅ Functional | Uploads a cover image for a locally tracked item. |
| **System & Config** | | | |
| `/api/system/uptime` | GET | ✅ Functional | Returns the server's uptime. |
| `/api/system/env` | GET | ✅ Functional | Returns server environment information. |
| `/api/system/status` | GET | ❌ **Stub** | Stub for providing system status. |
| `/api/system/storage`| GET | ❌ **Stub** | Stub for providing storage information. |
| `/api/system/logs` | GET | ❌ **Stub** | Stub for retrieving system logs. |
| `/api/system/reload` | POST | ❌ **Stub** | Stub for triggering a configuration reload. |
| `/api/system/reset` | POST | ❌ **Stub** | Stub for triggering a system reset. |
| `/api/config` | GET, PATCH | ✅ Functional | Retrieves or updates application configuration. |
| `/api/config/reset`| POST | ✅ Functional | Resets the configuration to its default state. |
| **Downloads** | | | |
| `/api/download` | POST | ❌ **Stub** | Stub for initiating a download. |
| `GET /api/download/status`| GET | ❌ **Stub** | Stub for checking a download's status. |
| `/api/downloads/status`| GET | ✅ Functional | Gets the status of the local download queue. |
| `/api/downloads/retry`| POST | ✅ Functional | Retries failed items in the local download queue. |
| **Other Modules** | | | |
| `/api/cache` | GET, DELETE | ✅ Functional | Manages the application's cache. |
| `/api/logging` | GET, PATCH | ✅ Functional | Manages application logging levels. |
| `/api/network` | GET, PATCH | ✅ Functional | Manages network configuration. |
| `/api/notifications`| POST | ✅ Functional | Creates a new user notification. |
| `/api/notifications/{user_id}`| GET | ✅ Functional | Retrieves notifications for a specific user. |
| `/api/notifications/{notification_id}`| PATCH | ✅ Functional | Marks a specific notification as read. |
| `/api/sync/trigger`| POST | ✅ Functional | Triggers a generic sync job. |
| `/api/sync/playlist/sync`| POST | ✅ Functional | Triggers a playlist sync job. |
| `/api/user/profile`| GET, PATCH | ✅ Functional | Gets or updates the local user's profile. |
| `/api/user/preferences`| GET, PATCH | ✅ Functional | Gets or updates the local user's preferences. |
| `/api/user/liked`| GET | ✅ Functional | Retrieves the user's liked songs from local storage. |
| `/api/user/sync_liked`| POST | ✅ Functional | Triggers a sync of the user's liked songs. |
| `/api/user/history`| GET, DELETE | ✅ Functional | Gets or clears the user's local listening history. |
| `/api/webhooks`| GET, POST | ✅ Functional | Lists all registered webhooks or registers a new one. |
| `/api/webhooks/{hook_id}`| DELETE | ✅ Functional | Deletes a specific registered webhook. |
| `/api/webhooks/fire`| POST | ✅ Functional | Manually fires a webhook for testing. |

### **1.2: Complete Code File Inventory (.py & .go only)**

This table provides the definitive list of all `.py` and `.go` source files as provided by the user.

| File Path | Purpose |
| :--- | :--- |
| **`./api/src/zotify_api/routes/`** | **API Route Definitions** |
| `./api/src/zotify_api/routes/config.py` | Defines endpoints for managing application configuration. |
| `./api/src/zotify_api/routes/network.py` | Defines endpoints for managing network configuration. |
| `./api/src/zotify_api/routes/spotify.py` | Defines all Spotify-specific interaction endpoints. |
| `./api/src/zotify_api/routes/webhooks.py` | Defines endpoints for managing webhooks. |
| `./api/src/zotify_api/routes/notifications.py`| Defines endpoints for user notifications. |
| `./api/src/zotify_api/routes/search.py` | Defines the primary search endpoint for Spotify. |
| `./api/src/zotify_api/routes/cache.py` | Defines endpoints for managing the application cache. |
| `./api/src/zotify_api/routes/tracks.py` | Defines endpoints for managing the local tracks database. |
| `./api/src/zotify_api/routes/logging.py` | Defines endpoints for managing logging levels. |
| `./api/src/zotify_api/routes/playlist.py` | Defines endpoints for managing local playlists. |
| `./api/src/zotify_api/routes/auth.py` | Defines all authentication-related API endpoints. |
| `./api/src/zotify_api/routes/stubs.py` | Defines explicitly unimplemented endpoints that return 501. |
| `./api/src/zotify_api/routes/metadata.py` | Defines endpoints for managing local metadata. |
| `./api/src/zotify_api/routes/downloads.py` | Defines endpoints for managing the download queue. |
| `./api/src/zotify_api/routes/sync.py` | Defines endpoints for triggering background synchronization jobs. |
| `./api/src/zotify_api/routes/system.py` | Defines endpoints for retrieving system information and status. |
| `./api/src/zotify_api/routes/user.py` | Defines endpoints for managing the local user profile. |
| **`./api/src/zotify_api/`** | **Core API Logic** |
| `./api/src/zotify_api/config.py` | Handles loading and managing API-specific settings. |
| `./api/src/zotify_api/logging_config.py`| Configures the application's logging setup. |
| `./api/src/zotify_api/main.py` | The main FastAPI application entrypoint and router configuration. |
| `./api/src/zotify_api/globals.py`| Stores global variables and application-wide objects. |
| `./api/src/zotify_api/auth_state.py`| Manages global authentication state and token storage. |
| `./api/src/zotify_api/database.py`| Contains database connection and session management logic. |
| **`./api/src/zotify_api/models/`** | **Data Models** |
| `./api/src/zotify_api/models/config.py` | Data models related to configuration. |
| `./api/src/zotify_api/models/spotify.py` | Data models related to Spotify objects. |
| `./api/src/zotify_api/models/sync.py` | Data models related to synchronization jobs. |
| **`./api/src/zotify_api/middleware/`** | **API Middleware** |
| `./api/src/zotify_api/middleware/request_id.py`| Middleware for adding a unique request ID to logs for traceability. |
| **`./api/src/zotify_api/schemas/`** | **Pydantic Schemas** |
| `./api/src/zotify_api/schemas/network.py` | Pydantic models for the Network module. |
| `./api/src/zotify_api/schemas/spotify.py` | Pydantic models for the Spotify module. |
| `./api/src/zotify_api/schemas/notifications.py`| Pydantic models for the Notifications module. |
| `./api/src/zotify_api/schemas/cache.py` | Pydantic models for the Cache module. |
| `./api/src/zotify_api/schemas/tracks.py` | Pydantic models for the local Tracks module. |
| `./api/src/zotify_api/schemas/logging.py` | Pydantic models for the Logging module. |
| `./api/src/zotify_api/schemas/auth.py` | Pydantic models for the Authentication module. |
| `./api/src/zotify_api/schemas/metadata.py` | Pydantic models for the local Metadata module. |
| `./api/src/zotify_api/schemas/playlists.py`| Pydantic models for the local Playlists module. |
| `./api/src/zotify_api/schemas/downloads.py`| Pydantic models for the Downloads module. |
| `./api/src/zotify_api/schemas/generic.py` | Generic response models (e.g., message, status) for the API. |
| `./api/src/zotify_api/schemas/system.py` | Pydantic models for the System module. |
| `./api/src/zotify_api/schemas/user.py` | Pydantic models for the User module. |
| **`./api/src/zotify_api/services/`** | **Business Logic Services** |
| `./api/src/zotify_api/services/sync_service.py` | Business logic for background synchronization jobs. |
| `./api/src/zotify_api/services/notifications_service.py`| Business logic for user notifications. |
| `./api/src/zotify_api/services/spoti_client.py`| **CRITICAL:** The central client for all Spotify API communication. |
| `./api/src/zotify_api/services/spotify.py` | Service functions that bridge routes to the SpotiClient. |
| `./api/src/zotify_api/services/user_service.py` | Business logic for local user profile management. |
| `./api/src/zotify_api/services/playlists_service.py`| Business logic for local playlist management. |
| `./api/src/zotify_api/services/webhooks.py` | Business logic for webhook management. |
| `./api/src/zotify_api/services/metadata_service.py` | Business logic for local metadata management. |
| `./api/src/zotify_api/services/search.py` | Business logic for the search feature. |
| `./api/src/zotify_api/services/db.py` | Utility functions for database interactions. |
| `./api/src/zotify_api/services/config_service.py` | Business logic for configuration management. |
| `./api/src/zotify_api/services/deps.py` | FastAPI dependencies for injection into route handlers. |
| `./api/src/zotify_api/services/__init__.py` | Makes the services directory a Python package. |
| `./api/src/zotify_api/services/auth.py` | Business logic for all authentication flows. |
| `./api/src/zotify_api/services/logging_service.py` | Business logic for logging management. |
| `./api/src/zotify_api/services/cache_service.py` | Business logic for cache management. |
| `./api/src/zotify_api/services/tracks_service.py` | Business logic for local tracks management. |
| `./api/src/zotify_api/services/network_service.py` | Business logic for network configuration. |
| `./api/src/zotify_api/services/downloads_service.py`| Business logic for the download queue. |
| **`./api/` (Root)** | **API Root Files** |
| `./api/minimal_test_app.py` | A minimal FastAPI app for testing purposes. |
| `./api/test_minimal_app.py` | A script to test the minimal FastAPI application. |
| `./api/route_audit.py` | A Python script to audit API routes. |
| **`./api/tests/`** | **Integration Tests** |
| `./api/tests/test_notifications.py`| Integration tests for the Notifications module. |
| `./api/tests/test_logging.py`| Integration tests for the Logging module. |
| `./api/tests/test_network.py`| Integration tests for the Network module. |
| `./api/tests/test_sync.py`| Integration tests for the Sync module. |
| `./api/tests/test_tracks.py`| Integration tests for the Tracks module. |
| `./api/tests/__init__.py` | Makes the tests directory a Python package. |
| `./api/tests/test_user.py`| Integration tests for the User module. |
| `./api/tests/test_downloads.py`| Integration tests for the Downloads module. |
| `./api/tests/test_system.py`| Integration tests for the System module. |
| `./api/tests/test_config.py`| Integration tests for the Config module. |
| `./api/tests/test_stubs.py`| Tests that confirm stubbed endpoints return a 501 error. |
| `./api/tests/test_playlists.py`| Integration tests for the local Playlists module. |
| `./api/tests/conftest.py`| Pytest configuration and shared fixtures for integration tests. |
| `./api/tests/test_cache.py`| Integration tests for the Cache module. |
| `./api/tests/test_metadata.py`| Integration tests for the Metadata module. |
| `./api/tests/test_spotify.py`| Integration tests for the Spotify module. |
| **`./api/tests/unit/`** | **Unit Tests** |
| `./api/tests/unit/test_playlists_service.py`| Unit tests for the local playlists service logic. |
| `./api/tests/unit/test_spoti_client.py`| Unit tests for the central SpotiClient. |
| `./api/tests/unit/test_sync.py`| Unit tests for the sync service logic. |
| `./api/tests/unit/test_network_service.py`| Unit tests for the network service logic. |
| `./api/tests/unit/test_cache_service.py`| Unit tests for the cache service logic. |
| `./api/tests/unit/test_new_endpoints.py`| Integration tests for recently added endpoints. |
| `./api/tests/unit/test_config.py`| Placeholder for config service unit tests. |
| `./api/tests/unit/test_auth.py` | Unit tests for the authentication service and routes. |
| `./api/tests/unit/test_metadata_service.py`| Unit tests for the metadata service logic. |
| `./api/tests/unit/test_tracks_service.py`| Unit tests for the tracks service logic. |
| `./api/tests/unit/test_webhooks.py`| Unit tests for the webhooks service logic. |
| `./api/tests/unit/test_search.py`| Unit tests for the Search endpoint. |
| `./api/tests/unit/test_downloads_service.py`| Unit tests for the downloads service logic. |
| `./api/tests/unit/test_notifications_service.py`| Unit tests for the notifications service logic. |
| `./api/tests/unit/test_user_service.py`| Unit tests for the user service logic. |
| `./api/tests/unit/test_logging_service.py`| Unit tests for the logging service logic. |
| **`./api/build/lib/zotify_api/`** | **Build Artifacts** |
| `./api/build/lib/zotify_api/routes/config.py`| Build artifact of the config route module. |
| `./api/build/lib/zotify_api/routes/network.py`| Build artifact of the network route module. |
| `./api/build/lib/zotify_api/routes/spotify.py`| Build artifact of the spotify route module. |
| `./api/build/lib/zotify_api/routes/webhooks.py`| Build artifact of the webhooks route module. |
| `./api/build/lib/zotify_api/routes/notifications.py`| Build artifact of the notifications route module. |
| `./api/build/lib/zotify_api/routes/search.py`| Build artifact of the search route module. |
| `./api/build/lib/zotify_api/routes/cache.py`| Build artifact of the cache route module. |
| `./api/build/lib/zotify_api/routes/tracks.py`| Build artifact of the tracks route module. |
| `./api/build/lib/zotify_api/routes/logging.py`| Build artifact of the logging route module. |
| `./api/build/lib/zotify_api/routes/playlist.py`| Build artifact of the playlist route module. |
| `./api/build/lib/zotify_api/routes/auth.py`| Build artifact of the auth route module. |
| `./api/build/lib/zotify_api/routes/stubs.py`| Build artifact of the stubs route module. |
| `./api/build/lib/zotify_api/routes/metadata.py`| Build artifact of the metadata route module. |
| `./api/build/lib/zotify_api/routes/downloads.py`| Build artifact of the downloads route module. |
| `./api/build/lib/zotify_api/routes/sync.py`| Build artifact of the sync route module. |
| `./api/build/lib/zotify_api/routes/system.py`| Build artifact of the system route module. |
| `./api/build/lib/zotify_api/routes/user.py`| Build artifact of the user route module. |
| `./api/build/lib/zotify_api/config.py`| Build artifact of the config module. |
| `./api/build/lib/zotify_api/logging_config.py`| Build artifact of the logging_config module. |
| `./api/build/lib/zotify_api/main.py`| Build artifact of the main module. |
| `./api/build/lib/zotify_api/globals.py`| Build artifact of the globals module. |
| `./api/build/lib/zotify_api/auth_state.py`| Build artifact of the auth_state module. |
| `./api/build/lib/zotify_api/database.py`| Build artifact of the database module. |
| `./api/build/lib/zotify_api/models/config.py`| Build artifact of the config model. |
| `./api/build/lib/zotify_api/models/spotify.py`| Build artifact of the spotify model. |
| `./api/build/lib/zotify_api/models/sync.py`| Build artifact of the sync model. |
| `./api/build/lib/zotify_api/middleware/request_id.py`| Build artifact of the request_id middleware. |
| `./api/build/lib/zotify_api/schemas/network.py`| Build artifact of the network schema. |
| `./api/build/lib/zotify_api/schemas/spotify.py`| Build artifact of the spotify schema. |
| `./api/build/lib/zotify_api/schemas/notifications.py`| Build artifact of the notifications schema. |
| `./api/build/lib/zotify_api/schemas/cache.py`| Build artifact of the cache schema. |
| `./api/build/lib/zotify_api/schemas/tracks.py`| Build artifact of the tracks schema. |
| `./api/build/lib/zotify_api/schemas/logging.py`| Build artifact of the logging schema. |
| `./api/build/lib/zotify_api/schemas/auth.py`| Build artifact of the auth schema. |
| `./api/build/lib/zotify_api/schemas/metadata.py`| Build artifact of the metadata schema. |
| `./api/build/lib/zotify_api/schemas/playlists.py`| Build artifact of the playlists schema. |
| `./api/build/lib/zotify_api/schemas/downloads.py`| Build artifact of the downloads schema. |
| `./api/build/lib/zotify_api/schemas/generic.py`| Build artifact of the generic schema. |
| `./api/build/lib/zotify_api/schemas/system.py`| Build artifact of the system schema. |
| `./api/build/lib/zotify_api/schemas/user.py`| Build artifact of the user schema. |
| `./api/build/lib/zotify_api/services/sync_service.py`| Build artifact of the sync_service module. |
| `./api/build/lib/zotify_api/services/notifications_service.py`| Build artifact of the notifications_service module. |
| `./api/build/lib/zotify_api/services/spotify.py`| Build artifact of the spotify service module. |
| `./api/build/lib/zotify_api/services/user_service.py`| Build artifact of the user_service module. |
| `./api/build/lib/zotify_api/services/playlists_service.py`| Build artifact of the playlists_service module. |
| `./api/build/lib/zotify_api/services/webhooks.py`| Build artifact of the webhooks service module. |
| `./api/build/lib/zotify_api/services/metadata_service.py`| Build artifact of the metadata_service module. |
| `./api/build/lib/zotify_api/services/search.py`| Build artifact of the search service module. |
| `./api/build/lib/zotify_api/services/db.py`| Build artifact of the db service module. |
| `./api/build/lib/zotify_api/services/config_service.py`| Build artifact of the config_service module. |
| `./api/build/lib/zotify_api/services/deps.py`| Build artifact of the deps module. |
| `./api/build/lib/zotify_api/services/__init__.py`| Build artifact of the services package init. |
| `./api/build/lib/zotify_api/services/auth.py`| Build artifact of the auth service module. |
| `./api/build/lib/zotify_api/services/logging_service.py`| Build artifact of the logging_service module. |
| `./api/build/lib/zotify_api/services/cache_service.py`| Build artifact of the cache_service module. |
| `./api/build/lib/zotify_api/services/tracks_service.py`| Build artifact of the tracks_service module. |
| `./api/build/lib/zotify_api/services/network_service.py`| Build artifact of the network_service module. |
| `./api/build/lib/zotify_api/services/downloads_service.py`| Build artifact of the downloads_service module. |
| **`./snitch/`** | **Snitch Go Application** |
| `./snitch/internal/listener/handler.go`| Defines the HTTP request handlers for the Snitch listener. |
| `./snitch/internal/listener/handler_test.go`| Tests for the Snitch request handlers. |
| `./snitch/internal/listener/server.go`| Defines the HTTP server for the Snitch listener. |
| `./snitch/snitch.go` | Main application file for the Snitch helper. |
| `./snitch/snitch_debug.go` | A debug version of the main Snitch application file. |
| `./snitch/cmd/snitch/main.go`| Command-line entry point for the Snitch application. |

---

## **Part 2: The Expectation — Documentation Gap Analysis**

This table provides a complete analysis of all 52 markdown files in the repository.

| File Path | Status | Gap Analysis |
| :--- | :--- | :--- |
| **`./` (Root Directory)** | | |
| `./README.md` | ❌ **Critically Inaccurate** | Fails to mention the mandatory `X-API-Key` authentication. Links to outdated/useless OpenAPI specifications. |
| **`./.github/`** | | |
| `./.github/ISSUE_TEMPLATE/bug-report.md` | ✅ **Accurate** | None. Standard, functional issue template. |
| `./.github/ISSUE_TEMPLATE/feature-request.md` | ✅ **Accurate** | None. Standard, functional issue template. |
| **`./docs/` (Root Docs)** | | |
| `./docs/developer_guide.md` | ❌ **Critically Inaccurate** | Describes a fictional API. Key endpoints (e.g., `/privacy/data`) do not exist, the documented response format is wrong, and endpoint paths are incorrect. |
| `./docs/INTEGRATION_CHECKLIST.md` | 🤷 **Ambiguous / Low-Value** | Minimal, context-free checklist for a single component. Appears to be a developer's note rather than formal documentation. |
| `./docs/operator_guide.md` | ⚠️ **Partially Inaccurate** | Describes a more robust API key management system than is implemented and refers to non-existent privacy endpoints. |
| `./docs/roadmap.md` | ❌ **Misleading and Inaccurate** | Presents a false narrative of a nearly complete project by marking incomplete items (e.g., stub removal, testing) as "✅ (Completed)". |
| `./docs/zotify-api-manual.md` | ❌ **Critically Inaccurate** | Unusable as a reference. Incomplete auth flow description, useless endpoint list with no details, and an incorrect manual test runbook. |
| **`./docs/projectplan/`** | | |
| `./docs/projectplan/admin_api_key_mitigation.md` | ❌ **Inaccurate (Aspirational)** | Describes a detailed design for a dynamic API key system that was never implemented. |
| `./docs/projectplan/admin_api_key_security_risk.md`| ✅ **Accurate** | Accurately describes the current, risky implementation of the static admin API key. One of the few honest planning documents. |
| `./docs/projectplan/doc_maintenance.md` | ❌ **Fictional (Process)** | Describes a disciplined, documentation-centric workflow that is the polar opposite of what actually happened. |
| `./docs/projectplan/HLD_Zotify_API.md` | ⚠️ **Partially Inaccurate** | The architectural overview is accurate, but the sections on process, governance, and documentation are pure fantasy. |
| `./docs/projectplan/LLD_18step_plan_Zotify_API.md` | ❌ **Falsified Record** | A complete work of fiction. Falsely claims an 18-step plan is complete. Contains multiple conflicting roadmaps. The most misleading file in the project. |
| `./docs/projectplan/next_steps_and_phases.md` | ❌ **Fictional and Contradictory** | The third conflicting roadmap. Wildly inaccurate, marking non-existent features as "Done". Claims to be the single source of truth for tasks, a mandate that was ignored. |
| `./docs/projectplan/privacy_compliance.md` | ❌ **Fictional** | Makes false claims about GDPR compliance and the existence of critical privacy API endpoints (`/privacy/data`) that do not exist. |
| `./docs/projectplan/roadmap.md` | ❌ **Fictional** | The second conflicting roadmap. Describes a detailed, disciplined development process that was completely ignored. |
| `./docs/projectplan/security.md` | ⚠️ **Partially Inaccurate** | Accurately identifies critical security flaws (e.g., plaintext token storage) but frames them as future roadmap items instead of immediate vulnerabilities. |
| `./docs/projectplan/spotify_capability_audit.md` | ✅ **Accurate (Superseded)** | Correctly states that it is superseded and points to the new document. Should be archived. |
| `./docs/projectplan/spotify_fullstack_capability_blueprint.md`| ❌ **Inaccurate (Aspirational)** | A massive, ambitious design blueprint that was almost completely ignored during implementation. The API structure and namespacing do not match this plan. |
| `./docs/projectplan/spotify_gap_alignment_report.md`| ❌ **Fictional and Contradictory**| Falsely marks non-existent features as "Done" and contradicts other planning documents it claims to align with. |
| `./docs/projectplan/task_checklist.md` | ✅ **Accurate (but Ignored)** | The checklist itself is a clear set of instructions. The gap is that this "authoritative" document was completely ignored during development. |
| **`./docs/projectplan/audit/`** | | |
| `./docs/projectplan/audit/AUDIT-phase-1.md` | ✅ **Accurate** | This file, the one being written. |
| `./docs/projectplan/audit/README.md` | ✅ **Accurate** | A simple README for the directory. |
| **`./docs/projectplan/reports/`** | | |
| `./docs/projectplan/reports/20250807-doc-clarification-completion-report.md`| ✅ **Accurate (Historical)** | An accurate report of a completed task. |
| `./docs/projectplan/reports/20250807-spotify-blueprint-completion-report.md`| ✅ **Accurate (Historical)** | An accurate report on the *creation* of the (fictional) blueprint document. |
| `./docs/projectplan/reports/20250808-comprehensive-auth-and-docs-update-report.md`| ✅ **Accurate (Historical)** | An accurate report of the OAuth flow implementation. |
| `./docs/projectplan/reports/20250808-oauth-unification-completion-report.md`| ✅ **Accurate (Historical)** | An accurate report of the OAuth flow implementation. |
| `./docs/projectplan/reports/20250809-api-endpoints-completion-report.md`| ✅ **Accurate (Historical)** | An accurate report of a large task that was completed. |
| `./docs/projectplan/reports/20250809-phase5-endpoint-refactor-report.md`| ✅ **Accurate (Historical)** | An accurate report of a successful architectural refactoring. |
| `./docs/projectplan/reports/20250809-phase5-final-cleanup-report.md`| ✅ **Accurate (Historical)** | An accurate report, but its conclusion that the phase was "complete" was premature. |
| `./docs/projectplan/reports/20250809-phase5-playlist-implementation-report.md`| ✅ **Accurate (Historical)** | An accurate report of a major feature implementation. |
| `./docs/projectplan/reports/20250809-phase5-search-cleanup-report.md`| ✅ **Accurate (Historical)** | An accurate report that also serves as evidence of the flawed documentation review process. |
| `./docs/projectplan/reports/FIRST_AUDIT.md`| ❌ **Inaccurate** | An early, incomplete, and flawed version of the current audit. |
| `./docs/projectplan/reports/README.md` | ⚠️ **Inaccurate (Incomplete)** | The index is missing links to several reports in its own directory. |
| **`./docs/snitch/`** | | |
| `./docs/snitch/PHASE_2_SECURE_CALLBACK.md` | ❌ **Outdated** | Describes security logic (`state` validation) that has since been moved from `snitch` to the main API backend. |
| `./docs/snitch/TEST_RUNBOOK.md` | ❌ **Outdated** | A manual testing guide for a previous version of the `snitch` application. The test steps are no longer valid. |
| `./docs/snitch/phase5-ipc.md` | ❌ **Fictional (Unimplemented)** | Describes a complex IPC architecture that was never implemented. The actual implementation is completely different. |
| **`./api/docs/`** | | |
| `./api/docs/CHANGELOG.md` | ⚠️ **Inaccurate (Incomplete)** | Contains some recent entries but is missing many significant changes and does not follow a consistent format. |
| `./api/docs/CONTRIBUTING.md` | ⚠️ **Inaccurate** | Specifies the wrong linter (`pylint` instead of `ruff`) and contains a broken link to a non-existent "Testing Criteria" section. |
| `./api/docs/DATABASE.md` | ⚠️ **Mostly Accurate (Incomplete)** | Accurately describes the *architecture* for DB support but fails to mention that no DB is configured by default and provides no schema/migration info. |
| `./api/docs/INSTALLATION.md` | ⚠️ **Incomplete (Stub)** | Provides accurate instructions for manual developer setup but contains empty placeholders for three other installation methods (Script, .deb, Docker). |
| `./api/docs/MANUAL.md` | ❌ **Critically Inaccurate** | Unusable. Incomplete auth flow description, useless endpoint list with no details, incorrect test runbook, and wrong port number. |
| `./api/docs/full_api_reference.md` | ❌ **Critically Inaccurate** | Unusable. A chaotic mix of outdated info, incorrect paths, fictional endpoints, and wrong response schemas. |
| **`./snitch/`** | | |
| `./snitch/README.md` | ❌ **Outdated** | Describes a configuration method (environment variable) and file structure that are no longer in use. |
| **`./snitch/docs/`** | | |
| `./snitch/docs/INSTALLATION.md` | 🤷 **Ambiguous** | Minimalist; just says to use `go build`. Lacks context. |
| `./snitch/docs/MILESTONES.md` | ❌ **Fictional** | Lists milestones for a development plan that was not followed. |
| `./snitch/docs/MODULES.md` | ❌ **Outdated** | Describes a single-file structure for `snitch` before it was refactored into a standard Go project. |
| `./snitch/docs/PHASES.md` | ❌ **Fictional** | Describes development phases that do not match the implemented reality. |
| `./snitch/docs/PROJECT_PLAN.md` | ❌ **Fictional** | A high-level plan for a version of `snitch` that was never built. |
| `./snitch/docs/ROADMAP.md` | ❌ **Fictional (Unimplemented)** | A detailed roadmap for a version of `snitch` with features (like random ports) that were never implemented. |
| `./snitch/docs/STATUS.md` | ❌ **Outdated** | A generic status update that is no longer relevant. |
| `./snitch/docs/TASKS.md` | ❌ **Fictional** | A list of tasks for a version of `snitch` that was never built. |
| `./snitch/docs/TEST_RUNBOOK.md` | ❌ **Outdated** | A duplicate of the other outdated runbook. |

---

## **Part 3: Final Advice & Recommendations**

The project's codebase is functional but its documentation is in a state of total collapse. It is actively harmful, misleading, and contradictory. More time appears to have been spent writing fictional plans and processes than was spent following them.

**My advice is to declare "documentation bankruptcy."** The existing planning documents are unsalvageable and untrustworthy.

### **Recommended Action Plan**

**Step 1: Archive the Fiction (Immediate)**
*   **Action:** Create a new directory `docs/archive` and move almost the entire contents of `docs/projectplan`, `docs/snitch`, and `snitch/docs` into it. These documents are toxic assets and must be removed from the main project view to prevent further confusion.
*   **Rationale:** The current documentation is worse than no documentation. It actively wastes developer time and creates false impressions about the project's status, architecture, and processes. Archiving it is the first step to establishing a new, reliable source of truth.

**Step 2: Establish a Minimal, Trustworthy Core**
*   **Action:** Create a new, single `README.md` in the root directory that is 100% accurate. It should cover:
    1.  A brief, honest description of the project's purpose.
    2.  Correct, verifiable installation and setup instructions.
    3.  A simple, correct guide to the authentication flow (`X-API-Key`).
    4.  A link to the auto-generated OpenAPI documentation (`/docs`) as the **single source of truth for all API endpoints**. Explicitly state that all other API reference documents are deprecated.
*   **Rationale:** Developers need a single, reliable entry point. All effort should be focused on making this one file perfect before attempting to document anything else.

**Step 3: Address Critical Codebase Risks**
*   **Action:** Create a new, focused plan to address the security risks identified in `docs/projectplan/security.md`, which was one of the few accurate documents.
    1.  **HIGH PRIORITY:** Implement secure, encrypted storage for the Spotify OAuth tokens. Storing them in a plaintext JSON file is a critical vulnerability.
    2.  Implement proper authentication and authorization for all endpoints that handle user data (e.g., the `notifications` endpoints).
*   **Rationale:** The codebase has known, documented, high-priority security flaws that should be addressed before any new features are considered.

**Step 4: Re-evaluate the Project's Goals**
*   **Action:** After the codebase is secured and a minimal, accurate README is in place, a new planning process should begin. This should start with a simple, high-level roadmap, not a complex, multi-layered set of fictional documents.
*   **Rationale:** The project needs to restart its planning process from a foundation of reality, not fantasy.
