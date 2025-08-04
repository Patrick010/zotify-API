# Zotify API Reference Manual

This manual documents the full capabilities of the Zotify API, designed for managing media libraries, metadata, playlists, downloads, and configuration. All endpoints are RESTful and served under the base path:

```
http://0.0.0.0:8080/api
```

---

## Authentication

No authentication is required for local testing. Production deployments should restrict access via reverse proxy or API gateway.

---

## Index

- [Configuration](#configuration)
- [Playlists](#playlist-management)
- [Tracks](#tracks)
- [Logging](#logging)
- [Caching](#caching)
- [Network](#network--proxy-settings)
- [Spotify Integration](#spotify-integration)
- [User](#user)
- [System](#system)
- [Fork-Specific Features](#fork-specific-features)

---

## Configuration

### `GET /config`

Returns the current application configuration.

**Request:**

```bash
curl http://0.0.0.0:8080/api/config
```

**Response:**

```json
{
  "library_path": "/music",
  "scan_on_startup": true,
  "cover_art_embed_enabled": true
}
```

**Errors:**

- `500 Internal Server Error`: If the configuration cannot be retrieved.

### `PATCH /config`

Updates specific fields in the application configuration.

**Request:**

```bash
curl -X PATCH http://0.0.0.0:8080/api/config \
  -H "Content-Type: application/json" \
  -d '{
    "scan_on_startup": false
  }'
```

**Body Parameters:**

| Name                      | Type    | Description                               |
| ------------------------- | ------- | ----------------------------------------- |
| `library_path`            | string  | (Optional) The path to the music library. |
| `scan_on_startup`         | boolean | (Optional) Whether to scan on startup.    |
| `cover_art_embed_enabled` | boolean | (Optional) Whether to embed cover art.    |

**Response:**

The updated configuration object.

**Errors:**

- `400 Bad Request`: If the request body is not valid JSON.

### `POST /config/reset`

Resets the application configuration to its default values.

**Request:**

```bash
curl -X POST http://0.0.0.0:8080/api/config/reset
```

**Response:**

The default configuration object.

---

## Playlist Management

### `GET /playlists`

Returns all saved playlists.

**Request:**

```bash
curl http://0.0.0.0:8080/api/playlists
```

**Response:**

```json
[
  {
    "id": "abc123",
    "name": "My Playlist",
    "tracks": ["track1", "track2"]
  }
]
```

### `POST /playlists`

Creates a new playlist.

**Request:**

```bash
curl -X POST http://0.0.0.0:8080/api/playlists \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My New Playlist"
  }'
```

**Body Parameters:**

| Name   | Type   | Description                |
| ------ | ------ | -------------------------- |
| `name` | string | The name of the playlist. |

**Response:**

The newly created playlist object.

### `DELETE /playlists/{playlist_id}`

Deletes a playlist by its ID.

**Request:**

```bash
curl -X DELETE http://0.0.0.0:8080/api/playlists/abc123
```

**Path Parameters:**

| Name          | Type   | Description                  |
| ------------- | ------ | ---------------------------- |
| `playlist_id` | string | The ID of the playlist to delete. |

**Response:**

- `204 No Content`

**Errors:**

- `404 Not Found`: If the playlist with the given ID does not exist.

### `POST /playlists/{playlist_id}/tracks`

Adds one or more tracks to a playlist.

**Request:**

```bash
curl -X POST http://0.0.0.0:8080/api/playlists/abc123/tracks \
  -H "Content-Type: application/json" \
  -d '{
    "track_ids": ["track3", "track4"]
  }'
```

**Path Parameters:**

| Name          | Type   | Description                           |
| ------------- | ------ | ------------------------------------- |
| `playlist_id` | string | The ID of the playlist to add tracks to. |

**Body Parameters:**

| Name        | Type     | Description                     |
| ----------- | -------- | ------------------------------- |
| `track_ids` | string[] | A list of track IDs to add. |

**Response:**

The updated playlist object.

**Errors:**

- `404 Not Found`: If the playlist with the given ID does not exist.

---

## Tracks

### `GET /tracks/{track_id}/metadata`

Returns metadata for a specific track.

**Request:**

```bash
curl http://0.0.0.0:8080/api/tracks/abc123/metadata
```

**Path Parameters:**

| Name       | Type   | Description                |
| ---------- | ------ | -------------------------- |
| `track_id` | string | The ID of the track. |

**Response:**

```json
{
  "id": "abc123",
  "title": "Track Title",
  "artist": "Artist",
  "album": "Album",
  "genre": "Rock",
  "year": 2020
}
```

### `PATCH /tracks/{track_id}/metadata`

Updates metadata fields for a track.

**Request:**

```bash
curl -X PATCH http://0.0.0.0:8080/api/tracks/abc123/metadata \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Title"
  }'
```

**Path Parameters:**

| Name       | Type   | Description                |
| ---------- | ------ | -------------------------- |
| `track_id` | string | The ID of the track. |

**Body Parameters:**

| Name     | Type   | Description                 |
| -------- | ------ | --------------------------- |
| `title`  | string | (Optional) The new title.   |
| `artist` | string | (Optional) The new artist.  |
| `album`  | string | (Optional) The new album.   |
| `genre`  | string | (Optional) The new genre.   |
| `year`   | integer| (Optional) The new year.    |

**Response:**

The updated track metadata object.

### `POST /tracks/{track_id}/metadata/refresh`

Triggers a refresh of the track's metadata from its source.

**Request:**

```bash
curl -X POST http://0.0.0.0:8080/api/tracks/abc123/metadata/refresh
```

**Path Parameters:**

| Name       | Type   | Description                |
| ---------- | ------ | -------------------------- |
| `track_id` | string | The ID of the track. |

**Response:**

The updated track metadata object.

### `POST /tracks/{track_id}/cover`

Uploads a cover image for a track.

**Request:**

```bash
curl -X POST http://0.0.0.0:8080/api/tracks/abc123/cover \
  -F "cover_image=@cover.jpg"
```

**Path Parameters:**

| Name       | Type   | Description                |
| ---------- | ------ | -------------------------- |
| `track_id` | string | The ID of the track. |

**Form Data:**

| Name          | Type | Description              |
| ------------- | ---- | ------------------------ |
| `cover_image` | file | The cover image to upload. |

**Response:**

```json
{
  "id": "abc123",
  "cover": "Embedded image: cover.jpg"
}
```

---

## Logging

### `GET /logging`

Returns the current logging configuration.

**Request:**

```bash
curl http://0.0.0.0:8080/api/logging
```

**Response:**

```json
{
  "level": "INFO",
  "log_to_file": false,
  "log_file": null
}
```

### `PATCH /logging`

Updates the logging configuration.

**Request:**

```bash
curl -X PATCH http://0.0.0.0:8080/api/logging \
  -H "Content-Type: application/json" \
  -d '{
    "level": "DEBUG"
  }'
```

**Body Parameters:**

| Name          | Type    | Description                                                                 |
| ------------- | ------- | --------------------------------------------------------------------------- |
| `level`       | string  | (Optional) The new log level. Must be one of: `CRITICAL`, `ERROR`, `WARNING`, `INFO`, `DEBUG`. |
| `log_to_file` | boolean | (Optional) Whether to log to a file.                                        |
| `log_file`    | string  | (Optional) The path to the log file.                                        |

**Response:**

The updated logging configuration object.

**Errors:**

- `400 Bad Request`: If the log level is invalid.

---

## Caching

### `GET /cache`

Returns statistics about the cache.

**Request:**

```bash
curl http://0.0.0.0:8080/api/cache
```

**Response:**

```json
{
  "total_items": 302,
  "by_type": {
    "search": 80,
    "metadata": 222
  }
}
```

### `DELETE /cache`

Clears the cache.

**Request:**

To clear the entire cache:

```bash
curl -X DELETE http://0.0.0.0:8080/api/cache \
  -H "Content-Type: application/json" \
  -d '{}'
```

To clear a specific type of cache:

```bash
curl -X DELETE http://0.0.0.0:8080/api/cache \
  -H "Content-Type: application/json" \
  -d '{
    "type": "metadata"
  }'
```

**Body Parameters:**

| Name   | Type   | Description                                            |
| ------ | ------ | ------------------------------------------------------ |
| `type` | string | (Optional) The type of cache to clear (e.g., "search", "metadata"). If omitted, the entire cache is cleared. |

**Response:**

```json
{
  "status": "cleared",
  "by_type": {
    "search": 0,
    "metadata": 0
  }
}
```

---

## Network / Proxy Settings

### `GET /network`

Returns the current network proxy configuration.

**Request:**

```bash
curl http://0.0.0.0:8080/api/network
```

**Response:**

```json
{
  "proxy_enabled": false,
  "http_proxy": null,
  "https_proxy": null
}
```

### `PATCH /network`

Updates the network proxy configuration.

**Request:**

```bash
curl -X PATCH http://0.0.0.0:8080/api/network \
  -H "Content-Type: application/json" \
  -d '{
    "proxy_enabled": true,
    "http_proxy": "http://proxy.local:3128"
  }'
```

**Body Parameters:**

| Name            | Type    | Description                          |
| --------------- | ------- | ------------------------------------ |
| `proxy_enabled` | boolean | (Optional) Whether the proxy is enabled. |
| `http_proxy`    | string  | (Optional) The HTTP proxy URL.       |
| `https_proxy`   | string  | (Optional) The HTTPS proxy URL.      |

**Response:**

The updated network proxy configuration object.

---

## Spotify Integration

### `GET /spotify/login`

Returns a URL to authorize the application with Spotify.

**Request:**

```bash
curl http://0.0.0.0:8080/api/spotify/login
```

**Response:**

```json
{
  "auth_url": "https://accounts.spotify.com/authorize?client_id=...&response_type=code&redirect_uri=...&scope=..."
}
```

### `GET /spotify/callback`

Callback endpoint for Spotify OAuth2 flow. This endpoint is called by Spotify after the user authorizes the application.

**Query Parameters:**

| Name   | Type   | Description                               |
| ------ | ------ | ----------------------------------------- |
| `code` | string | The authorization code from Spotify. |

**Response:**

```json
{
  "status": "Spotify tokens stored"
}
```

**Errors:**

- `400 Bad Request`: If the `code` query parameter is missing.

### `GET /spotify/token_status`

Returns the status of the Spotify API token.

**Request:**

```bash
curl http://0.0.0.0:8080/api/spotify/token_status
```

**Response:**

```json
{
  "access_token_valid": true,
  "expires_in_seconds": 3600
}
```

### `POST /spotify/sync_playlists`

Triggers a synchronization of playlists with Spotify.

**Request:**

```bash
curl -X POST http://0.0.0.0:8080/api/spotify/sync_playlists
```

**Response:**

```json
{
  "status": "Playlists synced (stub)"
}
```

### `GET /spotify/metadata/{track_id}`

Fetches metadata for a track from Spotify.

**Request:**

```bash
curl http://0.0.0.0:8080/api/spotify/metadata/3n3Ppam7vgaVa1iaRUc9Lp
```

**Path Parameters:**

| Name       | Type   | Description                |
| ---------- | ------ | -------------------------- |
| `track_id` | string | The ID of the track. |

**Response:**

The raw JSON response from the Spotify API.

**Errors:**

- `401 Unauthorized`: If the Spotify access token is invalid or expired.
- `404 Not Found`: If the track with the given ID does not exist on Spotify.

### `GET /spotify/playlists`

List user playlists.

**Request:**

```bash
curl http://0.0.0.0:8080/api/spotify/playlists
```

**Response:**

`501 Not Implemented`

### `GET /spotify/playlists/{playlist_id}`

Get playlist metadata.

**Request:**

```bash
curl http://0.0.0.0:8080/api/spotify/playlists/abc123
```

**Response:**

`501 Not Implemented`

### `DELETE /spotify/playlists/{playlist_id}`

Delete local copy.

**Request:**

```bash
curl -X DELETE http://0.0.0.0:8080/api/spotify/playlists/abc123
```

**Response:**

`501 Not Implemented`

### `GET /spotify/playlists/{playlist_id}/tracks`

List tracks in playlist.

**Request:**

```bash
curl http://0.0.0.0:8080/api/spotify/playlists/abc123/tracks
```

**Response:**

`501 Not Implemented`

### `POST /spotify/playlists/{playlist_id}/sync`

Sync specific playlist.

**Request:**

```bash
curl -X POST http://0.0.0.0:8080/api/spotify/playlists/abc123/sync
```

**Response:**

`501 Not Implemented`

### `PUT /spotify/playlists/{playlist_id}/metadata`

Update local playlist metadata.

**Request:**

```bash
curl -X PUT http://0.0.0.0:8080/api/spotify/playlists/abc123/metadata
```

**Response:**

`501 Not Implemented`

---

## User

### `GET /user/profile`

Get user profile.

**Request:**

```bash
curl http://0.0.0.0:8080/api/user/profile
```

**Response:**

`501 Not Implemented`

### `GET /user/liked`

List liked songs.

**Request:**

```bash
curl http://0.0.0.0:8080/api/user/liked
```

**Response:**

`501 Not Implemented`

### `POST /user/sync_liked`

Download liked songs.

**Request:**

```bash
curl -X POST http://0.0.0.0:8080/api/user/sync_liked
```

**Response:**

`501 Not Implemented`

### `GET /user/history`

List download history.

**Request:**

```bash
curl http://0.0.0.0:8080/api/user/history
```

**Response:**

`501 Not Implemented`

### `DELETE /user/history`

Clear history.

**Request:**

```bash
curl -X DELETE http://0.0.0.0:8080/api/user/history
```

**Response:**

`501 Not Implemented`

---

## System

### `GET /system/status`

Get system health.

**Request:**

```bash
curl http://0.0.0.0:8080/api/system/status
```

**Response:**

`501 Not Implemented`

### `GET /system/storage`

Get disk/storage usage.

**Request:**

```bash
curl http://0.0.0.0:8080/api/system/storage
```

**Response:**

`501 Not Implemented`

### `GET /system/logs`

Fetch logs.

**Request:**

```bash
curl http://0.0.0.0:8080/api/system/logs
```

**Response:**

`501 Not Implemented`

### `POST /system/reload`

Reload config.

**Request:**

```bash
curl -X POST http://0.0.0.0:8080/api/system/reload
```

**Response:**

`501 Not Implemented`

### `POST /system/reset`

Reset state.

**Request:**

```bash
curl -X POST http://0.0.0.0:8080/api/system/reset
```

**Response:**

`501 Not Implemented`

---

## Fork-Specific Features

### `POST /playlists/sync`

Initiates a synchronization of a playlist with a remote source.

**Request:**

```bash
curl -X POST http://0.0.0.0:8080/api/playlist/sync \
  -H "Content-Type: application/json" \
  -d '{
    "playlist_id": "abc123"
  }'
```

**Body Parameters:**

| Name          | Type   | Description                            |
| ------------- | ------ | -------------------------------------- |
| `playlist_id` | string | The ID of the playlist to synchronize. |

**Response:**

```json
{
  "status": "ok",
  "synced_tracks": 18,
  "conflicts": ["track_4", "track_9"]
}
```

### `GET /downloads/status`

Returns the status of the download queue.

**Request:**

```bash
curl http://0.0.0.0:8080/api/downloads/status
```

**Response:**

```json
{
  "in_progress": [],
  "failed": {
    "track_7": "Network error",
    "track_10": "404 not found"
  },
  "completed": ["track_3", "track_5"]
}
```

### `POST /downloads/retry`

Retries failed downloads.

**Request:**

```bash
curl -X POST http://0.0.0.0:8080/api/downloads/retry \
  -H "Content-Type: application/json" \
  -d '{
    "track_ids": ["track_7", "track_10"]
  }'
```

**Body Parameters:**

| Name        | Type     | Description                          |
| ----------- | -------- | ------------------------------------ |
| `track_ids` | string[] | A list of track IDs to retry. |

**Response:**

```json
{
  "retried": ["track_7", "track_10"],
  "queued": true
}
```

### `GET /metadata/{track_id}`

Returns extended metadata for a specific track.

**Request:**

```bash
curl http://0.0.0.0:8080/api/metadata/abc123
```

**Path Parameters:**

| Name       | Type   | Description                |
| ---------- | ------ | -------------------------- |
| `track_id` | string | The ID of the track. |

**Response:**

```json
{
  "title": "Track Title",
  "mood": "Chill",
  "rating": 4,
  "source": "Manual Import"
}
```

### `PATCH /metadata/{track_id}`

Updates extended metadata for a track.

**Request:**

```bash
curl -X PATCH http://0.0.0.0:8080/api/metadata/abc123 \
  -H "Content-Type: application/json" \
  -d '{
    "mood": "Energetic",
    "rating": 5
  }'
```

**Path Parameters:**

| Name       | Type   | Description                |
| ---------- | ------ | -------------------------- |
| `track_id` | string | The ID of the track. |

**Body Parameters:**

| Name     | Type    | Description                   |
| -------- | ------- | ----------------------------- |
| `mood`   | string  | (Optional) The new mood.      |
| `rating` | integer | (Optional) The new rating.    |
| `source` | string  | (Optional) The new source.    |

**Response:**

```json
{
  "status": "updated",
  "track_id": "abc123"
}
```

---

## Final Notes

- All endpoints are unauthenticated for local use.
- Use `jq` to pretty-print JSON responses in CLI.
- Future integrations (Spotify, tagging engines) will build on these base endpoints.

---

## Manual Test Runbook

### Setup

1.  Register your app with Spotify Developer Console.
2.  Set redirect URI to `http://localhost:8080/api/spotify/callback`.
3.  Update `CLIENT_ID` and `CLIENT_SECRET` in `api/src/zotify_api/routes/spotify.py`.
4.  Start API server.

### Steps

1.  Request login URL: `GET /api/spotify/login`
2.  Open URL in browser, authorize, and get the `code` query param.
3.  Call `/api/spotify/callback?code=YOUR_CODE` with that code.
4.  Check token status with `/api/spotify/token_status`.
5.  Trigger playlist sync with `/api/spotify/sync_playlists`.
6.  Fetch metadata for sample track IDs.
7.  Simulate token expiry and verify automatic refresh.
8.  Test with proxy settings enabled.
9.  Inject errors by revoking tokens on Spotify and verify error handling.
10. Repeat tests on slow networks or disconnects.
