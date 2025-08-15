# Operator Guide

This guide provides instructions for operators on how to manage and maintain the Zotify API in a production or development environment.

## Admin API Key Management

The Zotify API uses an admin API key to protect administrative endpoints.

### Configuration

It is strongly recommended to set a secure, random admin API key using an environment variable. This can be done by creating a `.env` file in the `api/` directory.

**Example `.env` file:**
```
ADMIN_API_KEY="your-super-secret-and-randomly-generated-key"
```
The application will load this key on startup. In a production environment (`APP_ENV="production"`), the application will refuse to start unless an admin API key is provided.

**Development Note:** If the `APP_ENV` is set to `development` (which is the default in `scripts/start.sh`) and no `ADMIN_API_KEY` is provided, the application will automatically use a default, non-secure key: `test_key`. A warning will be printed to the console when this happens.

### Using the Admin API Key

To make requests to protected endpoints, include the API key in the `X-API-Key` header:
```bash
curl -H "X-API-Key: your-super-secret-and-randomly-generated-key" http://localhost:8000/api/some-protected-endpoint
```

## Database Management

All application data, including download jobs, playlists, and user tokens, is stored in a unified database configured via the `DATABASE_URI` environment variable.

### Backup

It is critical to back up the database regularly to prevent data loss. The backup strategy depends on the database backend you are using:

-   **SQLite**: If you are using a SQLite database, the entire database is contained in a single file (e.g., `api/storage/zotify.db`). You should back up this file regularly using standard file backup procedures.
-   **PostgreSQL / MySQL / Other**: If you are using a dedicated database server, you should use the database's own backup tools (e.g., `pg_dump` for PostgreSQL) to create regular backups.

### Maintenance

Regular database maintenance, such as vacuuming (for SQLite) or other optimization tasks, should be performed as recommended by the documentation for your chosen database backend.

## Network Configuration

### CORS (Cross-Origin Resource Sharing)

The API includes a permissive Cross-Origin Resource Sharing (CORS) policy by default. This is required for browser-based applications (like the provided `gonk-testUI`) to be able to communicate with the API when served from a different origin (i.e., a different port).

-   **Default Policy:** The default configuration allows requests from all origins, with all methods and headers.
-   **Production:** For a production deployment, you may want to review this policy and restrict the allowed origins to only trusted domains. This configuration is located in `api/src/zotify_api/main.py`.

## Error Handling and Monitoring

The Zotify API includes a centralized error handling module that captures all unhandled exceptions across the platform. This system ensures consistent error responses and allows for automated actions in response to specific problems.

### Configuration

The behavior of the error handling module is controlled by a configuration file, which will be located at `api/config/error_handler_config.yaml`.

#### 1. Verbosity

You can control the level of detail in error responses by setting the `verbosity` key.

-   **`production` (default):** Error responses are minimal and do not include sensitive internal details like tracebacks. This is the recommended setting for any user-facing environment.
-   **`debug`:** Error responses include the full exception type, message, and traceback. This should only be used in controlled development or staging environments.

**Example `error_handler_config.yaml`:**
```yaml
verbosity: production
```

#### 2. Automated Actions (Triggers)

The system can be configured to automatically perform actions when specific types of errors occur. This is useful for sending alerts or notifications.

**Example Configuration:**
```yaml
# error_handler_config.yaml
verbosity: production
triggers:
  # This trigger will fire whenever a connection to an external service fails.
  - exception_type: requests.exceptions.ConnectionError
    actions:
      # Action 1: Log a critical message to the main log file.
      - type: log_critical
        message: "CRITICAL: Connection to an external provider failed. Check network connectivity."

      # Action 2: Send a notification to a Slack webhook.
      - type: webhook
        url: "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"
        payload:
          text: "🚨 Zotify API Alert: Provider connection error detected!"
```
To enable this, create the `error_handler_config.yaml` file and define your triggers and actions according to the schema in `ERROR_HANDLING_DESIGN.md`.

### Interpreting Error Logs

All unhandled exceptions are logged with a full traceback to the main application log. When an error occurs, look for a log entry containing the full exception details. The error message will include a unique `request_id` if the error originated from an API request, which can be used to correlate it with other log entries.

## Privacy and Compliance

-   **Audit Logs**: The application generates logs that can be used for auditing purposes. It is recommended to ship these logs to a centralized logging system for analysis and retention.
-   **Data Management**: All user-related data is stored in the unified database. Operators should be familiar with the database schema (`api/src/zotify_api/database/models.py`) to handle data access or deletion requests if necessary.
