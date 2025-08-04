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

- Library
- Playlist Management
- Downloads
- Metadata & Cover Art
- Logging and Configuration
- Caching
- Network / Proxy Settings
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
{ "name": "My Playlist" }
```

### `DELETE /playlists/{id}`

Delete the playlist with given ID.

### `POST /playlists/{id}/tracks`

Append tracks to playlist.

**Body:**

```json
{ "track_ids": ["abc123", "xyz456"] }
```

---

## Downloads

### `GET /downloads`

Returns current download queue.

### `POST /downloads`

Start a download.

**Body:**

```json
{ "track_id": "abc123" }
```

### `DELETE /downloads/{id}`

Cancel a download.

---

## Metadata and Cover Art

### `GET /metadata/{track_id}`

Fetch metadata for track.

### `PATCH /metadata/{track_id}`

Update metadata for a track.

**Body:**

```json
{
  "title": "New Title",
  "artist": "New Artist",
  "tags": ["chill", "favorite"]
}
```

### `POST /metadata/{track_id}/cover`

Upload cover art.

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

## Fork-Specific Features

### `POST /playlists/sync`

Trigger advanced playlist sync.

**Body:**

```json
{ "source": "external", "mode": "merge" }
```

### `GET /downloads/status`

Get extended download status.

### `POST /downloads/retry`

Retry failed downloads.

**Body:**

```json
{ "download_id": "xyz789" }
```

### `GET /metadata/tags`

Return all known tags for user-defined classification.

---

## Example Use Cases

### Create and populate a playlist

```bash
curl -X POST http://0.0.0.0:8080/api/playlists -H "Content-Type: application/json" -d '{"name": "My Chill Playlist"}'
curl -X POST http://0.0.0.0:8080/api/playlists/1/tracks -H "Content-Type: application/json" -d '{"track_ids": ["abc123"]}'
```

### Download and monitor a track

```bash
curl -X POST http://0.0.0.0:8080/api/downloads -H "Content-Type: application/json" -d '{"track_id": "abc123"}'
curl http://0.0.0.0:8080/api/downloads
```

### Update metadata

```bash
curl -X PATCH http://0.0.0.0:8080/api/metadata/abc123 -H "Content-Type: application/json" -d '{"title": "Updated Title"}'
```

### Clear metadata cache

```bash
curl -X DELETE http://0.0.0.0:8080/api/cache -H "Content-Type: application/json" -d '{"type": "metadata"}'
```

### Update proxy settings

```bash
curl -X PATCH http://0.0.0.0:8080/api/network -H "Content-Type: application/json" -d '{
  "proxy_enabled": true,
  "http_proxy": "http://localhost:3128"
}'
```

---

## Final Notes

- All endpoints are unauthenticated for local use.
- Use `jq` to pretty-print JSON responses in CLI.
- Future integrations (Spotify, tagging engines) will build on these base endpoints.
