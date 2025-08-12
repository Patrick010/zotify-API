# Zotify API

This repository contains the source code for the Zotify API, a RESTful service for interacting with the Zotify music and podcast downloader.

## Running the API

1.  **Install dependencies:**
    ```bash
    pip install -r api/requirements.txt  # Assuming a requirements.txt is generated from pyproject.toml
    ```
    *Note: For now, install dependencies directly from `api/pyproject.toml`.*

2.  **Set up the environment:**
    Create a `.env` file in the `api/` directory with the necessary settings (e.g., `DATABASE_URI`).

3.  **Run the API server:**
    ```bash
    uvicorn zotify_api.main:app --host 0.0.0.0 --port 8000
    ```

## Developer Testing UI (`gonk-testUI`)

This project includes a separate developer testing UI to help with API development and testing.

**1. Install dependencies:**
```bash
pip install -r gonk-testUI/requirements.txt # Assuming a requirements.txt is generated
```
*Note: For now, install dependencies directly from `gonk-testUI/pyproject.toml`.*

**2. Set the `DATABASE_URI` environment variable:**
The `gonk-testUI` needs access to the same database as the main API to use the `sqlite-web` integration.
```bash
export DATABASE_URI="sqlite:///../api/storage/zotify.db" # Example for Linux/macOS
set DATABASE_URI=sqlite:///../api/storage/zotify.db     # Example for Windows
```

**3. Run the `gonk-testUI` server:**
```bash
python gonk-testUI/app.py
```
The UI will be available at `http://localhost:8082`.
