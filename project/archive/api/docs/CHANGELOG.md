Changelog

All notable changes to the Zotify REST API will be documented in this file.

v0.1.35
Changed
    - Implemented `POST /api/spotify/sync_playlists` to fetch all user playlists and save them locally.
    - Refactored `POST /auth/spotify/callback` to use the `SpotiClient`, removing the last direct `httpx` call from the route files.
Fixed
    - Corrected multiple test cases related to response validation and mocking strategy.
    - Added missing `Depends` and `require_admin_api_key` imports that were causing test discovery to fail.

v0.1.34
Added
    - Full implementation for all Spotify playlist management endpoints under `/api/spotify/playlists`.
        - `GET /playlists`: List current user's playlists.
        - `POST /playlists`: Create a new playlist.
        - `GET /playlists/{id}`: Get a specific playlist.
        - `PUT /playlists/{id}`: Update a playlist's details.
        - `DELETE /playlists/{id}`: Unfollow a playlist.
        - `GET /playlists/{id}/tracks`: Get tracks from a playlist.
        - `POST /playlists/{id}/tracks`: Add tracks to a playlist.
        - `DELETE /playlists/{id}/tracks`: Remove tracks from a playlist.

v0.1.33
Changed
    - Implemented the `GET /api/search` endpoint to perform searches against the Spotify API.
Removed
    - Removed the duplicate `GET /api/spotify/metadata/{track_id}` endpoint. The `POST /api/tracks/metadata` endpoint should be used instead.

v0.1.32
Changed
    - Refactored `GET /api/auth/status` to use the `SpotiClient`.
    - Refactored `GET /api/auth/refresh` to use the `SpotiClient`.
    - Refactored `GET /api/spotify/devices` to use the `SpotiClient`.
Fixed
    - Corrected several integration tests to use service-level mocking instead of direct HTTP mocking, improving test stability and consistency.

v0.1.31
Changed
    - Refactored Spotify API interactions into a dedicated `SpotiClient` class to centralize authentication, requests, and error handling.
    - Updated `POST /api/tracks/metadata` to use the new `SpotiClient`, improving robustness and adhering to the service-layer architecture.
    - Updated `GET /api/spotify/me` to use the new `SpotiClient`.
Fixed
    - Corrected several test environment and mocking issues to ensure a stable and reliable test suite.

v0.1.30
Added
    - `GET /api/auth/status`: Returns current Spotify authentication status.
    - `POST /api/auth/logout`: Clears stored Spotify credentials.
    - `GET /api/auth/refresh`: Refreshes the Spotify access token.
    - `GET /api/spotify/me`: Returns the raw Spotify user profile.
    - `GET /api/spotify/devices`: Lists available Spotify playback devices.
    - `POST /api/tracks/metadata`: Fetches metadata for multiple tracks in a single request.
    - `GET /api/system/uptime`: Returns the API server's uptime.
    - `GET /api/system/env`: Returns environment information for the API server.
    - `GET /api/schema`: Returns the OpenAPI schema for the API.
Changed
    - Extended `/api/search` to allow searching by `type` (track, album, artist, playlist, all) and added `limit` and `offset` for pagination.

v0.1.29
Added

    User privacy compliance statement and GDPR alignment.
    Implemented data export and deletion API endpoints.
    Enforced audit logging for personal data access.
    Updated documentation with detailed privacy and security compliance info.
    Added compliance checks and tests to validate GDPR adherence.

v0.1.28
Changed

    Standardized the response structure for all endpoints.
    Added a `/version` endpoint.
    Performed a final polish pass on the codebase.

v0.1.27
Added

    Notifications subsystem with endpoints for creating, retrieving, and managing user notifications.

v0.1.26
Added

    User profile and preferences management endpoints.

v0.1.25
Changed

    Refactored the playlists subsystem to a dedicated service layer.

v0.1.24
Added

    Comprehensive security chapter to HLD and LLD.
    New `security.md` document.
    Security roadmap to LLD.

v0.1.23
Changed

    Replaced static admin API key with a dynamic, auto-generated key system to mitigate security risks.
    The application now generates a secure admin API key on first startup if one is not provided.

v0.1.22
Added

    Security risk documentation for the admin API key.
    Updated HLD and LLD with security considerations.

v0.1.21
Added

    Admin API key authentication for protected endpoints.
    `X-API-Key` header for authenticating admin requests.
    Production startup guard to require an admin API key.

Changed

    Protected all admin-only endpoints with the new authentication mechanism.
    Updated tests to include authentication checks.

