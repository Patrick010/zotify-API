# Zotify API - Developer Guide

**Version:** 1.1
**Date:** 2025-08-18

## 1. Introduction

This guide provides developers with the necessary information to set up a local development environment, run the server, execute tests, and interact with the Zotify API. It is intended for those who wish to contribute to the project or build applications on top of the API.

## 2. Local Development Setup

### 2.1. Prerequisites
-   Python 3.10+
-   `pip` and `venv` for package management
-   Git for cloning the repository

### 2.2. Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Patrick010/zotify-API.git
    cd zotify-API
    ```

2.  **Install Dependencies**
    It is highly recommended to use a virtual environment to isolate dependencies. The `start.sh` script assumes this setup.
    ```bash
    # Create and activate a virtual environment
    python3 -m venv .venv
    source .venv/bin/activate

    # Install the API and its dependencies in editable mode
    pip install -e ./api
    ```

### 2.3. Configuration

The API is configured primarily through **environment variables**. The `pydantic-settings` library automatically reads these variables on startup. For a full list of available settings, see `api/src/zotify_api/config.py`.

The most important variable is `APP_ENV`, which can be `development` or `production`. The provided startup script sets this to `development` for you.

### 2.4. Running the API Server (Recommended Method)

The easiest and recommended way to run the API for local development is to use the provided startup script.

**Command (from the project root):**
```bash
./scripts/start.sh
```

**What this script does:**
-   Sets `APP_ENV=development`, which enables debug features and uses sensible defaults.
-   Creates the necessary `api/storage` and `api/logs` directories.
-   Launches the `uvicorn` server with hot-reloading, so the server will automatically restart when you save a file.

The API will be available at `http://localhost:8000`. The interactive OpenAPI (Swagger) documentation will be at `http://localhost:8000/docs`.

## 3. Running the Test Suite

The test suite is a critical part of the development process.

**Command (from the project root):**
```bash
# Ensure you are in the virtual environment
source .venv/bin/activate

# Run the tests
pytest api/
```

**Important:** The tests are designed to run in a test environment, which is automatically configured when `pytest` runs. They use a temporary, in-memory SQLite database to ensure they do not interfere with your local development database.

## 4. Interacting with the API

While the interactive docs at `http://localhost:8000/docs` are the easiest way to test endpoints, you can also use `curl`.

**Note:** The `start.sh` script sets a default `ADMIN_API_KEY` of `test_key` for development. All administrative endpoints require this key to be passed in the `X-API-Key` header.

### Example: Checking Health
```bash
curl http://localhost:8000/api/health
```

### Example: Getting Authentication Status
```bash
curl -X GET http://localhost:8000/api/auth/status -H "X-API-Key: test_key"
```
**Expected Response:**
```json
{
  "data": {
    "is_authenticated": false,
    "expires_at": null
  }
}
```

### Example: Triggering a Download
```bash
curl -X POST http://localhost:8000/api/downloads \
  -H "X-API-Key: test_key" \
  -H "Content-Type: application/json" \
  -d '{"track_ids": ["spotify:track:4cOdK2wGLETOMsV3oDPEhB"]}'
```

## 5. Code Quality & Verification

Maintaining code quality is essential. All contributions must pass both static analysis checks and the full test suite.

### 5.1. Static Analysis with `mypy`

This project uses `mypy` to enforce strict static type checking. All code is fully type-hinted. Before submitting any code, you must run `mypy` and ensure there are no errors.

**Command (from the project root):**
```bash
# Ensure you are in the virtual environment
source .venv/bin/activate

# Run mypy with the project's config file
mypy --config-file api/mypy.ini api/src api/tests
```
Any `mypy` errors must be resolved before a pull request will be accepted.

### 5.2. Running the Test Suite

The test suite is built on `pytest`. It is critical to run the full suite to ensure your changes have not introduced any regressions.

**Prerequisites:**
- Ensure you are in the activated virtual environment.
- Make sure the required directories exist, as the application will fail to start without them:
  ```bash
  mkdir -p api/storage api/logs
  ```

**Command (from the project root):**
```bash
# Run the tests with the correct environment setting
APP_ENV=test pytest api/
```

**Important:** The tests are designed to run in a `test` environment, which is automatically configured when `pytest` runs. They use a temporary, in-memory SQLite database for most tests to ensure they do not interfere with your local development database, but some components may interact with the file system, hence the need for the directories above.

## 6. Key Documentation

For more detailed information, please consult the following documents:
-   **[Project Registry](./../../project/PROJECT_REGISTRY.md):** The master list of all project documents.
-   **[Logging Guide](./LOGGING_GUIDE.md):** A deep dive into the Flexible Logging Framework.
-   **[High-Level Design](./../../project/HIGH_LEVEL_DESIGN.md):** An overview of the platform's architecture.
-   **[Low-Level Design](./../../project/LOW_LEVEL_DESIGN.md):** Detailed implementation notes for various subsystems.
