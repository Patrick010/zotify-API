# Low-Level Design (LLD) – Zotify API

## Purpose
This LLD describes the specific implementation details of the Zotify API's subsystems, with a focus on the new provider-agnostic architecture.

---

## API Endpoint Baseline {#lld-api-endpoint-baseline}

This table provides a canonical overview of all planned and implemented endpoints for the Zotify API. It serves as the human-readable counterpart to the authoritative baseline defined in `api/endpoints.yaml`.

| Module      | Path                         | Methods               | Status        |
|-------------|------------------------------|-----------------------|---------------|
| **auth**    | `/api/auth/login`            | `POST`                | `planned`     |
|             | `/api/auth/logout`           | `POST`                | `planned`     |
|             | `/api/auth/status`           | `GET`                 | `implemented` |
| **user**    | `/api/user/profile`          | `GET`                 | `implemented` |
|             | `/api/user/preferences`      | `GET`, `PUT`          | `implemented` |
|             | `/api/user/liked`            | `GET`                 | `implemented` |
|             | `/api/user/history`          | `GET`                 | `implemented` |
|             | `/api/user/library`          | `GET`                 | `planned`     |
| **playlists** | `/api/playlists`             | `GET`, `POST`         | `implemented` |
|             | `/api/playlists/{id}`        | `GET`, `PUT`, `DELETE`| `planned`     |
|             | `/api/playlists/{id}/tracks` | `GET`, `POST`, `DELETE`| `planned`     |
| **tracks**  | `/api/tracks`                | `GET`                 | `implemented` |
|             | `/api/tracks/{id}`           | `GET`                 | `planned`     |
|             | `/api/tracks/{id}/download`  | `POST`                | `planned`     |
| **downloads** | `/api/downloads/status`      | `GET`                 | `implemented` |
|             | `/api/downloads/{id}/cancel` | `POST`                | `planned`     |
| **system**  | `/api/system/status`         | `GET`                 | `implemented` |
|             | `/api/system/storage`        | `GET`                 | `implemented` |
|             | `/api/system/logs`           | `GET`                 | `implemented` |
|             | `/api/system/uptime`         | `GET`                 | `implemented` |
|             | `/api/system/env`            | `GET`                 | `implemented` |
| **cache**   | `/api/cache`                 | `GET`, `DELETE`       | `implemented` |
| **config**  | `/api/config`                | `GET`, `PUT`          | `implemented` |
| **network** | `/api/network`               | `GET`                 | `implemented` |
| **search**  | `/api/search`                | `GET`                 | `implemented` |
| **webhooks**| `/api/webhooks`              | `POST`, `DELETE`      | `implemented` |
| **meta**    | `/ping`                      | `GET`                 | `implemented` |
|             | `/health`                    | `GET`                 | `implemented` |
|             | `/version`                   | `GET`                 | `implemented` |
|             | `/api/schema`                | `GET`                 | `implemented` |
|             | `/openapi.json`              | `GET`                 | `implemented` |
|             | `/docs`                      | `GET`                 | `implemented` |
|             | `/docs/oauth2-redirect`      | `GET`                 | `implemented` |
|             | `/redoc`                     | `GET`                 | `implemented` |
| **privacy** | `/privacy/data`              | `GET`, `DELETE`       | `planned`     |

---

## API Middleware {#lld-api-middleware}

The FastAPI application uses several middleware to provide cross-cutting concerns.

*   **CORS (Cross-Origin Resource Sharing)**:
    *   **Module:** `api/src/zotify_api/main.py`
    *   **Purpose:** To allow web-based clients (like `gonk-testUI`) hosted on different origins (IP/port) to communicate with the API. This is a browser security requirement.
    *   **Configuration:** The middleware is configured to be permissive, allowing all origins, methods, and headers (`*`). This is suitable for a local development tool but would need to be reviewed for a production deployment.

*   **Request ID**:
    *   **Module:** `api/src/zotify_api/middleware/request_id.py`
    *   **Purpose:** Injects a unique ID into every incoming request for improved logging and traceability.

---

