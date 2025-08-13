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

## Privacy and Compliance

-   **Audit Logs**: The application generates logs that can be used for auditing purposes. It is recommended to ship these logs to a centralized logging system for analysis and retention.
-   **Data Management**: All user-related data is stored in the unified database. Operators should be familiar with the database schema (`api/src/zotify_api/database/models.py`) to handle data access or deletion requests if necessary.
