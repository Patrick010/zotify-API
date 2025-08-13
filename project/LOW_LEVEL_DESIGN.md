# Low-Level Design (LLD) – Zotify API

## Purpose
This LLD describes the specific implementation details of the Zotify API's subsystems, with a focus on the new provider-agnostic architecture.

---

## API Middleware

The FastAPI application uses several middleware to provide cross-cutting concerns.

*   **CORS (Cross-Origin Resource Sharing)**:
    *   **Module:** `api/src/zotify_api/main.py`
    *   **Purpose:** To allow web-based clients (like `gonk-testUI`) hosted on different origins (IP/port) to communicate with the API. This is a browser security requirement.
    *   **Configuration:** The middleware is configured to be permissive, allowing all origins, methods, and headers (`*`). This is suitable for a local development tool but would need to be reviewed for a production deployment.

*   **Request ID**:
    *   **Module:** `api/src/zotify_api/middleware/request_id.py`
    *   **Purpose:** Injects a unique ID into every incoming request for improved logging and traceability.

---

## Provider Abstraction Layer

**Goal:** To decouple the core application logic from specific music service providers, allowing for future expansion to other services.

**Module:** `api/src/zotify_api/providers/`

*   **`base.py`**:
    *   Defines the `BaseProvider` abstract base class.
    *   This class specifies the common interface that all provider connectors must implement (e.g., `search`, `get_playlist`).

*   **`spotify_connector.py`**:
    *   Contains the `SpotifyConnector` class, which implements the `BaseProvider` interface for the Spotify service.
    *   All Spotify-specific logic, including calls to the `SpotiClient`, is encapsulated within this connector.

*   **Dependency (`services/deps.py`)**:
    *   A new `get_provider` dependency is responsible for instantiating and returning the currently active provider connector. For now, it always returns the `SpotifyConnector`.

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

**Goal:** To provide a robust integration with the Spotify Web API, implemented as the first connector for the provider abstraction layer.

*   **Authentication & Token Storage**:
    *   The OAuth2 callback saves tokens to the unified database.
    *   The `get_spoti_client` dependency handles token fetching and refreshing from the database.

*   **Playlist Synchronization**:
    *   The `sync_playlists` method in the `SpotifyConnector` saves all playlist data to the unified database.

---

## Configuration Management

The application uses a dual system for managing configuration, separating immutable startup settings from mutable runtime settings.

*   **Startup Configuration (`config.py`)**:
    *   **Purpose**: Manages core, system-level settings required for the application to boot (e.g., `database_uri`, `admin_api_key`).
    *   **Source**: Settings are loaded from environment variables using `pydantic-settings`.
    *   **Mutability**: These settings are considered immutable and are only read once at startup. They cannot be changed at runtime.

*   **Application Configuration (`config_service.py`)**:
    *   **Purpose**: Manages user-facing application settings that can be changed during operation (e.g., `library_path`, `scan_on_startup`).
    *   **Source**: Settings are persisted in a `config.json` file.
    *   **Mutability**: These settings can be read and updated at runtime via the `/api/config` endpoints (`GET`, `PATCH`, `POST /reset`).

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
