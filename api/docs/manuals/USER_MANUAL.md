<!-- ID: API-113 -->
# Zotify API - User Manual

**Version:** 1.1
**Date:** 2025-08-18

## 1. Introduction

This manual explains how to consume the Zotify REST API to manage your music library. It is intended for end-users or client application developers. For a full, interactive list of all endpoints, please see the [Swagger UI documentation](./../../docs) available on your local server instance.

## 2. Authentication

All protected endpoints require a valid API key to be sent in the `X-API-Key` HTTP header.

`X-API-Key: your_secret_admin_key`

If the key is missing or incorrect, you will receive a `401 Unauthorized` error.

## 3. Core Workflow Example

### Step 1: Add a Track for Download

To submit one or more tracks to the download queue, make a `POST` request to the `/downloads` endpoint.

-   **Endpoint:** `POST /api/downloads`
-   **Request Body:** A JSON object containing a list of Spotify track IDs.

**Example Request:**
```bash
curl -X POST "http://localhost:8000/api/downloads" \
  -H "X-API-Key: your_secret_admin_key" \
  -H "Content-Type: application/json" \
  -d '{"track_ids": ["spotify:track:4cOdK2wGLETOMsV3oDPEhB"]}'
```

**Example Success Response (`200 OK`):**
The API will return a standard `{"data": ...}` response containing a list of the created download jobs.
```json
{
  "data": [
    {
      "job_id": "a1b2c3d4-...",
      "track_id": "spotify:track:4cOdK2wGLETOMsV3oDPEhB",
      "status": "pending",
      "progress": 0.0,
      "created_at": "2025-08-18T10:30:00Z",
      "error_message": null
    }
  ]
}
```

### Step 2: Check Download Queue Status

To retrieve the status of all current and past download jobs, make a `GET` request to the `/downloads` endpoint.

-   **Endpoint:** `GET /api/downloads`

**Example Request:**
```bash
curl -X GET "http://localhost:8000/api/downloads" \
  -H "X-API-Key: your_secret_admin_key"
```

**Example Success Response (`200 OK`):**
The response will be a paginated list of all download jobs.
```json
{
  "data": [
    {
      "job_id": "a1b2c3d4-...",
      "track_id": "spotify:track:4cOdK2wGLETOMsV3oDPEhB",
      "status": "pending",
      "progress": 0.0,
      "created_at": "2025-08-18T10:30:00Z",
      "error_message": null
    }
  ],
  "meta": {
    "total_items": 1,
    "total_pages": 1,
    "current_page": 1,
    "page_size": 50
  }
}
```

## 4. Error Handling

When an API request fails, you will receive a JSON response with a standardized error schema.

**Example Error Response (`401 Unauthorized`):**
```json
{
  "error": {
    "code": "E401_INVALID_CREDENTIALS",
    "message": "Authentication failed: Invalid or missing API key.",
    "timestamp": "2025-08-18T10:35:00Z",
    "request_id": "uuid-..."
  }
}
```
For a full list of error codes and their meanings, please consult the `ERROR_HANDLING_GUIDE.md`.

## 5. What You Can Do With the API (Phases 1–5 Complete)

The current version of the Zotify API provides a comprehensive set of features for user management, music library interaction, and system control. Here is a summary of the available capabilities:

### User Management & Authentication
*   **Register and Login:** Create a new account and authenticate to receive a JWT token via the `/auth/register` and `/auth/login` endpoints.
*   **Manage Profile:** Access and update your user profile information through the `/user/profile` endpoint.
*   **Manage Preferences:** View and update your application preferences, including the `notifications.enabled` toggle, at `/user/preferences`.
*   **Manage Liked Tracks:** Add, remove, and view your list of liked tracks at `/user/liked`.
*   **View Playback History:** Access your track playback history via the `/user/history` endpoint.

### Music Library Interaction
*   **Interact with Content:** Perform standard operations on albums, tracks, and playlists using their respective endpoints.
*   **Manage Downloads:** Submit tracks for download and monitor their progress through the `/downloads` endpoint.
*   **Receive Notifications:** View system notifications at the `/notifications` endpoint.

### System & Configuration
*   **Trigger System Actions:** Initiate system-level tasks like cache clearing via the `/system/clear-cache` endpoint.
*   **Monitor System Status:** Check on the status of downloads, sync processes, and system configurations through their respective endpoints.

### Gonk Testing Tools
*   **Use the Gonk CLI:** Perform all user actions (login, profile/preference management, liked tracks, history) from the command line. The CLI can be pointed at a real API instance using the `--api` flag.
*   **Use the GonkUI:** Access the same functionality through a convenient web interface, which includes a toggle to switch between an internal mock JWT and a real API JWT for flexible testing.
