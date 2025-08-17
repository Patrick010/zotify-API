# Project API Endpoints Reference

## Overview

This file lists all public API endpoints for the Zotify API project, generated from the OpenAPI schema. It provides a high-level reference for developers, operators, and auditors.

### Notes:

-   Authentication requirements are noted for each endpoint.
-   Always update this file when adding, modifying, or deprecating endpoints.

---

## Zotify API Endpoints

### Default Endpoints
| Method | Path | Summary | Auth Required |
|---|---|---|---|
| GET,HEAD | `/openapi.json` | Get the OpenAPI 3.0 schema for the API. | No |
| GET,HEAD | `/docs` | Interactive API documentation (Swagger UI). | No |
| GET,HEAD | `/docs/oauth2-redirect` | Handles OAuth2 redirects for the Swagger UI. | No |
| GET,HEAD | `/redoc` | Alternative API documentation (ReDoc). | No |
| GET | `/ping` | A simple health check endpoint. | No |
| GET | `/version` | Get application version information. | No |

### `health`
| Method | Path | Summary | Auth Required |
|---|---|---|---|
| GET | `/health` | Detailed health check endpoint. | No |

### `system`
| Method | Path | Summary | Auth Required |
|---|---|---|---|
| GET | `/api/system/status` | Get system health and status. | Yes |
| GET | `/api/system/storage` | Get disk and storage usage. | Yes |
| GET | `/api/system/logs` | Fetch system logs. | Yes |
| POST | `/api/system/reload` | Trigger a reload of the application configuration. | Yes |
| POST | `/api/system/reset` | Reset the system state. | Yes |
| GET | `/api/system/uptime` | Get the API server's uptime. | Yes |
| GET | `/api/system/env` | Get environment information. | Yes |
| GET | `/api/schema` | Get a specific component of the OpenAPI schema. | Yes |

### `auth`
| Method | Path | Summary | Auth Required |
|---|---|---|---|
| POST | `/api/auth/spotify/callback` | Handles the secure callback from the Snitch service. | No |
| GET | `/api/auth/status` | Get the current authentication status with Spotify. | Yes |
| POST | `/api/auth/logout` | Revoke the current Spotify token. | Yes |
| GET | `/api/auth/refresh` | Force a refresh of the Spotify access token. | Yes |

### `metadata`
| Method | Path | Summary | Auth Required |
|---|---|---|---|
| GET | `/api/metadata/{track_id}` | Get extended metadata for a track. | Yes |
| PATCH | `/api/metadata/{track_id}` | Update extended metadata for a track. | Yes |

### `cache`
| Method | Path | Summary | Auth Required |
|---|---|---|---|
| GET | `/api/cache` | Get statistics about the application cache. | Yes |
| DELETE | `/api/cache` | Clear all or part of the application cache. | Yes |

### `user`
| Method | Path | Summary | Auth Required |
|---|---|---|---|
| GET | `/api/user/profile` | Retrieve the user's profile information. | Yes |
| PATCH | `/api/user/profile` | Modify existing user profile data. | Yes |
| GET | `/api/user/preferences` | Retrieve the user's preferences. | Yes |
| PATCH | `/api/user/preferences` | Modify the user's preferences. | Yes |
| GET | `/api/user/liked` | Retrieve a list of the user's liked songs. | Yes |
| POST | `/api/user/sync_liked` | Trigger a synchronization of the user's liked songs. | Yes |
| GET | `/api/user/history` | Retrieve the user's download history. | Yes |
| DELETE | `/api/user/history` | Clear the user's download history. | Yes |

### `playlists`
| Method | Path | Summary | Auth Required |
|---|---|---|---|
| GET | `/api/playlists` | List all user playlists. | Yes |
| POST | `/api/playlists` | Create a new playlist. | Yes |

### `tracks`
| Method | Path | Summary | Auth Required |
|---|---|---|---|
| GET | `/api/tracks` | List all tracks in the library. | Yes |
| POST | `/api/tracks` | Add a new track to the library. | Yes |
| GET | `/api/tracks/{track_id}` | Retrieve a specific track by its ID. | Yes |
| PATCH | `/api/tracks/{track_id}` | Modify an existing track's data. | Yes |
| DELETE | `/api/tracks/{track_id}` | Remove a track from the library. | Yes |
| POST | `/api/tracks/{track_id}/cover` | Upload a cover image for a track. | Yes |
| POST | `/api/tracks/metadata` | Retrieve metadata for multiple tracks in one call. | Yes |

### `download`
| Method | Path | Summary | Auth Required |
|---|---|---|---|
| POST | `/api/download/` | Add one or more tracks to the download queue. | Yes |
| GET | `/api/download/status` | Get the status of the download queue. | Yes |
| POST | `/api/download/retry` | Retry failed download jobs. | Yes |
| POST | `/api/download/process` | Manually trigger the download queue processor. | Yes |

### `sync`
| Method | Path | Summary | Auth Required |
|---|---|---|---|
| POST | `/api/sync/trigger` | Trigger a general synchronization task. | Yes |
| POST | `/api/sync/playlist/sync` | Synchronize a specific playlist. | Yes |

### `config`
| Method | Path | Summary | Auth Required |
|---|---|---|---|
| GET | `/api/config` | Retrieve the current application configuration. | Yes |
| PATCH | `/api/config` | Update specific fields in the configuration. | Yes |
| POST | `/api/config/reset` | Reset the configuration to default values. | Yes |

### `network`
| Method | Path | Summary | Auth Required |
|---|---|---|---|
| GET | `/api/network` | Retrieve the current network/proxy settings. | Yes |
| PATCH | `/api/network` | Update the network/proxy settings. | Yes |

### `search`
| Method | Path | Summary | Auth Required |
|---|---|---|---|
| GET | `/api/search` | Search for tracks, albums, and artists. | Yes |

### `webhooks`
| Method | Path | Summary | Auth Required |
|---|---|---|---|
| POST | `/api/webhooks/register` | Register a new webhook URL. | Yes |
| GET | `/api/webhooks` | List all registered webhooks. | Yes |
| DELETE | `/api/webhooks/{hook_id}` | Remove a registered webhook. | Yes |
| POST | `/api/webhooks/fire` | Fire a test event to all registered webhooks. | Yes |

### `spotify`
| Method | Path | Summary | Auth Required |
|---|---|---|---|
| GET | `/api/spotify/login` | Get the URL to initiate Spotify authentication. | No |
| GET | `/api/spotify/callback` | Callback endpoint for the Spotify OAuth flow (legacy). | No |
| GET | `/api/spotify/token_status` | Get the status of the current Spotify token. | Yes |
| POST | `/api/spotify/sync_playlists` | Trigger a full sync of playlists from Spotify. | Yes |
| GET | `/api/spotify/playlists` | List the user's playlists directly from Spotify. | Yes |

### `notifications`
| Method | Path | Summary | Auth Required |
|---|---|---|---|
| POST | `/api/notifications` | Create a new user notification. | Yes |
| GET | `/api/notifications/{user_id}` | Retrieve notifications for a specific user. | Yes |
| PATCH | `/api/notifications/{notification_id}` | Mark a specific notification as read. | Yes |
