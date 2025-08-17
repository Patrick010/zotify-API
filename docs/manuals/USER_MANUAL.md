# Zotify API User Manual

Welcome to the Zotify API! This guide will help you understand what the API does and how to use its core features.

## 1. Overview

The Zotify API is a backend service designed to manage and process a queue of media download jobs. You can add tracks to a download queue, monitor the status of jobs, and interact with various other system components through a simple RESTful interface.

## 2. Authentication

All requests to protected API endpoints must include an API key in the request headers.

*   **Header Name:** `X-API-Key`
*   **Header Value:** Your assigned administrator API key.

Requests without a valid API key will be rejected with a `401 Unauthorized` error.

**Example using `curl`:**
```bash
curl -X GET "http://localhost:8000/api/download/status" -H "X-API-Key: your_secret_key"
```

## 3. Core Features

Here are examples of how to use the most common features of the API.

### 3.1. Adding Tracks to the Download Queue

To add one or more tracks to be downloaded, you send a `POST` request to the `/api/download` endpoint with a list of track IDs.

**Endpoint:** `POST /api/download`

**Request Body:**
```json
{
  "track_ids": ["spotify:track:4cOdK2wGLETOMsV3oDPEhB", "spotify:track:11dFghVXANMlKmJXsNCbNl"]
}
```

**Example `curl` command:**
```bash
curl -X POST "http://localhost:8000/api/download" \
-H "X-API-Key: your_secret_key" \
-H "Content-Type: application/json" \
-d '{"track_ids": ["spotify:track:4cOdK2wGLETOMsV3oDPEhB"]}'
```

**Successful Response:**
The API will respond with a JSON array containing the newly created job objects.

```json
[
  {
    "job_id": "e8a3b5c7-...",
    "track_id": "spotify:track:4cOdK2wGLETOMsV3oDPEhB",
    "status": "pending",
    "progress": 0.0,
    "created_at": "2025-01-01T12:00:00Z",
    "error_message": null
  }
]
```

### 3.2. Checking the Queue Status

You can get a summary of the entire download queue by sending a `GET` request to the `/api/download/status` endpoint.

**Endpoint:** `GET /api/download/status`

**Example `curl` command:**
```bash
curl -X GET "http://localhost:8000/api/download/status" -H "X-API-Key: your_secret_key"
```

**Successful Response:**
The API will respond with a JSON object summarizing the state of all jobs.

```json
{
  "total_jobs": 1,
  "pending": 1,
  "completed": 0,
  "failed": 0,
  "jobs": [
    {
      "job_id": "e8a3b5c7-...",
      "track_id": "spotify:track:4cOdK2wGLETOMsV3oDPEhB",
      "status": "pending",
      "progress": 0.0,
      "created_at": "2025-01-01T12:00:00Z",
      "error_message": null
    }
  ]
}
```

This covers the basic usage of the Zotify API. For a full list of available endpoints, please refer to the OpenAPI or Swagger documentation provided by the API at `/docs`.
