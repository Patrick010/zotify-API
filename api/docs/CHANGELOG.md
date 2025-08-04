# Changelog

All notable changes to the Zotify REST API will be documented in this file.

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
