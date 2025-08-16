# Installation Guide

This document provides detailed instructions for installing and setting up the Zotify API.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

-   **Python 3.10 or greater**
-   **pip**: The Python package installer.
-   **Git**: For cloning the repository.
-   **FFmpeg**: (Optional, required for some download functionality) A cross-platform solution to record, convert and stream audio and video.

## Installation

This installation guide is for developers who want to run the API from the source code.

### 1. Clone the Repository

First, clone the project repository from GitHub to your local machine:
```bash
git clone <repository_url>
cd <repository_directory>
```

### 2. Install Dependencies

The API's dependencies are listed in `api/pyproject.toml`. You can install them using `pip`. It is recommended to use a Python virtual environment.

From the root of the project directory, run:
```bash
pip install -e ./api
```
This command installs all the necessary packages for the API to run.

### 3. Create Storage Directory

The application requires a `storage` directory inside the `api` directory to store its database and other temporary files. Create it before running the application for the first time:

```bash
mkdir api/storage
```

### 4. Configure the Environment

The API is configured using environment variables. `pydantic-settings` will automatically load them from a `.env` file in the `api/` directory.

**For local development and testing, you must set the application environment to `development`.** This disables production security checks and enables helpful defaults.

**Example `.env` file:**
```
# Set the environment to development mode
APP_ENV="development"

# Use a SQLite database located in the api/storage/ directory
DATABASE_URI="sqlite:///storage/zotify.db"

# You can optionally set the admin API key. If you don't, a default will be used in development mode.
# ADMIN_API_KEY="your_secret_key_here"
```

### 5. Running the API

A startup script is provided to manage the application's lifecycle. This script ensures that all necessary checks are performed before starting the server.

Before running the script, make sure it is executable:
```bash
chmod +x scripts/start.sh
```

Now, you can run the API server using the script:
```bash
./scripts/start.sh
```
The API server will start, and it will be accessible at **`http://localhost:8000`**.

## Developer Tools (`gonk-testUI`)

The project includes a standalone developer UI for testing the API. For instructions on how to install and run it, please see the `README.md` file inside the `gonk-testUI/` directory.
