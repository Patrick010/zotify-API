# Operator Manual

This guide provides instructions for deploying, configuring, and maintaining the Zotify API.

## 1. Deployment

Deployment of the Zotify API is handled via standard Python packaging and can be run in any environment that supports Python 3.10+.

### 1.1. Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Patrick010/zotify-API.git
    cd zotify-API
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    The project uses `pip` for dependency management.
    ```bash
    pip install -r requirements.txt
    ```

### 1.2. Running the Application

The application is run using `uvicorn`, a high-performance ASGI server.

```bash
uvicorn zotify_api.main:app --host 0.0.0.0 --port 8000
```

You can configure the host and port as needed.

## 2. Configuration

The application is configured through environment variables and a `logging_config.yml` file.

### 2.1. Main Application

The main application settings are managed in `zotify_api/config.py` and are sourced from environment variables. The following variables are required:

*   `APP_ENV`: The application environment. Set to `production` for live environments, or `test` for running the test suite.
*   `ADMIN_API_KEY`: A secret key required for accessing administrative endpoints.
*   `DATABASE_URI`: The connection string for the SQLAlchemy database. Example: `sqlite:///./storage/zotify.db` or `postgresql://user:password@host:port/database`.

### 2.2. Logging Configuration

The logging system is configured via `logging_config.yml` in the project root. This file defines the handlers, their levels, and their specific parameters.

**Example `logging_config.yml`:**

```yaml
handlers:
  - type: console_handler
    levels: [DEBUG, INFO, WARNING, ERROR, CRITICAL]

  - type: json_audit_handler
    levels: [AUDIT]
    filename: "storage/audit.log"

  - type: database_job_handler
    levels: [JOB_STATUS]
```

**Handler Details:**

*   **`console_handler`**: Outputs plain-text logs to standard output.
*   **`json_audit_handler`**: Writes audit-level events to a JSON file. Ensure the specified `filename` path is writable by the application.
*   **`database_job_handler`**: Writes job status updates to the `job_logs` table in the database.

## 3. Maintenance

### 3.1. Database

The application uses SQLAlchemy and will create the necessary tables on startup if they do not exist, as defined by the models in `zotify_api/database/models.py`. No manual migration steps are required for initial setup.

### 3.2. Log Rotation

The `json_audit_handler` writes to a file that may grow over time. Standard log rotation tools like `logrotate` should be configured to manage this file to prevent excessive disk usage.
