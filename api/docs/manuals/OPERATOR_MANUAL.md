# Zotify API - Operator's Manual

**Version:** 1.1
**Date:** 2025-08-18

## 1. Introduction

This manual provides detailed, actionable guidance for deploying, configuring, and maintaining the Zotify API in a production or semi-production environment. It assumes you have a working knowledge of Linux system administration, process management, and networking.

## 2. Deployment

### 2.1. Initial Setup

The following steps will get the application code and dependencies installed on a fresh Debian/Ubuntu server.

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Patrick010/zotify-API.git
    cd zotify-API
    ```

2.  **Install Dependencies:**
    Use a virtual environment to isolate the application.
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -e ./api
    ```

### 2.2. Production Service (systemd)

For a robust production deployment, it is essential to run the API as a managed service. The following is an example of a `systemd` service file.

**Create the service file:**
```bash
sudo nano /etc/systemd/system/zotify-api.service
```

**Paste the following content:**
```ini
[Unit]
Description=Zotify API Service
After=network.target

[Service]
# Replace 'your_user' with the user you want to run the service as
User=your_user
Group=your_user
# The working directory should be the /api folder
WorkingDirectory=/path/to/zotify-API/api
# The command to start the server. Note the absolute path to uvicorn in the venv.
ExecStart=/path/to/zotify-API/.venv/bin/uvicorn zotify_api.main:app --host 127.0.0.1 --port 8000 --workers 4
# Set environment variables here
Environment="APP_ENV=production"
Environment="ADMIN_API_KEY=your_super_secret_key"
# Add other environment variables as needed

[Install]
WantedBy=multi-user.target
```

**Enable and start the service:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable zotify-api.service
sudo systemctl start zotify-api.service
sudo systemctl status zotify-api.service
```

## 3. Configuration

Configuration is managed via environment variables and the `logging_framework.yml` file.

### 3.1. Environment Variables

-   **`APP_ENV`**: The most critical variable. Set to `production` for any non-development environment. This enables security features like sensitive data redaction in logs.
-   **`ADMIN_API_KEY`**: A mandatory secret key required to access any administrative or system-level endpoints.
-   **`DATABASE_URI`**: The connection string for the database. Defaults to SQLite but can be pointed to a production PostgreSQL instance.

### 3.2. Logging Configuration

The behavior of the logging system is controlled by `api/logging_framework.yml`. This file allows you to define log sinks, set levels, and create routing rules. This file can be reloaded at runtime without restarting the server.

**To reload the logging configuration:**
Send an authenticated `POST` request to `/api/system/logging/reload`.
```bash
curl -X POST http://localhost:8000/api/system/logging/reload -H "X-API-Key: your_super_secret_key"
```

## 4. Maintenance

### 4.1. Log Rotation

The application creates log files in the `api/logs/` directory (e.g., `debug.log`, `security.log`). In a production environment, these files must be rotated to prevent them from consuming excessive disk space.

**Example `logrotate` configuration:**
Create a file at `/etc/logrotate.d/zotify-api`:
```
/path/to/zotify-API/api/logs/*.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    create 0640 your_user your_group
}
```
This configuration rotates all `.log` files in the directory daily, keeping 14 compressed archives.

### 4.2. Database Backup

Regular backups of the application database are critical.

**Example SQLite backup command:**
```bash
sqlite3 /path/to/zotify-API/api/storage/zotify.db ".backup /path/to/backups/zotify_$(date +%F).db"
```
This command should be run regularly via a `cron` job, and backups should be stored securely.

## 5. Monitoring

-   **Health Check:** A simple health check endpoint is available at `/api/health`. Monitoring systems should be configured to check this endpoint regularly.
-   **Log Monitoring:** The `api/logs/security.log` file should be monitored for any unusual activity. In a production environment, consider forwarding this log to a centralized security information and event management (SIEM) system.
