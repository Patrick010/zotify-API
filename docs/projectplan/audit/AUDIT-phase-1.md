# **AUDIT-phase-1: Comprehensive API & Documentation Reality Audit (Corrected v3)**

**Date:** 2025-08-10
**Author:** Jules
**Version:** 3.0 (This version corrects the scope of the file inventory to include only .py and .go files, as requested. This is the definitive baseline.)
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

This table provides the definitive list of all 117 `.py` and `.go` source files in the project.

| File Path | Purpose |
| :--- | :--- |
| **`./` (Root Directory)** | |
| `./audit_endpoints.py` | A script used to audit and list API endpoints. |
| **`./zotify/` (CLI Tool)** | |
| `./zotify/__init__.py` | Makes the `zotify` directory a Python package. |
| `./zotify/__main__.py` | Main entry point for running the Zotify CLI tool (`python -m zotify`). |
| `./zotify/album.py` | Contains logic for downloading albums for the CLI. |
| `./zotify/app.py` | Main application logic and command handling for the CLI. |
| `./zotify/config.py` | Manages the complex configuration for the CLI tool. |
| `./zotify/const.py` | Defines global constants for the CLI application. |
| `./zotify/playlist.py` | Contains logic for downloading Spotify playlists for the CLI. |
| `./zotify/podcast.py` | Contains logic for downloading podcast episodes for the CLI. |
| `./zotify/termoutput.py`| Provides sophisticated terminal output formatting for the CLI. |
| `./zotify/track.py` | Contains logic for downloading and parsing individual tracks in the CLI. |
| `./zotify/utils.py` | Miscellaneous utility functions for the CLI. |
| `./zotify/zotify.py` | Defines the central `Zotify` class that holds state for the CLI. |
| **`./snitch/` (Go Helper App)** | |
| `./snitch/cmd/snitch/main.go`| Command-line entry point for the Snitch application. |
| `./snitch/internal/listener/handler.go`| Defines the HTTP request handlers for the Snitch listener. |
| `./snitch/internal/listener/handler_test.go`| Tests for the Snitch request handlers. |
| `./snitch/internal/listener/server.go`| Defines the HTTP server for the Snitch listener. |
| `./snitch/snitch.go` | Main application file for the Snitch helper. |
| **`./api/` (Zotify API)** | |
| `./api/minimal_test_app.py` | A minimal FastAPI app for testing purposes. |
| `./api/route_audit.py` | A Python script to audit API routes. |
| `./api/test_minimal_app.py` | A script to test the minimal FastAPI application. |
| **`./api/tests/`** | |
| `./api/tests/__init__.py` | Makes the `tests` directory a Python package. |
| `./api/tests/conftest.py`| Pytest configuration and shared fixtures for integration tests. |
| `./api/tests/test_cache.py`| Integration tests for the Cache module. |
| `./api/tests/test_config.py`| Integration tests for the Config module. |
| `./api/tests/test_downloads.py`| Integration tests for the Downloads module. |
| `./api/tests/test_logging.py`| Integration tests for the Logging module. |
| `./api/tests/test_metadata.py`| Integration tests for the Metadata module. |
| `./api/tests/test_network.py`| Integration tests for the Network module. |
| `./api/tests/test_notifications.py`| Integration tests for the Notifications module. |
| `./api/tests/test_playlists.py`| Integration tests for the local Playlists module. |
| `./api/tests/test_spotify.py`| Integration tests for the Spotify module. |
| `./api/tests/test_stubs.py`| Tests that confirm stubbed endpoints return a 501 error. |
| `./api/tests/test_sync.py`| Integration tests for the Sync module. |
| `./api/tests/test_system.py`| Integration tests for the System module. |
| `./api/tests/test_tracks.py`| Integration tests for the Tracks module. |
| `./api/tests/test_user.py`| Integration tests for the User module. |
| **`./api/tests/unit/`** | |
| `./api/tests/unit/test_auth.py` | Unit tests for the authentication service and routes. |
| `./api/tests/unit/test_cache_service.py`| Unit tests for the cache service logic. |
| `./api/tests/unit/test_config.py`| Placeholder for config service unit tests. |
| `./api/tests/unit/test_downloads_service.py`| Unit tests for the downloads service logic. |
| `./api/tests/unit/test_logging_service.py`| Unit tests for the logging service logic. |
| `./api/tests/unit/test_metadata_service.py`| Unit tests for the metadata service logic. |
| `./api/tests/unit/test_network_service.py`| Unit tests for the network service logic. |
| `./api/tests/unit/test_new_endpoints.py`| Integration tests for recently added endpoints. |
| `./api/tests/unit/test_notifications_service.py`| Unit tests for the notifications service logic. |
| `./api/tests/unit/test_playlists_service.py`| Unit tests for the local playlists service logic. |
| `./api/tests/unit/test_search.py`| Unit tests for the Search endpoint. |
| `./api/tests/unit/test_spoti_client.py`| Unit tests for the central SpotiClient. |
| `./api/tests/unit/test_sync.py`| Unit tests for the sync service logic. |
| `./api/tests/unit/test_tracks_service.py`| Unit tests for the tracks service logic. |
| `./api/tests/unit/test_user_service.py`| Unit tests for the user service logic. |
| `./api/tests/unit/test_webhooks.py`| Unit tests for the webhooks service logic. |
| **`./api/src/zotify_api/`** | |
| `./api/src/zotify_api/auth_state.py`| Manages global authentication state and token storage. |
| `./api/src/zotify_api/config.py` | Handles loading and managing API-specific settings. |
| `./api/src/zotify_api/database.py`| Contains database connection and session management logic. |
| `./api/src/zotify_api/globals.py`| Stores global variables and application-wide objects. |
| `./api/src/zotify_api/logging_config.py`| Configures the application's logging setup. |
| `./api/src/zotify_api/main.py` | The main FastAPI application entrypoint and router configuration. |
| **`./api/src/zotify_api/middleware/`** | |
| `./api/src/zotify_api/middleware/request_id.py`| Middleware for adding a unique request ID to logs for traceability. |
| **`./api/src/zotify_api/models/`** | |
| `./api/src/zotify_api/models/config.py` | Data models related to configuration. |
| `./api/src/zotify_api/models/spotify.py` | Data models related to Spotify objects. |
| `./api/src/zotify_api/models/sync.py` | Data models related to synchronization jobs. |
| **`./api/src/zotify_api/routes/`** | |
| `./api/src/zotify_api/routes/auth.py` | Defines all authentication-related API endpoints. |
| `./api/src/zotify_api/routes/cache.py` | Defines endpoints for managing the application cache. |
| `./api/src/zotify_api/routes/config.py` | Defines endpoints for managing application configuration. |
| `./api/src/zotify_api/routes/downloads.py` | Defines endpoints for managing the download queue. |
| `./api/src/zotify_api/routes/logging.py` | Defines endpoints for managing logging levels. |
| `./api/src/zotify_api/routes/metadata.py` | Defines endpoints for managing local metadata. |
| `./api/src/zotify_api/routes/network.py` | Defines endpoints for managing network configuration. |
| `./api/src/zotify_api/routes/notifications.py`| Defines endpoints for user notifications. |
| `./api/src/zotify_api/routes/playlist.py` | Defines endpoints for managing local playlists. |
| `./api/src/zotify_api/routes/search.py` | Defines the primary search endpoint for Spotify. |
| `./api/src/zotify_api/routes/spotify.py` | Defines all Spotify-specific interaction endpoints. |
| `./api/src/zotify_api/routes/stubs.py` | Defines explicitly unimplemented endpoints that return 501. |
| `./api/src/zotify_api/routes/sync.py` | Defines endpoints for triggering background synchronization jobs. |
| `./api/src/zotify_api/routes/system.py` | Defines endpoints for retrieving system information and status. |
| `./api/src/zotify_api/routes/tracks.py` | Defines endpoints for managing the local tracks database. |
| `./api/src/zotify_api/routes/user.py` | Defines endpoints for managing the local user profile. |
| `./api/src/zotify_api/routes/webhooks.py` | Defines endpoints for managing webhooks. |
| **`./api/src/zotify_api/schemas/`** | |
| `./api/src/zotify_api/schemas/auth.py` | Pydantic models for the Authentication module. |
| `./api/src/zotify_api/schemas/cache.py` | Pydantic models for the Cache module. |
| `./api/src/zotify_api/schemas/downloads.py`| Pydantic models for the Downloads module. |
| `./api/src/zotify_api/schemas/generic.py` | Generic response models (e.g., message, status) for the API. |
| `./api/src/zotify_api/schemas/logging.py` | Pydantic models for the Logging module. |
| `./api/src/zotify_api/schemas/metadata.py` | Pydantic models for the local Metadata module. |
| `./api/src/zotify_api/schemas/network.py` | Pydantic models for the Network module. |
| `./api/src/zotify_api/schemas/notifications.py`| Pydantic models for the Notifications module. |
| `./api/src/zotify_api/schemas/playlists.py`| Pydantic models for the local Playlists module. |
| `./api/src/zotify_api/schemas/spotify.py` | Pydantic models for the Spotify module. |
| `./api/src/zotify_api/schemas/system.py` | Pydantic models for the System module. |
| `./api/src/zotify_api/schemas/tracks.py` | Pydantic models for the local Tracks module. |
| `./api/src/zotify_api/schemas/user.py` | Pydantic models for the User module. |
| **`./api/src/zotify_api/services/`** | |
| `./api/src/zotify_api/services/__init__.py` | Makes the services directory a Python package. |
| `./api/src/zotify_api/services/auth.py` | Business logic for all authentication flows. |
| `./api/src/zotify_api/services/cache_service.py` | Business logic for cache management. |
| `./api/src/zotify_api/services/config_service.py` | Business logic for configuration management. |
| `./api/src/zotify_api/services/db.py` | Utility functions for database interactions. |
| `./api/src/zotify_api/services/deps.py` | FastAPI dependencies for injection into route handlers. |
| `./api/src/zotify_api/services/downloads_service.py`| Business logic for the download queue. |
| `./api/src/zotify_api/services/logging_service.py` | Business logic for logging management. |
| `./api/src/zotify_api/services/metadata_service.py` | Business logic for local metadata management. |
| `./api/src/zotify_api/services/network_service.py` | Business logic for network configuration. |
| `./api/src/zotify_api/services/notifications_service.py`| Business logic for user notifications. |
| `./api/src/zotify_api/services/playlists_service.py`| Business logic for local playlist management. |
| `./api/src/zotify_api/services/search.py` | Business logic for the search feature. |
| `./api/src/zotify_api/services/spoti_client.py`| **CRITICAL:** The central client for all Spotify API communication. |
| `./api/src/zotify_api/services/spotify.py` | Service functions that bridge routes to the SpotiClient. |
| `./api/src/zotify_api/services/sync_service.py` | Business logic for background synchronization jobs. |
| `./api/src/zotify_api/services/tracks_service.py` | Business logic for local tracks management. |
| `./api/src/zotify_api/services/user_service.py` | Business logic for local user profile management. |
| `./api/src/zotify_api/services/webhooks.py` | Business logic for webhook management. |