## Provider Abstraction Layer {#lld-provider-abstraction-layer}

**Goal:** To decouple the core application logic from specific music service providers, allowing for future expansion to other services. This layer serves as a first-generation implementation of this principle. The long-term architectural vision is to supersede this with a dynamic plugin system, as detailed in [`DYNAMIC_PLUGIN_PROPOSAL.md`](./proposals/DYNAMIC_PLUGIN_PROPOSAL.md).

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

## Unified Database Architecture {#lld-unified-database-architecture}

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

## Spotify Integration Design {#lld-spotify-integration-design}

**Goal:** To provide a robust integration with the Spotify Web API, implemented as the first connector for the provider abstraction layer.

*   **Authentication & Token Storage**:
    *   The OAuth2 callback saves tokens to the unified database.
    *   The `get_spoti_client` dependency handles token fetching and refreshing from the database.

*   **Playlist Synchronization**:
    *   The `sync_playlists` method in the `SpotifyConnector` saves all playlist data to the unified database.

---

## Configuration Management {#lld-configuration-management}

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

## Downloads Subsystem Design {#lld-downloads-subsystem-design}

**Goal:** To provide a persistent and robust download management system using the unified database.

*   **API Endpoints (`routes/downloads.py`)**:
    *   The route handlers use the `get_db` dependency to get a database session.

*   **Service Layer (`services/download_service.py`)**:
    -   The service is a set of stateless functions that use the CRUD layer to interact with the `download_jobs` table.

---

---

## Generic Error Handling Module {#lld-generic-error-handling-module}

**Goal:** To centralize all exception handling in a single, configurable, and extensible module.

**Module:** `api/src/zotify_api/core/error_handler/`

*   **`main.py` or `__init__.py`**:
    *   Contains the core `ErrorHandler` class.
    *   This class will hold the logic for processing exceptions, formatting responses, and logging.
    *   It will be instantiated as a singleton early in the application lifecycle.

*   **`hooks.py`**:
    *   Contains the functions responsible for integrating the `ErrorHandler` with the rest of the system.
    *   `register_fastapi_hooks(app, handler)`: Adds a custom exception handler to the FastAPI application to catch `HTTPException` and standard `Exception`.
    *   `register_system_hooks(handler)`: Sets `sys.excepthook` and the `asyncio` event loop's exception handler to route all other unhandled exceptions to the `ErrorHandler`.

*   **`config.py`**:
    *   Defines the Pydantic models for the error handler's configuration, including the schema for defining triggers and actions.
    *   The configuration will be loaded from a separate file (e.g., `error_handler_config.yaml`).

*   **`triggers.py`**:
    *   Implements the logic for the trigger/action system.
    *   A `TriggerManager` class will read the configuration and execute actions (e.g., calling a webhook, sending an email) when a matching exception is processed by the `ErrorHandler`.

*   **`formatter.py`**:
    *   Contains different formatter classes for standardizing the error output.
    *   `JsonFormatter`: For API responses.
    *   `PlainTextFormatter`: For CLI tools and logs.
    *   The active formatter will be determined by the context (e.g., an API request vs. a background task).

---

## Flexible Logging Framework {#lld-flexible-logging-framework}

**Goal:** To provide a developer-centric, configurable, and asynchronous logging framework.

**Module:** `api/src/zotify_api/core/logging_framework/`

*   **`schemas.py`**:
    *   Defines the Pydantic models for validating the `logging_framework.yml` configuration file.
    *   The `TriggerConfig` model now supports both `event` and `tag` based triggers, with a validator to ensure mutual exclusivity.

*   **`service.py`**:
    *   **`LoggingService`**: Implemented as a singleton, this class is the core of the framework. It loads the validated configuration, instantiates sinks, and dispatches log events.
    *   **Trigger Handling**: The service now supports two types of triggers defined in the YAML: event-based triggers (which are destructive and replace the original log) and tag-based triggers (which are non-destructive and route a copy of the log to a new destination).

