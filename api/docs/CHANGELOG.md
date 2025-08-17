# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to a custom versioning scheme for pre-releases.

## [Unreleased]

### Added
- **New Logging System**: Implemented a new, robust logging service that is fully configurable via `logging_config.yml`.
  - Includes a `ConsoleHandler` for standard output.
  - Includes a `JsonAuditHandler` for writing structured audit logs to a file.
  - Includes a `DatabaseJobHandler` for persisting the status of long-running jobs to the database.

### Changed
- **Error Handler Extensibility**: Refactored the error handling module's action system. Actions are now discovered dynamically from files in the `actions/` directory, making the system fully extensible without modifying core code.

### Fixed
- **Test Suite Stability**: Resolved persistent `OperationalError` failures in the download-related tests by refactoring the faulty, module-level database setup in `test_download.py` to use the standardized, function-scoped fixtures from `conftest.py`.
- **Test Environment Consistency**: Corrected a critical import-order issue related to SQLAlchemy model registration by ensuring the `models.py` module is loaded before `Base.metadata.create_all()` is called within the test database fixture. This fixed `no such table` errors for all tests.

---
## [0.1.0] - 2025-08-12

This is the initial documented release, capturing the state of the Zotify API after a series of major architectural refactorings.

### Added

-   **API Feature Set:**
    -   Spotify Authentication via OAuth2, including token refresh, and secure callback handling.
    -   Full CRUD (Create, Read, Update, Delete) operations for Playlists.
    -   Full CRUD operations for Tracks (database-only, metadata is separate).
    -   Persistent Download Queue system to manage and track download jobs.
    -   API for searching content via the configured provider.
    -   Endpoints for synchronizing playlists and library data from Spotify.
    -   System endpoints for monitoring application status, configuration, and logs.
    -   Webhook system for sending outbound notifications on application events.
-   **Developer Experience:**
    -   `gonk-testUI`: A standalone developer UI for easily testing all API endpoints.
    -   Comprehensive Project Documentation, including live status documents, developer guides, and a project registry.
    -   Default `DATABASE_URI` configuration to allow the application to run out-of-the-box for local development.

### Changed

-   **Unified Database:** All application data (including Spotify tokens, playlists, tracks, and download jobs) was migrated to a single, unified database backend using SQLAlchemy. This replaced multiple ad-hoc storage mechanisms (JSON files, in-memory dicts).
-   **Provider Abstraction Layer:** The architecture was refactored to be provider-agnostic. The Spotify-specific client was refactored into a stateless `SpotiClient` used by a `SpotifyConnector` that implements a generic `BaseProvider` interface.

### Fixed

-   Resolved a series of cascading `ImportError` and `ModuleNotFoundError` issues at startup caused by an incomplete refactoring of the authentication and provider systems. The application now starts cleanly.

### Removed

-   Removed the old file-based storage system for Spotify tokens (`spotify_tokens.json`).
-   Removed the mandatory environment variable check for `DATABASE_URI` from `start.sh` in favor of a development default.
