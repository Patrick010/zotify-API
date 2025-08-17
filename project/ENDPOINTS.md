# Project API Endpoints Reference

## Overview

This file lists all public API endpoints for the Zotify API project. It provides a high-level reference for developers, operators, and auditors.

### Notes:

-   Authentication requirements are noted for each endpoint.
-   Always update this file when adding, modifying, or deprecating endpoints.

---

## Zotify API Endpoints

### System & Health
| Endpoint | Method | Path | Auth Required | Purpose |
|---|---|---|---|---|
| OpenAPI Schema | GET,HEAD | `/openapi.json` | No | Retrieve the OpenAPI 3.0 schema for the API. |
| Swagger UI | GET,HEAD | `/docs` | No | Interactive API documentation (Swagger UI). |
| Swagger Auth | GET,HEAD | `/docs/oauth2-redirect` | No | Handles OAuth2 redirects for the Swagger UI. |
| ReDoc | GET,HEAD | `/redoc` | No | Alternative API documentation (ReDoc). |
| Ping | GET | `/ping` | No | Simple health check endpoint. |
| Health Check | GET | `/health` | No | Detailed health check endpoint. |
| Version | GET | `/version` | No | Get application version information. |
| Get Schema | GET | `/api/schema` | Yes | Get a specific component of the OpenAPI schema. |
| System Status | GET | `/api/system/status` | Yes | Get system health and status. |
| Storage Status | GET | `/api/system/storage` | Yes | Get disk and storage usage. |
| Get Logs | GET | `/api/system/logs` | Yes | Fetch system logs. |
| Reload Config | POST | `/api/system/reload` | Yes | Trigger a reload of the application configuration. |
| Reset System | POST | `/api/system/reset` | Yes | Reset the system state. |
| Uptime | GET | `/api/system/uptime` | Yes | Get the API server's uptime. |
| Environment | GET | `/api/system/env` | Yes | Get environment information. |

### Authentication
| Endpoint | Method | Path | Auth Required | Purpose |
|---|---|---|---|---|
| Spotify Callback | POST | `/api/auth/spotify/callback` | No | The callback endpoint for the Spotify OAuth flow. |
| Auth Status | GET | `/api/auth/status` | Yes | Get the current authentication status with Spotify. |
| Logout | POST | `/api/auth/logout` | Yes | Revoke the current Spotify token. |
| Refresh Token | GET | `/api/auth/refresh` | Yes | Force a refresh of the Spotify access token. |

### Configuration
| Endpoint | Method | Path | Auth Required | Purpose |
|---|---|---|---|---|
| Get Config | GET | `/api/config` | Yes | Retrieve the current application configuration. |
| Update Config | PATCH | `/api/config` | Yes | Update specific fields in the configuration. |
| Reset Config | POST | `/api/config/reset` | Yes | Reset the configuration to default values. |

### User Management
| Endpoint | Method | Path | Auth Required | Purpose |
|---|---|---|---|---|
| Get User Profile | GET | `/api/user/profile` | Yes | Retrieve the user's profile information. |
| Update User Profile | PATCH | `/api/user/profile` | Yes | Modify existing user profile data. |
| Get User Preferences | GET | `/api/user/preferences` | Yes | Retrieve the user's preferences. |
| Update User Preferences | PATCH | `/api/user/preferences` | Yes | Modify the user's preferences. |
| Get Liked Songs | GET | `/api/user/liked` | Yes | Retrieve a list of the user's liked songs. |
| Sync Liked Songs | POST | `/api/user/sync_liked` | Yes | Trigger a synchronization of the user's liked songs. |
| Get History | GET | `/api/user/history` | Yes | Retrieve the user's download history. |
| Clear History | DELETE | `/api/user/history` | Yes | Clear the user's download history. |

