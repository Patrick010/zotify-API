# Changelog

All notable changes to the Zotify REST API will be documented in this file.

## v0.1.3 - 2025-08-04

### Added
- Full playlist management module (`GET`, `POST`, `DELETE`, `add/remove tracks`).
- Playlist import from `.json` and export to `.json` and `.m3u`.
- Modular project structure with `models`, `routes`, and `storage` directories.
- JSON-file-based storage for playlists.

## v0.1.2 - 2025-08-04

### Added
- Core search and download endpoints.
  - `GET /search` with pagination.
  - `POST /download/{target}` where target is one of `track`, `album`, or `playlist`.
- Pydantic models for search and download request/response bodies.
- Validation for search parameters and download request bodies.

## v0.1.1 - 2025-08-04

### Added
- Stub endpoints for retrieving metadata for tracks, albums, and artists.
  - `GET /tracks/{track_id}`
  - `GET /albums/{album_id}`
  - `GET /artists/{artist_id}`
- Pydantic models for metadata responses.

## v0.1.0 - 2025-08-04

### Added
- Initial setup of the FastAPI server.
- Basic `/ping` health check endpoint.
- Decoupled architecture to allow the API to run alongside a standard Zotify v0.6.x installation.
- All dependencies are managed within the `api` module.
- Comprehensive documentation for installation, usage, and contribution.
- OpenAPI 3.0 specifications in both JSON and YAML formats.
