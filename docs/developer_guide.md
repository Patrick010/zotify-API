# Developer Guide

This guide provides instructions for setting up the Zotify API for local development and contributing to the project.

## Getting Started

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Googolplexed0/zotify.git
    cd zotify
    ```

2.  **Install dependencies:**
    ```bash
    pip install -e ./api
    ```

3.  **Run the API server:**
    ```bash
    uvicorn zotify_api.main:app --reload --host 0.0.0.0 --port 8080
    ```

## Admin API Key

Some endpoints are protected and require an admin API key. The application uses a dynamic, auto-generated admin API key system that is secure by default.

### Local Development

For local development, you have two options:

1.  **Auto-generated key:** On the first startup, a new admin API key will be generated and stored in the `.admin_api_key` file in the `api` directory. The key will also be printed to the console. You can use this key for subsequent requests.
2.  **`.env` file:** For a consistent key across restarts, you can create a `.env` file in the `api` directory and set the `ADMIN_API_KEY` environment variable:
    ```
    ADMIN_API_KEY="your-secret-key"
    ```

When making requests to protected endpoints, include the API key in the `X-API-Key` header:

```bash
curl -H "X-API-Key: your-secret-key" http://0.0.0.0:8080/api/some-protected-endpoint
```

## User Profiles and Preferences

The API provides endpoints for managing user profiles and preferences.

### Endpoints

*   `GET /user/profile`: Retrieve the user's profile.
*   `PATCH /user/profile`: Update the user's profile.
*   `GET /user/preferences`: Retrieve the user's preferences.
*   `PATCH /user/preferences`: Update the user's preferences.

### Data Storage

User data is stored in a JSON file in the `api/storage` directory. This is a temporary solution that will be replaced with a database in a future iteration.