---

## **Part 2: The Expectation — Documentation Gap Analysis**

| File Path | Status | Gap Analysis |
| :--- | :--- | :--- |
| **`./README.md`** | ❌ **Critically Inaccurate** | Fails to mention the mandatory `X-API-Key` authentication. |
| **`./api/docs/CHANGELOG.md`** | ⚠️ **Contradictory** | Recent entries are accurate, but its history conflicts with other planning documents. |
| **`./api/docs/zotify-openapi-external-v1.yaml`** | ❌ **Useless** | Documents only 3 of ~80 endpoint operations. Should be deleted. |
| **`./docs/developer_guide.md`** | ❌ **Critically Inaccurate** | Contains incorrect information and is missing entire feature sets. |
| **`./docs/projectplan/HLD_Zotify_API.md`**| ⚠️ **Inaccurate** | Describes an ideal process that has failed. |
| **`./docs/projectplan/LLD_18step_plan_Zotify_API.md`** | ❌ **False** | The central checklist is falsified. Should be archived immediately. |
| **`./docs/projectplan/next_steps_and_phases.md`** | ❌ **Fictional** | Contains a third, conflicting roadmap. Should be archived. |
| **`./docs/projectplan/spotify_fullstack_capability_blueprint.md`** | ⚠️ **Outdated** | Proposes an architecture (namespacing) that was not implemented. |
| **`./docs/projectplan/spotify_gap_alignment_report.md`** | ❌ **Contradictory** | Conflicts with the Blueprint and reality. Should be archived. |
| **`./docs/projectplan/privacy_compliance.md`** | ❌ **Inaccurate** | Claims features like `/privacy/data` endpoints exist when they do not. |
| **`./docs/projectplan/task_checklist.md`** | ✅ **Accurate** | This file has been kept up-to-date. |

