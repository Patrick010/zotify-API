Changelog

All notable changes to the Zotify REST API will be documented in this file.
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
