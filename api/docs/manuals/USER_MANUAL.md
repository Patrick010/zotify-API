# Zotify API - User Manual

This manual documents the full capabilities of the Zotify API, designed for managing media libraries, metadata, playlists, downloads, and configuration.

---

## Architectural Overview

The Zotify API is a developer-centric framework built to provide powerful, automation-oriented functionality for interacting with music services like Spotify.

The architecture is built on a few key principles:
-   **Service-Oriented**: The API is divided into a series of services, each responsible for a specific domain (e.g., downloads, playlists).
-   **Unified Database**: All persistent data (download jobs, playlists, user tokens, etc.) is stored in a single, unified database. This is managed by a backend-agnostic persistence layer built on SQLAlchemy, allowing you to use different database systems (e.g., SQLite, PostgreSQL).
-   **Provider Abstraction (Future)**: The API is being designed to support multiple music providers in the future. Spotify is the first implemented provider, but the architecture is being built to accommodate others.

---

## Authentication

The Zotify API uses the **OAuth 2.0 Authorization Code Flow with PKCE** to securely connect to a user's Spotify account.

The flow is as follows:
1.  **Initiate Login**: A client sends a `GET` request to `/api/spotify/login`.
2.  **User Authorization**: The API returns a Spotify authorization URL. The user must open this URL in a browser and grant permission.
3.  **Callback**: After the user grants permission, Spotify redirects the browser to the configured `REDIRECT_URI`. In a local development environment, this is typically handled by the `snitch` helper application.
4.  **Token Exchange**: The API's callback endpoint (`/api/spotify/callback`) receives the authorization code, validates it, and securely exchanges it for an access token and a refresh token.
5.  **Token Persistence**: The access and refresh tokens are then stored securely in the unified database. The system will automatically use the refresh token to get a new access token when the old one expires.

## API Testing with `gonk-testUI`

A standalone developer tool, `gonk-testUI`, is provided to make testing the API easy. It provides a web UI to browse all API endpoints, generate forms for them, and view responses. It also includes an embedded database browser.

For instructions on how to set up and run this tool, please see the `README.md` file inside the `gonk-testUI/` directory.

---

## API Endpoints

This section provides a summary of the available API endpoints. For a complete, machine-readable specification, please refer to the OpenAPI schema at the `/openapi.json` endpoint of the running API.

### Authentication (`/spotify`)

-   `GET /login`: Initiates the Spotify OAuth2 login flow.
-   `GET /callback`: The callback endpoint for the OAuth2 flow.
-   `GET /token_status`: Checks the status of the current Spotify API token.

### Playlists (`/spotify`)

-   `POST /sync_playlists`: Triggers a full sync of the user's playlists from Spotify to the local database.
-   `GET /playlists`: Lists playlists from Spotify.
-   `POST /playlists`: Creates a new playlist on Spotify.
-   ... and other CRUD operations for playlists and their tracks.

### Downloads (`/download`)

-   `POST /`: Queues one or more tracks for download. The job is added to a persistent queue in the database.
-   `GET /status`: Returns the current status of all jobs in the download queue.
-   `POST /retry`: Retries all failed download jobs.
-   `POST /process`: Manually triggers the processing of one job from the queue.

### Other Endpoints

The API also provides endpoints for managing:
-   **System**: Health checks, environment info, etc. (`/system`)
-   **Configuration**: Reading and updating the application's configuration. (`/config`)
-   **Logging**: Managing log levels. (`/logging`)
-   ... and more. Please refer to the `/openapi.json` schema for a complete list.