---

## **Part 3: Final Advice & Recommendations**

The project is at a critical inflection point. The codebase is salvageable and now has a solid architectural foundation. The documentation and planning process, however, is broken and must be rebuilt from a new baseline of truth.

**My advice is to treat the project's documentation as a high-priority technical debt and pay it down immediately.**

### **Recommended Action Plan**

**Step 1: Erase the False History (Immediate)**
*   **Action:** Create a new directory `docs/archive` and move the most misleading planning documents into it.
*   **Rationale:** This immediately removes the sources of confusion and contradiction.

**Step 2: Establish a Single Source of Truth (Next)**
*   **Action:** Overhaul `docs/roadmap.md` to be the **single, authoritative roadmap**. Update it to reflect the *true* state of the project based on this audit.
*   **Action:** Update the `HLD_Zotify_API.md` to be the **single, authoritative architectural guide**.
*   **Action:** Generate a new, complete `openapi.json` from the FastAPI application and make it the **single, authoritative API contract**.

**Step 3: Fix Critical User & Developer Onboarding**
*   **Action:** Update the `README.md` and `developer_guide.md` to be 100% accurate based on the findings in this report.

**Step 4: Address Codebase Gaps**
*   **Action:** Create a new, focused plan to address the remaining functional and architectural gaps.
