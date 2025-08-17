# Zotify API - Operator Manual

This manual provides detailed, actionable guidance for deploying, configuring, and maintaining the Zotify API in a production environment.

---

## 1. Deployment Process

### Purpose
This section outlines the complete process for deploying the Zotify API server from the source code. It covers everything from cloning the repository to running the application with a process manager for production use.

### Command / Example
A typical deployment consists of the following sequence of commands, executed from the server's command line:
\`\`\`bash
# 1. Clone the repository from GitHub
git clone https://github.com/Patrick010/zotify-API.git
cd zotify-API

# 2. Set up a dedicated Python virtual environment to isolate dependencies
python3 -m venv venv
source venv/bin/activate

# 3. Install the application and its dependencies in editable mode
pip install -e ./api

# 4. Create required storage directories for the database and logs
mkdir -p api/storage

# 5. Create and populate the environment configuration file (see Configuration section)
# nano api/.env

# 6. Run the application server using a process manager like systemd (see below)
# For a quick foreground test, you can run uvicorn directly:
# uvicorn zotify_api.main:app --host 127.0.0.1 --port 8000
\`\`\`

### Usage Notes
- **User Permissions:** Ensure the user running the API has read/write permissions for the `api/storage` directory.
- **Production Server:** For production, it is strongly recommended to run `uvicorn` behind a reverse proxy like Nginx and manage the process using `systemd`. This provides SSL termination, load balancing, and process resilience.
- **Firewall:** Ensure the port the API runs on (e.g., 8000) is accessible from the reverse proxy, but not necessarily from the public internet.

---

## 2. Uvicorn Process Management

### Purpose
Run the Zotify API service using `uvicorn` for local development or production deployment.

### Command
\`\`\`bash
uvicorn zotify_api.main:app --host 127.0.0.1 --port 8000 --workers 4
\`\`\`

### Parameters / Flags
| Parameter/Flag        | Description                                                                                             | Notes                                                                                                                              |
| --------------------- | ------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `zotify_api.main:app` | The Python import path to the FastAPI `app` instance.                                                   | A required positional argument for uvicorn.                                                                                        |
| `--host <ip>`         | The IP address to bind the server to.                                                                   | Use `127.0.0.1` for production (to be accessed via reverse proxy). Use `0.0.0.0` inside a Docker container.                          |
| `--port <port>`       | The TCP port to listen on.                                                                              | Default: `8000`.                                                                                                                   |
| `--workers <int>`     | The number of worker processes to spawn.                                                                | For production use. A good starting point is `2 * (number of CPU cores) + 1`. Omit this flag for development.                      |
| `--reload`            | Enables auto-reloading the server when code changes are detected.                                       | **For development use only.** Do not use in production.                                                                            |

### Expected Output
A successful server start will display the following log messages:
\`\`\`
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
\`\`\`

### Common Issues / Troubleshooting
-   **Issue:** `Port 8000 already in use`
    -   **Solution:** Change the `--port` or find and stop the process currently using it with `sudo lsof -i :8000`.
-   **Issue:** `Environment variables not loaded`
    -   **Solution:** Confirm the `.env` file is located at `api/.env` and is readable by the service user. For `systemd`, ensure the `EnvironmentFile` path is correct.

---

## 3. Maintenance

### Purpose
Regular maintenance tasks to ensure the health and stability of the Zotify API.

### 3.1. Database Backup

#### Command
\`\`\`bash
# For PostgreSQL
pg_dump -U <db_user> -h <db_host> <db_name> > zotify_backup_$(date +%F).sql

# For SQLite
sqlite3 /path/to/api/storage/zotify.db ".backup /path/to/backup/zotify_backup_$(date +%F).db"
\`\`\`

#### Usage Notes
- This command should be run regularly via a `cron` job.
- Store backups in a secure, remote location.

### 3.2. Log Rotation

#### Purpose
The `json_audit.log` can grow indefinitely. Log rotation prevents it from consuming excessive disk space.

#### Command / Example
Configure `logrotate` by creating a file at `/etc/logrotate.d/zotify`:
\`\`\`
/path/to/api/storage/audit.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
    create 0640 your_user your_group
}
\`\`\`

#### Usage Notes
- This configuration rotates the log daily, keeps 7 compressed archives, and safely handles a missing log file.
- Adjust `daily`, `rotate`, and permissions as needed.

### References
- [Uvicorn Deployment Guide](https://www.uvicorn.org/deployment/)
- [Logrotate Man Page](https://man7.org/linux/man-pages/man8/logrotate.8.html)
