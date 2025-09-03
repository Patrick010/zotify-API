# Zotify API Reference Manual

This manual documents the full capabilities of the Zotify API, designed for managing media libraries, metadata, playlists, downloads, and configuration. All endpoints are RESTful and served under the base path:

```
http://0.0.0.0:8000
```
*(Note: The `/api` prefix is configurable and may not be present in all environments.)*

---

## Architectural Overview

It is critical to understand that the Zotify API is **not** a reimplementation of the Spotify Web API. Instead, it is a developer-centric framework built around the original Zotify CLI client, which itself uses Librespot for authentication and media retrieval.

The primary purpose of this API is to expose powerful, automation-oriented functionality that Spotify’s own Web API either does not offer or makes difficult to script. This includes:

*   **Direct Media Downloads**: Programmatically download tracks, albums, or playlists.
*   **Offline Caching**: Manage a local cache of media content.
*   **Advanced Automation**: Hook into a robust queueing and download management system.
*   **Raw Librespot Access**: Provide a safe, scriptable, and scalable interface to Librespot's underlying capabilities.

Think of the Zotify API as a developer platform for building systems on top of Spotify's content ecosystem, with a strong focus on media acquisition and local library management.

---

## Authentication

The Zotify API uses the **OAuth 2.0 Authorization Code Flow with PKCE** to securely connect to a user's Spotify account. This process is designed for both interactive and headless environments and is orchestrated by the API and the `snitch` helper application.

The flow is as follows:
1.  **Initiate Login**: A client sends a `GET` request to `/api/spotify/login`.
2.  **User Authorization**: The API returns a Spotify authorization URL. The user must open this URL in a browser and grant permission to the application.
3.  **Callback to Snitch**: After the user grants permission, Spotify redirects the browser to `http://127.0.0.1:4381/login`, where the `snitch` application is listening. Snitch captures the authorization `code` and `state` token from the request.
4.  **Secure Handoff**: Snitch makes a `POST` request to the Zotify API's `/api/auth/spotify/callback` endpoint, sending the `code` and `state` in a secure JSON body.
5.  **Token Exchange**: The main API validates the `state` token, then securely exchanges the `code` for a permanent refresh token and a short-lived access token from Spotify using the PKCE verifier. The tokens are then persisted.

This process ensures that credentials and secrets are never exposed in the browser.

---

## Endpoints

### Authentication

#### `GET /spotify/login`

Initiates the authentication flow. This endpoint generates all the necessary PKCE parameters and returns a Spotify URL that the user must open in their browser to grant permissions.

**Response (Success 200 OK):**
```json
{
  "auth_url": "https://accounts.spotify.com/authorize?client_id=..."
}
```

#### `POST /auth/spotify/callback`

This endpoint is not intended for direct use by users. It is the secure callback target for the `snitch` application. Snitch forwards the `code` and `state` here to be exchanged for final tokens.

**Request Body:**
```json
{
  "code": "...",
  "state": "..."
}
```

**Response (Success 200 OK):**
```json
{
  "status": "success"
}
```

---

## Index

- Library
- Playlist Management
- Downloads
- Metadata & Cover Art
- Logging and Configuration
- Caching
- Network / Proxy Settings
- Spotify Integration
- User
- System
- Fork-Specific Features

---

## Library

### `GET /library`

List available tracks in the library.

**Example Response:**

```json
[
  {
    "id": "abc123",
    "title": "My Song",
    "artist": "Example Artist",
    "album": "Album X"
  }
]
```

---

## Playlist Management

### `GET /playlists`

Returns all saved playlists.

### `POST /playlists`

Create a new playlist.

**Body:**

```json
{
  "name": "My Playlist",
  "description": "My favorite songs"
}
```

---

## Downloads

### `GET /downloads/status`

Returns current download queue.

### `POST /downloads/retry`

Retry a download.

**Body:**

```json
{ "track_ids": ["abc123"] }
```

---

## Tracks

### `GET /tracks`

Returns a list of tracks.

### `GET /tracks/{track_id}`

Returns a specific track by its ID.

### `POST /tracks`

Creates a new track.

**Body:**

```json
{
  "name": "New Track",
  "artist": "New Artist"
}
```

### `PATCH /tracks/{track_id}`

Updates a track by its ID.

**Body:**

```json
{
  "name": "Updated Track"
}
```

### `DELETE /tracks/{track_id}`

Deletes a track by its ID.

### `POST /tracks/{track_id}/cover`

Uploads a cover image for a track.

---

## Logging

### `GET /logging`

Returns logging config.

### `PATCH /logging`

Update log level.

**Body:**

```json
{ "level": "DEBUG" }
```

Accepted levels: CRITICAL, ERROR, WARNING, INFO, DEBUG

---

## Configuration

