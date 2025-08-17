# Developer Guide

This guide provides instructions for developers working on the Zotify API. It covers the project architecture, development setup, and contribution guidelines.

## 1. Project Architecture

The Zotify API follows a standard layered architecture, separating concerns into distinct modules. The main components are located within the `src/zotify_api/` directory.

*   **`main.py`**: The FastAPI application entry point. It initializes the app, middleware, and routers.
*   **`routes/`**: Contains the API endpoint definitions. Each file corresponds to a logical feature set (e.g., `download.py`, `playlists.py`).
*   **`services/`**: Contains the business logic for the application. Services are called by the route handlers and are responsible for coordinating tasks.
*   **`database/`**: Manages all database interactions.
    *   `session.py`: Defines the SQLAlchemy engine, session factory, and the declarative `Base`.
    *   `models.py`: Defines all SQLAlchemy ORM models.
    *   `crud.py`: Contains functions for Create, Read, Update, and Delete operations on the database models.
*   **`schemas/`**: Defines the Pydantic models used for API request and response validation.
*   **`core/`**: Contains core, cross-cutting concerns.
    *   `error_handler/`: A robust system for handling and acting on exceptions. See `ERROR_HANDLING_GUIDE.md` for more details.
    *   `logging_handlers/`: Contains the custom handlers for the application's logging service.
*   **`config.py`**: Manages application settings, sourced from environment variables.

## 2. Development Setup

Follow the installation instructions in the [Operator Manual](OPERATOR_MANUAL.md). For development, it is highly recommended to use a virtual environment.

### 2.1. Running in Development Mode

To run the server with hot-reloading enabled for development:

```bash
uvicorn zotify_api.main:app --reload
```

### 2.2. Running Tests

The project uses `pytest`. Tests are located in the `tests/` directory.

1.  **Set the test environment:**
    The application requires the `APP_ENV` variable to be set to `test` to use test-specific configurations.

2.  **Run the full suite:**
    From the `/app/api` directory:
    ```bash
    APP_ENV=test python3 -m pytest
    ```

3.  **Run a specific test file:**
    ```bash
    APP_ENV=test python3 -m pytest tests/unit/test_new_logging_system.py
    ```

## 3. Contribution Guidelines

### 3.1. Adding a New API Endpoint

1.  **Define the Schema:** Create request/response Pydantic models in the appropriate file in `src/zotify_api/schemas/`.
2.  **Add CRUD operations:** If the endpoint interacts with the database, add the necessary functions to `src/zotify_api/database/crud.py`.
3.  **Create the Service Logic:** Add a new function to the relevant service file in `src/zotify_api/services/` to implement the business logic.
4.  **Create the Route:** Add the new endpoint to the appropriate router file in `src/zotify_api/routes/`.
5.  **Write Tests:** Add a new test file in `tests/` to verify the functionality of your new endpoint.

### 3.2. Adding a New Error Handler Action

The error handling system is designed to be extensible. To add a new action:

1.  Create a new Python file in `src/zotify_api/core/error_handler/actions/`.
2.  In this file, define a class that inherits from `BaseAction`.
3.  Implement the `run(self, context: dict)` method.
4.  The action will be dynamically loaded by the `TriggerManager` based on its filename. No further registration is required.

Refer to `ERROR_HANDLING_GUIDE.md` for a full explanation of the error handling system.