v0.1.20
Added

    Dedicated metadata_service for all metadata-related logic.

    New metadata.py schema file for request/response validation.

    Unit tests for metadata_service and updated integration tests for metadata routes.

Changed

    Refactored metadata routes to use the new metadata_service and Pydantic schemas.

v0.1.19
Added

    Dedicated user_service for all user-related logic.

    New user.py schema file for request/response validation.

    Unit tests for user_service and updated integration tests for user routes.

Changed

    Refactored user routes to use the new user_service and Pydantic schemas.

v0.1.18
Added

    Dedicated network_service for all network-related logic.

    New network.py schema file for request/response validation.

    Unit tests for network_service and updated integration tests for network routes.

Changed

    Refactored network routes to use the new network_service and Pydantic schemas.

v0.1.17
Added

    Dedicated logging_service for all logging-related logic.

    New logging.py schema file for request/response validation.

    Unit tests for logging_service and updated integration tests for logging routes.

Changed

    Refactored logging routes to use the new logging_service and Pydantic schemas.

v0.1.16
Changed

    Performed a full audit of all documentation under the docs/ directory.
    Updated API reference pages, developer guides, usage examples, and CHANGELOG.md to be accurate, complete, and consistent with the current codebase.

v0.1.15
Added

    Dedicated downloads_service for all download-related logic.

    New downloads.py schema file for request/response validation.

    Unit tests for downloads_service and updated integration tests for downloads routes.

Changed

    Refactored downloads routes to use the new downloads_service and Pydantic schemas.

v0.1.14
Added

    Dedicated tracks_service for all track-related logic.

    New tracks.py schema file for request/response validation.

    Unit tests for tracks_service and updated integration tests for tracks routes.

Changed

    Refactored tracks routes to use the new tracks_service and Pydantic schemas.

v0.1.13
Added

    Dedicated playlists_service for playlist management.

    Full unit test coverage for the playlists service.

Changed

    Refactored playlists routes to use the new service layer.

    Updated integration tests to match the dependency injection pattern.

v0.1.12
Added

    Dedicated config_service for application configuration handling.

    Extended tests for config logic with additional edge case coverage.

Changed

    Refactored config routes to use config_service.

    Fixed intermittent test failures in playlist tests.

v0.1.11
Added

    Dedicated sync_service with run_sync_job moved from routes to service layer.

    New unit tests covering sync failure scenarios.

Changed

    Refactored sync routes to use FastAPI dependency injection for run_sync_job.

v0.1.10
Added

    Dependency injection for search subsystem.

    Additional tests for database failure with fallback to Spotify.

Changed

    Refactored perform_search in services/search.py to accept db_engine and spotify_search_func arguments.

    Updated routes/search.py to use injected dependencies.

    Improved testability and maintainability of search code.

v0.1.9
Fixed

    Corrected failing test_reset_config by ensuring config defaults are restored on reset.

v0.1.8
Added

    Live Spotify integration with OAuth2 authentication.

    Endpoints for managing Spotify API tokens.

    Stubs for syncing playlists and fetching metadata from Spotify.

v0.1.7
Added

    Comprehensive API reference manual.

v0.1.6
Added

    Fork-specific features:

        Advanced playlist sync endpoint.

        Download status and retry endpoints.

        Extended metadata endpoints.

v0.1.5
Added

    Endpoints for managing logging, caching, and network settings.

v0.1.4
Added

    Endpoints for managing application configuration and track metadata.

v0.1.3
Added

    Full playlist management module (GET, POST, DELETE, add/remove tracks).

    Playlist import from .json and export to .json and .m3u.

    Modular project structure with models, routes, and storage directories.

    JSON-file-based storage for playlists.

v0.1.2
Added

    Core search and download endpoints:

        GET /search with pagination.

        POST /download/{target} where target is one of track, album, or playlist.

    Pydantic models for search and download request/response bodies.

    Validation for search parameters and download request bodies.

v0.1.1
Added

    Stub endpoints for retrieving metadata for tracks, albums, and artists:

        GET /tracks/{track_id}

        GET /albums/{album_id}

        GET /artists/{artist_id}

    Pydantic models for metadata responses.

v0.1.0
Added

    Initial setup of the FastAPI server.

    Basic /ping health check endpoint.

    Decoupled architecture to allow the API to run alongside a standard Zotify v0.6.x installation.

    All dependencies are managed within the api module.

    Comprehensive documentation for installation, usage, and contribution.

    OpenAPI 3.0 specifications in both JSON and YAML formats.