### `GET /config`

Returns current system config.

### `PATCH /config`

Update runtime configuration.

### `POST /config/reset`

Reset configuration to default values.

---

## Caching

### `GET /cache`

View current cache usage.

**Example Response:**

```json
{
  "total_items": 300,
  "by_type": {
    "search": 100,
    "metadata": 200
  }
}
```

### `DELETE /cache`

Clear all or specific caches.

**Body:**

```json
{ "type": "metadata" }
```

---

## Network / Proxy Settings

### `GET /network`

Returns current proxy settings.

### `PATCH /network`

Update proxy settings.

**Body:**

```json
{
  "proxy_enabled": true,
  "http_proxy": "http://proxy.local:3128",
  "https_proxy": "https://proxy.secure:443"
}
```

---

## Spotify Integration

### `GET /spotify/token_status`

Returns the status of the Spotify API token.

### `POST /spotify/sync_playlists`

Triggers a synchronization of playlists with Spotify.

### `GET /spotify/metadata/{track_id}`

Fetches metadata for a track from Spotify.

### `GET /spotify/playlists`

List user playlists.

### `GET /spotify/playlists/{playlist_id}`

Get playlist metadata.

### `DELETE /spotify/playlists/{playlist_id}`

Delete local copy.

### `GET /spotify/playlists/{playlist_id}/tracks`

List tracks in playlist.

### `POST /spotify/playlists/{playlist_id}/sync`

Sync specific playlist.

### `PUT /spotify/playlists/{playlist_id}/metadata`

Update local playlist metadata.

---

## User

### `GET /user/profile`

Get user profile.

### `GET /user/liked`

List liked songs.

### `POST /user/sync_liked`

Download liked songs.

### `GET /user/history`

List download history.

### `DELETE /user/history`

Clear history.

---

## System

### `GET /system/status`

Get system health.

### `GET /system/storage`

Get disk/storage usage.

### `GET /system/logs`

Fetch logs.

### `POST /system/reload`

Reload config.

### `POST /system/reset`

Reset state.

---

## Fork-Specific Features

### `POST /sync/playlist/sync`

Trigger advanced playlist sync.

**Body:**

```json
{ "playlist_id": "abc123" }
```

---

## Example Use Cases

### Create and populate a playlist

```bash
curl -X POST http://0.0.0.0:8080/api/playlists -H "Content-Type: application/json" -d '{"name": "My Chill Playlist", "description": "My favorite songs"}'
```

### Download and monitor a track

```bash
curl http://0.0.0.0:8080/api/downloads/status
curl -X POST http://0.0.0.0:8080/api/downloads/retry -H "Content-Type: application/json" -d '{"track_ids": ["track_7"]}'
```

### Update track metadata

```bash
curl -X PATCH http://0.0.0.0:8080/api/tracks/abc123 -H "Content-Type: application/json" -d '{"name": "Updated Title"}'
```

### Clear metadata cache

```bash
curl -X DELETE http://0.0.0.0:8080/api/cache -H "Content-Type": "application/json" -d '{"type": "metadata"}'
```

### Update proxy settings

```bash
curl -X PATCH http://0.0.0.0:8080/api/network -H "Content-Type": "application/json" -d '{
  "proxy_enabled": true,
  "http_proxy": "http://localhost:3128"
}'
```

---

## Final Notes

- All endpoints are unauthenticated for local use.
- Use `jq` to pretty-print JSON responses in CLI.
- Future integrations (Spotify, tagging engines) will build on these base endpoints.

---

## Manual Test Runbook

This runbook describes how to manually test the full authentication flow.

### Setup

1.  **Start the Zotify API Server:**
    ```bash
    uvicorn zotify_api.main:app --host 0.0.0.0 --port 8000
    ```
2.  **Start the Snitch Service:**
    -   Make sure the Snitch binary is built (`cd snitch && go build .`).
    -   Set the callback URL environment variable:
        ```bash
        export SNITCH_API_CALLBACK_URL="http://localhost:8000/api/auth/spotify/callback"
        ```
    -   Run the snitch executable:
        ```bash
        ./snitch
        ```

### Steps

1.  **Request login URL:** Send a `GET` request to `http://localhost:8000/api/spotify/login`.
2.  **Authorize in Browser:** Open the `auth_url` from the response in your web browser. Log in to Spotify and grant the requested permissions.
3.  **Automatic Callback:** The browser will be redirected to Snitch, which will then automatically POST the authorization code to the Zotify API.
4.  **Check Token Status:** Send a `GET` request to `http://localhost:8000/api/spotify/token_status`. The `access_token_valid` field should be `true`.
5.  **Test an Authenticated Endpoint:** For example, fetch metadata for a track with `GET /api/spotify/metadata/{track_id}`.