*   **`filters.py`**:
    *   Contains the `SensitiveDataFilter`, a `logging.Filter` subclass that uses regex to find and redact sensitive information (tokens, codes) from log messages before they are processed by any sink.

*   **`main.py` (Application Entry Point)**:
    *   The `initialize_logging_framework` function is called on startup.
    *   It reads `logging_framework.yml`, expands any environment variables (e.g., `${VAR}`), and then loads the configuration.
    *   If the `APP_ENV` is set to `production`, it programmatically adds the `SensitiveDataFilter` to the root logger, enabling global, automatic redaction of sensitive data.

*   **`__init__.py`**:
    *   Exposes the primary public API function, `log_event()`.

*   **Configuration (`api/logging_framework.yml`)**:
    *   A YAML file where all sinks and triggers (both event-based and tag-based) are defined.

*   **Reload Endpoint (`routes/system.py`)**:
    *   The `POST /api/system/logging/reload` endpoint allows for hot-reloading the configuration from `logging_framework.yml`.

*   **Future Extensibility (Plugin System)**:
    *   To allow for true extensibility without modifying the core API, a dynamic plugin system has been proposed. This would allow developers to create and install their own custom sink types as separate packages. See [`DYNAMIC_PLUGIN_PROPOSAL.md`](./DYNAMIC_PLUGIN_PROPOSAL.md) for details.

---

## Supporting Modules {#lld-supporting-modules}

This section describes the low-level design of the official supporting modules for the Zotify Platform.

### Gonk-TestUI {#lld-gonk-testui}

**Purpose:** A standalone developer tool for testing the Zotify API.

*   **Backend (`app.py`):** A lightweight Flask server.
    *   Serves the static frontend files (`index.html`, `css`, `js`).
    *   Provides server-side logic for launching and stopping the `sqlite-web` process.
    *   Accepts command-line arguments (`--ip`, `--port`, `--api-url`) to configure the server and the target API URL.
*   **Frontend (`static/`):** A single-page application built with plain JavaScript.
    *   Dynamically fetches the API's `openapi.json` schema to build forms for each endpoint.
    *   Uses `fetch` to make live API calls.
    *   Includes a theme toggle with preferences saved to `localStorage`.
*   **Templating:** The `index.html` is rendered as a Flask template to allow the backend to inject the configurable `--api-url` into the frontend at runtime.

### Snitch {#lld-snitch}

**Purpose:** A helper application to securely manage the OAuth callback flow for CLI clients.

*   **Architecture:** A self-contained, single-file Go application (`snitch.go`) that runs a temporary local web server. The single-file structure was adopted to resolve a persistent and complex build issue.
*   **Security:** It uses a Zero Trust security model with end-to-end payload encryption to protect the authorization code. It also redacts sensitive data from its logs when the `APP_ENV` is set to `production`.
*   **Detailed Design:** For the full low-level design, including the cryptographic workflow, please refer to the canonical design documents in the `snitch/docs/` directory.

---

## Ongoing Maintenance {#lld-ongoing-maintenance}
All development tasks must follow the [Task Execution Checklist](./TASK_CHECKLIST.md) to ensure consistency, quality, and security.

---

## Privacy Subsystem (GDPR Compliance) {#lld-privacy-subsystem}

**Goal:** To provide endpoints that allow users to export and delete their personal data, in compliance with GDPR.

*   **`GET /privacy/data`**:
    *   **Description:** Exports all personal data related to the authenticated user. The data should be returned in a machine-readable JSON format.
    *   **Authentication:** Requires user authentication (e.g., via a future JWT implementation). For now, it will be protected by the admin API key.
    *   **Response Body (Success 200 OK):**
        ```json
        {
          "user_id": "string",
          "profile": { },
          "playlists": [ ],
          "liked_songs": [ ],
          "download_history": [ ]
        }
        ```

*   **`DELETE /privacy/data`**:
    *   **Description:** Deletes all personal data related to the authenticated user. This is a destructive action and should be handled with care.
    *   **Authentication:** Requires user authentication. For now, it will be protected by the admin API key.
    *   **Response Body (Success 204 No Content):** Empty response.
