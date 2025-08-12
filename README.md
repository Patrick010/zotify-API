# Zotify API

This repository contains the source code for the Zotify API, a RESTful service for interacting with the Zotify music and podcast downloader.

## Getting Started

### 1. Installation

For detailed installation instructions, please see the [Installation Guide](./docs/system/INSTALLATION.md).

In summary:
-   Clone the repository.
-   Install the API dependencies: `pip install -e ./api`
-   Install the developer UI dependencies: `pip install -e ./gonk-testUI`

### 2. Configuration

The API requires a database connection string to be configured via a `DATABASE_URI` environment variable.

Create a `.env` file in the `api/` directory:
```
# Example for a SQLite database
DATABASE_URI="sqlite:///storage/zotify.db"
```

### 3. Running the API

A startup script is provided to run the API server.

First, make the script executable:
```bash
chmod +x scripts/start.sh
```

Then, run the script from the root of the project:
```bash
./scripts/start.sh
```
The API will be available at `http://localhost:8000`.

## Documentation

Comprehensive system documentation is available in the `docs/system` directory.

-   **[Installation Guide](./docs/system/INSTALLATION.md)**
-   **[User Manual](./docs/system/USER_MANUAL.md)**
-   **[Developer Guide](./docs/system/DEVELOPER_GUIDE.md)**
-   **[Operator Guide](./docs/system/OPERATOR_GUIDE.md)**
-   **[System Requirements](./docs/system/REQUIREMENTS.md)**

## Developer Testing UI (`gonk-testUI`)

This project includes a separate developer testing UI. For instructions on how to run it, please see the `README.md` file inside the `gonk-testUI/` directory.
