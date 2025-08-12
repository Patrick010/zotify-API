# Low-Level Design (LLD) – Zotify API

## Purpose
This LLD describes the specific implementation details of the Zotify API's subsystems, with a focus on the new provider-agnostic architecture.

## Provider Abstraction Layer

**Goal:** To decouple the core application logic from specific music service providers, allowing for future expansion to other services.

**Module:** `api/src/zotify_api/providers/`

*   **`base.py`**:
    *   Defines the `BaseProvider` abstract base class.
    *   This class specifies the common interface that all provider adapters must implement (e.g., `search`, `get_playlist`).

*   **`spotify_adapter.py`**:
    *   Contains the `SpotifyAdapter` class, which implements the `BaseProvider` interface for the Spotify service.
    *   All Spotify-specific logic, including calls to the `SpotiClient`, is encapsulated within this adapter.

*   **Dependency (`services/deps.py`)**:
    *   A new `get_provider` dependency is responsible for instantiating and returning the currently active provider adapter. For now, it always returns the `SpotifyAdapter`.

---

## Unified Database Architecture

**Goal:** To establish a single, unified, and backend-agnostic persistence layer for the entire application, managed by SQLAlchemy.

**Module:** `api/src/zotify_api/database/`

*   **`session.py`**:
    *   Creates a single SQLAlchemy `engine` based on the `DATABASE_URI` from the application settings.
    *   Provides a `SessionLocal` factory for creating database sessions.
    *   Provides a `get_db` dependency for use in FastAPI routes.

*   **`models.py`**:
    *   Contains all SQLAlchemy ORM model definitions.

*   **`crud.py`**:
    *   Provides a layer of abstraction for database operations.

---

## Spotify Integration Design

**Goal:** To provide a robust integration with the Spotify Web API, implemented as the first adapter for the provider abstraction layer.

*   **Authentication & Token Storage**:
    *   The OAuth2 callback saves tokens to the unified database.
    *   The `get_spoti_client` dependency handles token fetching and refreshing from the database.

*   **Playlist Synchronization**:
    *   The `sync_playlists` method in the `SpotifyAdapter` saves all playlist data to the unified database.

---

## Downloads Subsystem Design

**Goal:** To provide a persistent and robust download management system using the unified database.

*   **API Endpoints (`routes/downloads.py`)**:
    *   The route handlers use the `get_db` dependency to get a database session.

*   **Service Layer (`services/download_service.py`)**:
    -   The service is a set of stateless functions that use the CRUD layer to interact with the `download_jobs` table.

---

## Ongoing Maintenance
All development tasks must follow the [Task Execution Checklist](./task_checklist.md) to ensure consistency, quality, and security.
