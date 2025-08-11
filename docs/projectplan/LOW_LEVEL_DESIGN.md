# Low-Level Design (LLD) – Zotify API

## Purpose
This LLD describes the specific implementation details of the Zotify API's subsystems, with a focus on the new unified database architecture.

## Unified Database Architecture

**Goal:** To establish a single, unified, and backend-agnostic persistence layer for the entire application, managed by SQLAlchemy.

**Module:** `api/src/zotify_api/database/`

*   **`session.py`**:
    *   Creates a single SQLAlchemy `engine` based on the `DATABASE_URI` from the application settings.
    *   Provides a `SessionLocal` factory for creating database sessions.
    *   Provides a `get_db` dependency for use in FastAPI routes, ensuring that a database session is created for each request and closed afterward.
    *   Defines the `Base` class that all ORM models inherit from.

*   **`models.py`**:
    *   Contains all SQLAlchemy ORM model definitions. This includes tables for `users`, `spotify_tokens`, `tracks`, `playlists`, and `download_jobs`.
    *   Defines all table relationships (e.g., the many-to-many relationship between playlists and tracks).

*   **`crud.py`**:
    *   Provides a layer of abstraction for database operations.
    *   Contains functions for creating, reading, updating, and deleting records for each model (e.g., `create_download_job`, `get_spotify_token`).
    *   Service-layer modules call these functions instead of interacting with the database session directly.

---

## Spotify Integration Design

**Goal:** To provide a robust integration with the Spotify Web API, with all persistent data stored in the unified database.

*   **Authentication & Token Storage**:
    *   The OAuth2 callback (`routes/spotify.py`) now saves the access and refresh tokens to the `spotify_tokens` table in the database via a CRUD function.
    *   A new dependency, `get_spoti_client` (`services/deps.py`), is responsible for providing an authenticated `SpotiClient`. It fetches the token from the database, automatically refreshes it if it's expired, and saves the new token back to the database.

*   **Playlist Synchronization**:
    *   The `sync_playlists` service function (`services/spotify.py`) now saves all of the user's playlists and their associated tracks to the `playlists` and `tracks` tables in the database, replacing the previous file-based storage (`playlists.json`).

---

## Downloads Subsystem Design

**Goal:** To provide a persistent and robust download management system using the unified database.

*   **API Endpoints (`routes/downloads.py`)**:
    *   The API endpoints remain the same, providing a consistent interface for managing downloads.
    *   The route handlers now use the `get_db` dependency to get a database session, which they pass to the service functions.

*   **Service Layer (`services/download_service.py`)**:
    -   The service has been refactored into a set of stateless functions that accept a database session (`db: Session`).
    -   All download queue operations (adding jobs, getting status, processing jobs) are now handled by calling the appropriate CRUD functions in `database/crud.py`, which interact with the `download_jobs` table.
    -   The previous standalone SQLite implementation (`services/downloads_db.py`) has been removed.

*   **Data Models (`schemas/downloads.py`)**:
    *   The Pydantic schemas have been updated to support the new architecture, with separate schemas for creating, updating, and reading data. They are configured with `orm_mode = True` to be compatible with SQLAlchemy objects.

---

## Ongoing Maintenance
All development tasks must follow the [Task Execution Checklist](./task_checklist.md) to ensure consistency, quality, and security.
