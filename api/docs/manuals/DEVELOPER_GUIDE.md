# Zotify API - Developer Guide

This guide provides developers with the necessary information to run, test, and contribute to the Zotify API locally.

---

## 1. Local Development Setup

### Purpose
To create a consistent and isolated local environment for developing and testing the Zotify API.

### Prerequisites
- Python 3.10+
- `pip` for package installation
- Git
- An accessible database (SQLite is sufficient for local development)

### Setup Steps

1.  **Clone the Repository**
    \`\`\`bash
    git clone https://github.com/Patrick010/zotify-API.git
    cd zotify-API
    \`\`\`

2.  **Install Dependencies**
    It is crucial to use a virtual environment.
    \`\`\`bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -e ./api
    \`\`\`

3.  **Set Up Local Environment**
    The application uses a `.env` file for configuration. Copy the example and fill in your details.
    \`\`\`bash
    # From the /api directory
    cp .env.example .env
    # Edit .env to set your local configuration.
    nano .env
    \`\`\`
    **Required `.env` variables for local development:**
    \`\`\`
    APP_ENV="development"
    ADMIN_API_KEY="dev_key"
    DATABASE_URI="sqlite:///storage/zotify.db"
    SPOTIFY_CLIENT_ID="your_spotify_client_id"
    SPOTIFY_CLIENT_SECRET="your_spotify_client_secret"
    SPOTIFY_REDIRECT_URI="http://127.0.0.1:8000/api/auth/spotify/callback"
    \`\`\`

4.  **Create Storage Directory & Database**
    The application will create the database file on first run, but the directory must exist.
    \`\`\`bash
    # From the /api directory
    mkdir -p storage
    \`\`\`

---

## 2. Running and Testing

### Purpose
To run the API server locally with hot-reloading for active development and to execute the full test suite.

### 2.1. Run the API Locally
#### Command
\`\`\`bash
# Run from the /api directory
uvicorn zotify_api.main:app --reload --host 127.0.0.1 --port 8000
\`\`\`
#### Expected Output
\`\`\`
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12347]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
\`\`\`
#### Usage Notes
- The interactive OpenAPI (Swagger) documentation is available at `http://127.0.0.1:8000/docs`. This is the best way to explore and test endpoints during development.

### 2.2. Run the Test Suite
#### Command
\`\`\`bash
# Run from the /api directory
APP_ENV=test python3 -m pytest
\`\`\`
#### Usage Notes
- `APP_ENV=test` is **required**. It configures the app to use an in-memory SQLite database and other test-specific settings, preventing interference with your development database.

---

## 3. Local API Interaction Examples

### Purpose
To provide practical `curl` examples for interacting with a locally running instance of the API.

### 3.1. Health Check
#### Command
\`\`\`bash
curl http://127.0.0.1:8000/api/health
\`\`\`
#### Expected Response
\`\`\`json
{
  "status": "ok"
}
\`\`\`

### 3.2. Add a Track to the Download Queue
#### Command
\`\`\`bash
curl -X POST http://127.0.0.1:8000/api/download \
  -H "X-API-Key: dev_key" \
  -H "Content-Type: application/json" \
  -d '{"track_ids": ["spotify:track:4cOdK2wGLETOMsV3oDPEhB"]}'
\`\`\`
#### Expected Response
A JSON array with the created job object(s).
\`\`\`json
[
  {
    "job_id": "some-uuid-string",
    "track_id": "spotify:track:4cOdK2wGLETOMsV3oDPEhB",
    "status": "pending",
    "progress": 0.0,
    "created_at": "...",
    "error_message": null
  }
]
\`\`\`

### 3.3. Check Download Queue Status
#### Command
\`\`\`bash
curl -X GET "http://127.0.0.1:8000/api/download/status" -H "X-API-Key: dev_key"
\`\`\`

### Troubleshooting
- **`ModuleNotFoundError: zotify_api`**: You are likely in the wrong directory. Ensure you run `uvicorn` and `pytest` from the `/api` directory.
- **`401 Unauthorized`**: Ensure you are passing the `X-API-Key` header and that its value matches the `ADMIN_API_KEY` in your `.env` file.
- **`500 Internal Server Error`**: Check the `uvicorn` server logs for a full traceback. This often points to a misconfiguration or a bug.

### References
- **API Documentation:** `http://127.0.0.1:8000/docs`
- **Operator Manual:** `OPERATOR_MANUAL.md`
- **Error Handling Guide:** `ERROR_HANDLING_GUIDE.md`