### Library & Metadata
| Endpoint | Method | Path | Auth Required | Purpose |
|---|---|---|---|---|
| Get Track Metadata | GET | `/api/metadata/{track_id}` | Yes | Retrieve extended metadata for a track. |
| Update Track Metadata | PATCH | `/api/metadata/{track_id}` | Yes | Update extended metadata for a track. |
| Get Playlists | GET | `/api/playlists` | Yes | List all user playlists. |
| Create Playlist | POST | `/api/playlists` | Yes | Create a new playlist. |
| List Tracks | GET | `/api/tracks` | Yes | List all tracks in the library. |
| Get Track | GET | `/api/tracks/{track_id}` | Yes | Retrieve a specific track by its ID. |
| Create Track | POST | `/api/tracks` | Yes | Add a new track to the library. |
| Update Track | PATCH | `/api/tracks/{track_id}` | Yes | Modify an existing track's data. |
| Delete Track | DELETE | `/api/tracks/{track_id}` | Yes | Remove a track from the library. |
| Upload Cover | POST | `/api/tracks/{track_id}/cover` | Yes | Upload a cover image for a track. |
| Get Batch Metadata | POST | `/api/tracks/metadata` | Yes | Retrieve metadata for multiple tracks in one call. |
| Search | GET | `/api/search` | Yes | Search for tracks, albums, and artists. |

### Downloads & Sync
| Endpoint | Method | Path | Auth Required | Purpose |
|---|---|---|---|---|
| Add to Download Queue | POST | `/api/download/` | Yes | Add one or more tracks to the download queue. |
| Get Download Status | GET | `/api/download/status` | Yes | Get the status of the download queue. |
| Retry Downloads | POST | `/api/download/retry` | Yes | Retry failed download jobs. |
| Process Downloads | POST | `/api/download/process` | Yes | Manually trigger the download queue processor. |
| Trigger Sync | POST | `/api/sync/trigger` | Yes | Trigger a general synchronization task. |
| Sync Playlist | POST | `/api/sync/playlist/sync` | Yes | Synchronize a specific playlist. |

### Spotify Integration
| Endpoint | Method | Path | Auth Required | Purpose |
|---|---|---|---|---|
| Spotify Login URL | GET | `/api/spotify/login` | No | Get the URL to initiate Spotify authentication. |
| Spotify Callback | GET | `/api/spotify/callback` | No | Callback endpoint for the Spotify OAuth flow (legacy). |
| Spotify Token Status | GET | `/api/spotify/token_status` | Yes | Get the status of the current Spotify token. |
| Sync Spotify Playlists | POST | `/api/spotify/sync_playlists` | Yes | Trigger a full sync of playlists from Spotify. |
| List Spotify Playlists | GET | `/api/spotify/playlists` | Yes | List the user's playlists directly from Spotify. |

### Notifications & Webhooks
| Endpoint | Method | Path | Auth Required | Purpose |
|---|---|---|---|---|
| Register Webhook | POST | `/api/webhooks/register` | Yes | Register a new webhook URL. |
| List Webhooks | GET | `/api/webhooks` | Yes | List all registered webhooks. |
| Delete Webhook | DELETE | `/api/webhooks/{hook_id}` | Yes | Remove a registered webhook. |
| Fire Test Webhook | POST | `/api/webhooks/fire` | Yes | Fire a test event to all registered webhooks. |
| Create Notification | POST | `/api/notifications` | Yes | Create a new user notification. |
| Get Notifications | GET | `/api/notifications/{user_id}` | Yes | Retrieve notifications for a specific user. |
| Mark Notification Read | PATCH | `/api/notifications/{notification_id}` | Yes | Mark a specific notification as read. |

### Network
| Endpoint | Method | Path | Auth Required | Purpose |
|---|---|---|---|---|
| Get Network Config | GET | `/api/network` | Yes | Retrieve the current network/proxy settings. |
| Update Network Config | PATCH | `/api/network` | Yes | Update the network/proxy settings. |

### Caching
| Endpoint | Method | Path | Auth Required | Purpose |
|---|---|---|---|---|
| Get Cache Status | GET | `/api/cache` | Yes | Get statistics about the application cache. |
| Clear Cache | DELETE | `/api/cache` | Yes | Clear all or part of the application cache. |
