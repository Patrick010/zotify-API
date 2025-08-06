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

Some endpoints are protected and require an admin API key. To access these endpoints, you need to set the `ADMIN_API_KEY` environment variable.

You can do this by creating a `.env` file in the `api` directory with the following content:

```
ADMIN_API_KEY="your-secret-key"
```

Alternatively, you can set the environment variable directly in your shell:

```bash
export ADMIN_API_KEY="your-secret-key"
```

When making requests to protected endpoints, include the API key in the `X-API-Key` header:

```bash
curl -H "X-API-Key: your-secret-key" http://0.0.0.0:8080/api/some-protected-endpoint
```

In production (`app_env="production"`), the application will refuse to start unless an admin API key is provided. This behavior can be disabled by setting `REQUIRE_ADMIN_API_KEY_IN_PROD=false`.
