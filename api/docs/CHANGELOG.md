## v0.1.12

### Changed
- Refactored **playlists subsystem** to use a dedicated `playlists_service.py` service layer.
- Updated `routes/playlist.py` to use the new service layer via dependency injection.
- Improved maintainability by removing direct DB/logic calls from routes.
- Added full unit test coverage for playlists routes and service.
- **Maintained and updated related documentation to reflect changes.**

## v0.1.11

### Changed
- Refactored **config subsystem** to use a dedicated `config_service.py` service layer.
- Updated `routes/config.py` to use dependency injection for configuration management.
- Added new unit tests to cover all code paths in config handling.
- Fixed intermittent failure in `tests/test_playlists.py`.
- Resolved bug in `tests/test_config.py::test_reset_config` where defaults were not restored correctly.
- **Maintained and updated related documentation to reflect changes.**

## v0.1.10

### Changed
- Refactored **sync subsystem** to extract `run_sync_job` into `sync_service.py`.
- Updated `routes/sync.py` to use dependency injection for sync job execution.
- Added test coverage for sync runner failures and fallback behavior.
- **Maintained and updated related documentation to reflect changes.**

## v0.1.9

### Changed
- Refactored **search subsystem** for maintainability and testability:
  - Moved `search_spotify` to a dedicated `services/search_spotify.py` module.
  - Updated `perform_search` in `services/search.py` to accept injected `db_engine` and `spotify_search_func`.
  - Updated `routes/search.py` to use FastAPI dependency injection for feature flags, DB engine, and search function.
- Fixed failing search tests caused by inconsistent import and patch targets.
- Added new tests for database failure fallback to Spotify search.
- **Maintained and updated related documentation to reflect changes.**
