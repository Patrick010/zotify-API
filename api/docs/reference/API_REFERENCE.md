> This file is auto-generated from the OpenAPI specification. For planned endpoints (not yet implemented), see `docs/api/endpoints.yaml`.

# API Reference

This document provides a detailed reference for the Zotify API. It is generated from the OpenAPI 3.0 specification.

## General Information

- **Title:** Zotify API
- **Version:** 0.1.20
- **Description:** A RESTful API for Zotify, a Spotify music downloader.

## Endpoints Summary

This summary is grouped by tags and provides a quick overview of all available endpoints.

### `auth`

- `GET /api/auth/spotify/login`: Spotify Login
- `GET /api/auth/spotify/callback`: Spotify Callback
- `GET /api/auth/status`: Get Status
- `POST /api/auth/logout`: Logout
- `GET /api/auth/refresh`: Refresh

### `cache`

- `GET /api/cache`: Get Cache Stats
- `DELETE /api/cache`: Clear Cache

### `config`

- `GET /api/config`: Get Config
- `PATCH /api/config`: Update Config
- `POST /api/config/reset`: Reset Config

### `downloads`

- `POST /api/downloads`: Download
- `GET /api/downloads/status`: Get Download Queue Status
- `POST /api/downloads/retry`: Retry Failed Downloads
- `POST /api/downloads/process`: Process Job

### `health`

- `GET /health`: Health Check

### `network`

- `GET /api/network`: Get Network
- `PATCH /api/network`: Update Network

### `notifications`

- `POST /api/notifications`: Create Notification
- `GET /api/notifications/{user_id}`: Get Notifications
- `PATCH /api/notifications/{notification_id}`: Mark Notification As Read

### `playlists`

- `GET /api/playlists`: List Playlists
- `POST /api/playlists`: Create New Playlist

### `search`

- `GET /api/search`: Search

### `sync`

- `POST /api/sync/trigger`: Trigger Sync

### `system`

- `POST /api/system/logging/reload`: Reload Logging Config
- `GET /api/system/status`: Get System Status
- `GET /api/system/storage`: Get System Storage
- `GET /api/system/logs`: Get System Logs
- `POST /api/system/reload`: Reload System Config
- `POST /api/system/reset`: Reset System State
- `GET /api/system/uptime`: Get Uptime
- `GET /api/system/env`: Get Env
- `GET /api/schema`: Get Schema

### `tracks`

- `GET /api/tracks`: List Tracks
- `POST /api/tracks`: Create Track
- `GET /api/tracks/{track_id}`: Get Track
- `PATCH /api/tracks/{track_id}`: Update Track
- `DELETE /api/tracks/{track_id}`: Delete Track
- `POST /api/tracks/{track_id}/cover`: Upload Track Cover
- `POST /api/tracks/metadata`: Get Tracks Metadata
- `GET /api/tracks/{track_id}/metadata`: Get extended metadata for a track
- `PATCH /api/tracks/{track_id}/metadata`: Update extended metadata for a track

### `user`

- `GET /api/user/profile`: Get User Profile
- `PATCH /api/user/profile`: Update User Profile
- `GET /api/user/preferences`: Get User Preferences
- `PATCH /api/user/preferences`: Update User Preferences
- `GET /api/user/liked`: Get User Liked
- `POST /api/user/sync_liked`: Sync User Liked
- `GET /api/user/history`: Get User History
- `DELETE /api/user/history`: Delete User History

### `webhooks`

- `POST /api/webhooks/register`: Register Webhook
- `GET /api/webhooks`: List Webhooks
- `DELETE /api/webhooks/{hook_id}`: Unregister Webhook
- `POST /api/webhooks/fire`: Fire Webhook

<br>

---

<br>

<details>
<summary>Full OpenAPI Specification (JSON)</summary>

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "Zotify API",
    "description": "A RESTful API for Zotify, a Spotify music downloader.",
    "version": "0.1.20"
  },
  "paths": {
    "/api/auth/spotify/login": {
      "get": {
        "tags": [
          "auth"
        ],
        "summary": "Spotify Login",
        "operationId": "spotify_login_api_auth_spotify_login_get",
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/OAuthLoginResponse"
                }
              }
            }
          }
        }
      }
    },
    "/api/auth/spotify/callback": {
      "get": {
        "tags": [
          "auth"
        ],
        "summary": "Spotify Callback",
        "operationId": "spotify_callback_api_auth_spotify_callback_get",
        "parameters": [
          {
            "name": "code",
            "in": "query",
            "required": true,
            "schema": {
              "type": "string",
              "title": "Code"
            }
          },
          {
            "name": "state",
            "in": "query",
            "required": true,
            "schema": {
              "type": "string",
              "title": "State"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {}
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/api/auth/status": {
      "get": {
        "tags": [
          "auth"
        ],
        "summary": "Get Status",
        "description": "Returns the current authentication status",
        "operationId": "get_status_api_auth_status_get",
        "parameters": [
          {
            "name": "X-API-Key",
            "in": "header",
            "required": false,
            "schema": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "title": "X-Api-Key"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/AuthStatus"
                }
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/api/auth/logout": {
      "post": {
        "tags": [
          "auth"
        ],
        "summary": "Logout",
        "description": "Clears stored Spotify credentials from the database.\\n\\nThis function deletes the token from local storage, effectively logging the user out\\nfrom this application's perspective.",
        "operationId": "logout_api_auth_logout_post",
        "parameters": [
          {
            "name": "X-API-Key",
            "in": "header",
            "required": false,
            "schema": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "title": "X-Api-Key"
            }
          }
        ],
        "responses": {
          "204": {
            "description": "Successful Response"
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/api/auth/refresh": {
      "get": {
        "tags": [
          "auth"
        ],
        "summary": "Refresh",
        "description": "Refreshes the Spotify access token",
        "operationId": "refresh_api_auth_refresh_get",
        "parameters": [
          {
            "name": "X-API-Key",
            "in": "header",
            "required": false,
            "schema": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "title": "X-Api-Key"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/RefreshResponse"
                }
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/api/cache": {
      "get": {
        "tags": [
          "cache"
        ],
        "summary": "Get Cache Stats",
        "description": "Returns statistics about the cache.",
        "operationId": "get_cache_api_cache_get",
        "responses": {
          "200": {
            "description": "Cache statistics.",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/StandardResponse_CacheStatusResponse_"
                }
              }
            }
          }
        }
      },
      "delete": {
        "tags": [
          "cache"
        ],
        "summary": "Clear Cache",
        "description": "Clear entire cache or by type.",
        "operationId": "clear_cache_api_cache_delete",
        "parameters": [
          {
            "name": "X-API-Key",
            "in": "header",
            "required": false,
            "schema": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "title": "X-Api-Key"
            }
          }
        ],
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/CacheClearRequest"
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Cache statistics after clearing.",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/StandardResponse_CacheStatusResponse_"
                }
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/api/system/logging/reload": {
      "post": {
        "tags": [
          "system"
        ],
        "summary": "Reload Logging Config",
        "description": "Reloads the logging framework's configuration from the\\n`logging_framework.yml` file at runtime.",
        "operationId": "reload_logging_config_api_system_logging_reload_post",
        "parameters": [
          {
            "name": "X-API-Key",
            "in": "header",
            "required": false,
            "schema": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "title": "X-Api-Key"
            }
          }
        ],
        "responses": {
          "202": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {}
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/api/system/status": {
      "get": {
        "tags": [
          "system"
        ],
        "summary": "Get System Status",
        "operationId": "get_system_status_api_system_status_get",
        "parameters": [
          {
            "name": "X-API-Key",
            "in": "header",
            "required": false,
            "schema": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "title": "X-Api-Key"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {}
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/api/system/storage": {
      "get": {
        "tags": [
          "system"
        ],
        "summary": "Get System Storage",
        "operationId": "get_system_storage_api_system_storage_get",
        "parameters": [
          {
            "name": "X-API-Key",
            "in": "header",
            "required": false,
            "schema": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "title": "X-Api-Key"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {}
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/api/system/logs": {
      "get": {
        "tags": [
          "system"
        ],
        "summary": "Get System Logs",
        "operationId": "get_system_logs_api_system_logs_get",
        "parameters": [
          {
            "name": "X-API-Key",
            "in": "header",
            "required": false,
            "schema": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "title": "X-Api-Key"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {}
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/api/system/reload": {
      "post": {
        "tags": [
          "system"
        ],
        "summary": "Reload System Config",
        "operationId": "reload_system_config_api_system_reload_post",
        "parameters": [
          {
            "name": "X-API-Key",
            "in": "header",
            "required": false,
            "schema": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "title": "X-Api-Key"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {}
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/api/system/reset": {
      "post": {
        "tags": [
          "system"
        ],
        "summary": "Reset System State",
        "operationId": "reset_system_state_api_system_reset_post",
        "parameters": [
          {
            "name": "X-API-Key",
            "in": "header",
            "required": false,
            "schema": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "title": "X-Api-Key"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {}
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/api/system/uptime": {
      "get": {
        "tags": [
          "system"
        ],
        "summary": "Get Uptime",
        "description": "Returns uptime in seconds and human-readable format.",
        "operationId": "get_uptime_api_system_uptime_get",
        "parameters": [
          {
            "name": "X-API-Key",
            "in": "header",
            "required": false,
            "schema": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "title": "X-Api-Key"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/StandardResponse_SystemUptime_"
                }
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/api/system/env": {
      "get": {
        "tags": [
          "system"
        ],
        "summary": "Get Env",
        "description": "Returns a safe subset of environment info",
        "operationId": "get_env_api_system_env_get",
        "parameters": [
          {
            "name": "X-API-Key",
            "in": "header",
            "required": false,
            "schema": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "title": "X-Api-Key"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/StandardResponse_SystemEnv_"
                }
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/api/user/profile": {
      "get": {
        "tags": [
          "user"
        ],
        "summary": "Get User Profile",
        "operationId": "get_user_profile_api_user_profile_get",
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/StandardResponse_UserProfileResponse_"
                }
              }
            }
          }
        }
      },
      "patch": {
        "tags": [
          "user"
        ],
        "summary": "Update User Profile",
        "operationId": "update_user_profile_api_user_profile_patch",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/UserProfileUpdate"
              }
            }
          },
          "required": true
        },
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/StandardResponse_UserProfileResponse_"
                }
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/api/user/preferences": {
      "get": {
        "tags": [
          "user"
        ],
        "summary": "Get User Preferences",
        "operationId": "get_user_preferences_api_user_preferences_get",
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/StandardResponse_UserPreferences_"
                }
              }
            }
          }
        }
      },
      "patch": {
        "tags": [
          "user"
        ],
        "summary": "Update User Preferences",
        "operationId": "update_user_preferences_api_user_preferences_patch",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/UserPreferencesUpdate"
              }
            }
          },
          "required": true
        },
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/StandardResponse_UserPreferences_"
                }
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/api/user/liked": {
      "get": {
        "tags": [
          "user"
        ],
        "summary": "Get User Liked",
        "operationId": "get_user_liked_api_user_liked_get",
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "additionalProperties": true,
                  "type": "object",
                  "title": "Response Get User Liked Api User Liked Get"
                }
              }
            }
          }
        }
      }
    },
    "/api/user/sync_liked": {
      "post": {
        "tags": [
          "user"
        ],
        "summary": "Sync User Liked",
        "operationId": "sync_user_liked_api_user_sync_liked_post",
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/StandardResponse_SyncLikedResponse_"
                }
              }
            }
          }
        }
      }
    },
    "/api/user/history": {
      "get": {
        "tags": [
          "user"
        ],
        "summary": "Get User History",
        "operationId": "get_user_history_api_user_history_get",
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "additionalProperties": true,
                  "type": "object",
                  "title": "Response Get User History Api User History Get"
                }
              }
            }
          }
        }
      },
      "delete": {
        "tags": [
          "user"
        ],
        "summary": "Delete User History",
        "operationId": "delete_user_history_api_user_history_delete",
        "responses": {
          "204": {
            "description": "Successful Response"
          }
        }
      }
    },
    "/api/playlists": {
      "get": {
        "tags": [
          "playlists"
        ],
        "summary": "List Playlists",
        "operationId": "list_playlists_api_playlists_get",
        "parameters": [
          {
            "name": "limit",
            "in": "query",
            "required": false,
            "schema": {
              "type": "integer",
              "minimum": 1,
              "default": 25,
              "title": "Limit"
            }
          },
          {
            "name": "offset",
            "in": "query",
            "required": false,
            "schema": {
              "type": "integer",
              "minimum": 0,
              "default": 0,
              "title": "Offset"
            }
          },
          {
            "name": "search",
            "in": "query",
            "required": false,
            "schema": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "title": "Search"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/PlaylistsResponse"
                }
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      },
      "post": {
        "tags": [
          "playlists"
        ],
        "summary": "Create New Playlist",
        "operationId": "create_new_playlist_api_playlists_post",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/PlaylistIn"
              }
            }
          }
        },
        "responses": {
          "201": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/PlaylistOut"
                }
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/api/tracks": {
      "get": {
        "tags": [
          "tracks"
        ],
        "summary": "List Tracks",
        "operationId": "list_tracks_api_tracks_get",
        "parameters": [
          {
            "name": "limit",
            "in": "query",
            "required": false,
            "schema": {
              "type": "integer",
              "maximum": 100,
              "minimum": 1,
              "default": 25,
              "title": "Limit"
            }
          },
          {
            "name": "offset",
            "in": "query",
            "required": false,
            "schema": {
              "type": "integer",
              "default": 0,
              "title": "Offset"
            }
          },
          {
            "name": "q",
            "in": "query",
            "required": false,
            "schema": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "title": "Q"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "additionalProperties": true,
                  "title": "Response List Tracks Api Tracks Get"
                }
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      },
      "post": {
        "tags": [
          "tracks"
        ],
        "summary": "Create Track",
        "operationId": "create_track_api_tracks_post",
        "parameters": [
          {
            "name": "X-API-Key",
            "in": "header",
            "required": false,
            "schema": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "title": "X-Api-Key"
            }
          }
        ],
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/CreateTrackModel"
              }
            }
          }
        },
        "responses": {
          "201": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/TrackResponseModel"
                }
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/api/tracks/{track_id}": {
      "get": {
        "tags": [
          "tracks"
        ],
        "summary": "Get Track",
        "operationId": "get_track_api_tracks__track_id__get",
        "parameters": [
          {
            "name": "track_id",
            "in": "path",
            "required": true,
            "schema": {
              "type": "string",
              "title": "Track Id"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/TrackResponseModel"
                }
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      },
      "patch": {
        "tags": [
          "tracks"
        ],
        "summary": "Update Track",
        "operationId": "update_track_api_tracks__track_id__patch",
        "parameters": [
          {
            "name": "track_id",
            "in": "path",
            "required": true,
            "schema": {
              "type": "string",
              "title": "Track Id"
            }
          },
          {
            "name": "X-API-Key",
            "in": "header",
            "required": false,
            "schema": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "title": "X-Api-Key"
            }
          }
        ],
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/UpdateTrackModel"
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/TrackResponseModel"
                }
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      },
      "delete": {
        "tags": [
          "tracks"
        ],
        "summary": "Delete Track",
        "operationId": "delete_track_api_tracks__track_id__delete",
        "parameters": [
          {
            "name": "track_id",
            "in": "path",
            "required": true,
            "schema": {
              "type": "string",
              "title": "Track Id"
            }
          },
          {
            "name": "X-API-Key",
            "in": "header",
            "required": false,
            "schema": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "title": "X-Api-Key"
            }
          }
        ],
        "responses": {
          "204": {
            "description": "Successful Response"
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/api/tracks/{track_id}/cover": {
      "post": {
        "tags": [
          "tracks"
        ],
        "summary": "Upload Track Cover",
        "operationId": "upload_track_cover_api_tracks__track_id__cover_post",
        "parameters": [
          {
            "name": "track_id",
            "in": "path",
            "required": true,
            "schema": {
              "type": "string",
              "title": "Track Id"
            }
          },
          {
            "name": "X-API-Key",
            "in": "header",
            "required": false,
            "schema": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "title": "X-Api-Key"
            }
          }
        ],
        "requestBody": {
          "required": true,
          "content": {
            "multipart/form-data": {
              "schema": {
                "$ref": "#/components/schemas/Body_upload_track_cover_api_tracks__track_id__cover_post"
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {}
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/api/tracks/metadata": {
      "post": {
        "tags": [
          "tracks"
        ],
        "summary": "Get Tracks Metadata",
        "description": "Returns metadata for all given tracks in one call.",
        "operationId": "get_tracks_metadata_api_tracks_metadata_post",
        "parameters": [
          {
            "name": "X-API-Key",
            "in": "header",
            "required": false,
            "schema": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "title": "X-Api-Key"
            }
          }
        ],
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/TrackMetadataRequest"
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/TrackMetadataResponse"
                }
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/api/tracks/{track_id}/metadata": {
      "get": {
        "tags": [
          "tracks"
        ],
        "summary": "Get extended metadata for a track",
        "description": "Retrieves extended metadata for a specific track.\\n\\n- **track_id**: The ID of the track to retrieve metadata for.",
        "operationId": "get_track_metadata_api_tracks__track_id__metadata_get",
        "parameters": [
          {
            "name": "track_id",
            "in": "path",
            "required": true,
            "schema": {
              "type": "string",
              "title": "Track Id"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/MetadataResponse"
                }
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      },
      "patch": {
        "tags": [
          "tracks"
        ],
        "summary": "Update extended metadata for a track",
        "description": "Updates extended metadata for a specific track.\\n\\n- **track_id**: The ID of the track to update.\\n- **meta**: A `MetadataUpdate` object with the fields to update.",
        "operationId": "patch_track_metadata_api_tracks__track_id__metadata_patch",
        "parameters": [
          {
            "name": "track_id",
            "in": "path",
            "required": true,
            "schema": {
              "type": "string",
              "title": "Track Id"
            }
          }
        ],
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/MetadataUpdate"
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/MetadataPatchResponse"
                }
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/api/downloads": {
      "post": {
        "tags": [
          "downloads"
        ],
        "summary": "Download",
        "description": "Queue one or more tracks for download.",
        "operationId": "download_api_downloads_post",
        "parameters": [
          {
            "name": "X-API-Key",
            "in": "header",
            "required": false,
            "schema": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "title": "X-Api-Key"
            }
          }
        ],
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/DownloadRequest"
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/StandardResponse_List_DownloadJob__"
                }
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/api/downloads/status": {
      "get": {
        "tags": [
          "downloads"
        ],
        "summary": "Get Download Queue Status",
        "description": "Get the current status of the download queue.",
        "operationId": "get_download_queue_status_api_downloads_status_get",
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/StandardResponse_DownloadQueueStatus_"
                }
              }
            }
          }
        }
      }
    },
    "/api/downloads/retry": {
      "post": {
        "tags": [
          "downloads"
        ],
        "summary": "Retry Failed Downloads",
        "description": "Retry all failed downloads in the queue.",
        "operationId": "retry_failed_downloads_api_downloads_retry_post",
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/StandardResponse_DownloadQueueStatus_"
                }
              }
            }
          }
        }
      }
    },
    "/api/downloads/process": {
      "post": {
        "tags": [
          "downloads"
        ],
        "summary": "Process Job",
        "description": "Manually process one job from the download queue.",
        "operationId": "process_job_api_downloads_process_post",
        "parameters": [
          {
            "name": "X-API-Key",
            "in": "header",
            "required": false,
            "schema": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "title": "X-Api-Key"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/StandardResponse_Union_DownloadJob__NoneType__"
                }
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/api/sync/trigger": {
      "post": {
        "tags": [
          "sync"
        ],
        "summary": "Trigger Sync",
        "description": "Triggers a global synchronization job.\\nIn a real app, this would be a background task.",
        "operationId": "trigger_sync_api_sync_trigger_post",
        "parameters": [
          {
            "name": "X-API-Key",
            "in": "header",
            "required": false,
            "schema": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "title": "X-Api-Key"
            }
          }
        ],
        "responses": {
          "202": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {}
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/api/config": {
      "get": {
        "tags": [
          "config"
        ],
        "summary": "Get Config",
        "operationId": "get_config_api_config_get",
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/StandardResponse_ConfigModel_"
                }
              }
            }
          }
        }
      },
      "patch": {
        "tags": [
          "config"
        ],
        "summary": "Update Config",
        "operationId": "update_config_api_config_patch",
        "parameters": [
          {
            "name": "X-API-Key",
            "in": "header",
            "required": false,
            "schema": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "title": "X-Api-Key"
            }
          }
        ],
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/ConfigUpdate"
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/StandardResponse_ConfigModel_"
                }
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/api/config/reset": {
      "post": {
        "tags": [
          "config"
        ],
        "summary": "Reset Config",
        "operationId": "reset_config_api_config_reset_post",
        "parameters": [
          {
            "name": "X-API-Key",
            "in": "header",
            "required": false,
            "schema": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "title": "X-Api-Key"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/StandardResponse_ConfigModel_"
                }
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/api/network": {
      "get": {
        "tags": [
          "network"
        ],
        "summary": "Get Network",
        "operationId": "get_network_api_network_get",
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/StandardResponse_NetworkConfigResponse_"
                }
              }
            }
          }
        }
      },
      "patch": {
        "tags": [
          "network"
        ],
        "summary": "Update Network",
        "operationId": "update_network_api_network_patch",
        "parameters": [
          {
            "name": "X-API-Key",
            "in": "header",
            "required": false,
            "schema": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "title": "X-Api-Key"
            }
          }
        ],
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/ProxyConfig"
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/StandardResponse_NetworkConfigResponse_"
                }
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/api/search": {
      "get": {
        "tags": [
          "search"
        ],
        "summary": "Search",
        "operationId": "search_api_search_get",
        "parameters": [
          {
            "name": "q",
            "in": "query",
            "required": true,
            "schema": {
              "type": "string",
              "title": "Q"
            }
          },
          {
            "name": "type",
            "in": "query",
            "required": false,
            "schema": {
              "enum": [
                "track",
                "album",
                "artist",
                "playlist",
                "all"
              ],
              "type": "string",
              "default": "all",
              "title": "Type"
            }
          },
          {
            "name": "limit",
            "in": "query",
            "required": false,
            "schema": {
              "type": "integer",
              "default": 20,
              "title": "Limit"
            }
          },
          {
            "name": "offset",
            "in": "query",
            "required": false,
            "schema": {
              "type": "integer",
              "default": 0,
              "title": "Offset"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {}
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/api/webhooks/register": {
      "post": {
        "tags": [
          "webhooks"
        ],
        "summary": "Register Webhook",
        "operationId": "register_webhook_api_webhooks_register_post",
        "parameters": [
          {
            "name": "X-API-Key",
            "in": "header",
            "required": false,
            "schema": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "title": "X-Api-Key"
            }
          }
        ],
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/WebhookPayload"
              }
            }
          }
        },
        "responses": {
          "201": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/StandardResponse_Webhook_"
                }
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/api/webhooks": {
      "get": {
        "tags": [
          "webhooks"
        ],
        "summary": "List Webhooks",
        "operationId": "list_webhooks_api_webhooks_get",
        "parameters": [
          {
            "name": "X-API-Key",
            "in": "header",
            "required": false,
            "schema": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "title": "X-Api-Key"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "additionalProperties": true,
                  "title": "Response List Webhooks Api Webhooks Get"
                }
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/api/webhooks/{hook_id}": {
      "delete": {
        "tags": [
          "webhooks"
        ],
        "summary": "Unregister Webhook",
        "operationId": "unregister_webhook_api_webhooks__hook_id__delete",
        "parameters": [
          {
            "name": "hook_id",
            "in": "path",
            "required": true,
            "schema": {
              "type": "string",
              "title": "Hook Id"
            }
          },
          {
            "name": "X-API-Key",
            "in": "header",
            "required": false,
            "schema": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "title": "X-Api-Key"
            }
          }
        ],
        "responses": {
          "204": {
            "description": "Successful Response"
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/api/webhooks/fire": {
      "post": {
        "tags": [
          "webhooks"
        ],
        "summary": "Fire Webhook",
        "operationId": "fire_webhook_api_webhooks_fire_post",
        "parameters": [
          {
            "name": "X-API-Key",
            "in": "header",
            "required": false,
            "schema": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "title": "X-Api-Key"
            }
          }
        ],
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/FirePayload"
              }
            }
          }
        },
        "responses": {
          "202": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {}
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/api/notifications": {
      "post": {
        "tags": [
          "notifications"
        ],
        "summary": "Create Notification",
        "operationId": "create_notification_api_notifications_post",
        "parameters": [
          {
            "name": "X-API-Key",
            "in": "header",
            "required": false,
            "schema": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "title": "X-Api-Key"
            }
          }
        ],
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/NotificationCreate"
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/StandardResponse_Notification_"
                }
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/api/notifications/{user_id}": {
      "get": {
        "tags": [
          "notifications"
        ],
        "summary": "Get Notifications",
        "operationId": "get_notifications_api_notifications__user_id__get",
        "parameters": [
          {
            "name": "user_id",
            "in": "path",
            "required": true,
            "schema": {
              "type": "string",
              "title": "User Id"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "additionalProperties": true,
                  "title": "Response Get Notifications Api Notifications  User Id  Get"
                }
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/api/notifications/{notification_id}": {
      "patch": {
        "tags": [
          "notifications"
        ],
        "summary": "Mark Notification As Read",
        "operationId": "mark_notification_as_read_api_notifications__notification_id__patch",
        "parameters": [
          {
            "name": "notification_id",
            "in": "path",
            "required": true,
            "schema": {
              "type": "string",
              "title": "Notification Id"
            }
          },
          {
            "name": "X-API-Key",
            "in": "header",
            "required": false,
            "schema": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "title": "X-Api-Key"
            }
          }
        ],
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/NotificationUpdate"
              }
            }
          }
        },
        "responses": {
          "204": {
            "description": "Successful Response"
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/ping": {
      "get": {
        "summary": "Ping",
        "operationId": "ping_ping_get",
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {}
              }
            }
          }
        }
      }
    },
    "/health": {
      "get": {
        "tags": [
          "health"
        ],
        "summary": "Health Check",
        "operationId": "health_check_health_get",
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {}
              }
            }
          }
        }
      }
    },
    "/version": {
      "get": {
        "summary": "Version",
        "operationId": "version_version_get",
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {}
              }
            }
          }
        }
      }
    },
    "/api/schema": {
      "get": {
        "tags": [
          "system"
        ],
        "summary": "Get Schema",
        "description": "Returns either full OpenAPI spec or schema fragment for requested object type (via query param).",
        "operationId": "get_schema_api_schema_get",
        "parameters": [
          {
            "name": "q",
            "in": "query",
            "required": false,
            "schema": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "title": "Q"
            }
          },
          {
            "name": "X-API-Key",
            "in": "header",
            "required": false,
            "schema": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "null"
                }
              ],
              "title": "X-Api-Key"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {}
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    }
  },
  "components": {
    "schemas": {
      "AuthStatus": {
        "properties": {
          "authenticated": {
            "type": "boolean",
            "title": "Authenticated"
          },
          "user_id": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ],
            "title": "User Id"
          },
          "token_valid": {
            "type": "boolean",
            "title": "Token Valid"
          },
          "expires_in": {
            "type": "integer",
            "title": "Expires In"
          }
        },
        "type": "object",
        "required": [
          "authenticated",
          "token_valid",
          "expires_in"
        ],
        "title": "AuthStatus"
      },
      "Body_upload_track_cover_api_tracks__track_id__cover_post": {
        "properties": {
          "cover_image": {
            "type": "string",
            "format": "binary",
            "title": "Cover Image"
          }
        },
        "type": "object",
        "required": [
          "cover_image"
        ],
        "title": "Body_upload_track_cover_api_tracks__track_id__cover_post"
      },
      "CacheClearRequest": {
        "properties": {
          "type": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ],
            "title": "Type",
            "description": "The type of cache to clear (e.g., 'search', 'metadata'). If omitted, the entire cache is cleared."
          }
        },
        "type": "object",
        "title": "CacheClearRequest"
      },
      "CacheStatusResponse": {
        "properties": {
          "total_items": {
            "type": "integer",
            "title": "Total Items",
            "description": "The total number of items in the cache."
          },
          "by_type": {
            "additionalProperties": {
              "type": "integer"
            },
            "type": "object",
            "title": "By Type",
            "description": "A dictionary with the number of items for each cache type."
          }
        },
        "type": "object",
        "required": [
          "total_items",
          "by_type"
        ],
        "title": "CacheStatusResponse"
      },
      "ConfigModel": {
        "properties": {
          "library_path": {
            "type": "string",
            "title": "Library Path"
          },
          "scan_on_startup": {
            "type": "boolean",
            "title": "Scan On Startup"
          },
          "cover_art_embed_enabled": {
            "type": "boolean",
            "title": "Cover Art Embed Enabled"
          }
        },
        "type": "object",
        "required": [
          "library_path",
          "scan_on_startup",
          "cover_art_embed_enabled"
        ],
        "title": "ConfigModel"
      },
      "ConfigUpdate": {
        "properties": {
          "library_path": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ],
            "title": "Library Path"
          },
          "scan_on_startup": {
            "anyOf": [
              {
                "type": "boolean"
              },
              {
                "type": "null"
              }
            ],
            "title": "Scan On Startup"
          },
          "cover_art_embed_enabled": {
            "anyOf": [
              {
                "type": "boolean"
              },
              {
                "type": "null"
              }
            ],
            "title": "Cover Art Embed Enabled"
          }
        },
        "additionalProperties": false,
        "type": "object",
        "title": "ConfigUpdate"
      },
      "CreateTrackModel": {
        "properties": {
          "name": {
            "type": "string",
            "maxLength": 200,
            "minLength": 1,
            "title": "Name"
          },
          "artist": {
            "anyOf": [
              {
                "type": "string",
                "maxLength": 200
              },
              {
                "type": "null"
              }
            ],
            "title": "Artist"
          },
          "album": {
            "anyOf": [
              {
                "type": "string",
                "maxLength": 200
              },
              {
                "type": "null"
              }
            ],
            "title": "Album"
          },
          "duration_seconds": {
            "anyOf": [
              {
                "type": "integer",
                "exclusiveMinimum": 0
              },
              {
                "type": "null"
              }
            ],
            "title": "Duration Seconds"
          },
          "path": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ],
            "title": "Path"
          }
        },
        "type": "object",
        "required": [
          "name"
        ],
        "title": "CreateTrackModel"
      },
      "DownloadJob": {
        "properties": {
          "track_id": {
            "type": "string",
            "title": "Track Id"
          },
          "job_id": {
            "type": "string",
            "title": "Job Id"
          },
          "status": {
            "$ref": "#/components/schemas/DownloadJobStatus"
          },
          "progress": {
            "anyOf": [
              {
                "type": "number"
              },
              {
                "type": "null"
              }
            ],
            "title": "Progress"
          },
          "created_at": {
            "type": "string",
            "format": "date-time",
            "title": "Created At"
          },
          "error_message": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ],
            "title": "Error Message"
          }
        },
        "type": "object",
        "required": [
          "track_id",
          "job_id",
          "status",
          "progress",
          "created_at",
          "error_message"
        ],
        "title": "DownloadJob"
      },
      "DownloadJobStatus": {
        "type": "string",
        "enum": [
          "pending",
          "in_progress",
          "completed",
          "failed"
        ],
        "title": "DownloadJobStatus"
      },
      "DownloadQueueStatus": {
        "properties": {
          "total_jobs": {
            "type": "integer",
            "title": "Total Jobs"
          },
          "pending": {
            "type": "integer",
            "title": "Pending"
          },
          "completed": {
            "type": "integer",
            "title": "Completed"
          },
          "failed": {
            "type": "integer",
            "title": "Failed"
          },
          "jobs": {
            "items": {
              "$ref": "#/components/schemas/DownloadJob"
            },
            "type": "array",
            "title": "Jobs"
          }
        },
        "type": "object",
        "required": [
          "total_jobs",
          "pending",
          "completed",
          "failed",
          "jobs"
        ],
        "title": "DownloadQueueStatus"
      },
      "DownloadRequest": {
        "properties": {
          "track_ids": {
            "items": {
              "type": "string"
            },
            "type": "array",
            "title": "Track Ids"
          }
        },
        "type": "object",
        "required": [
          "track_ids"
        ],
        "title": "DownloadRequest"
      },
      "FirePayload": {
        "properties": {
          "event": {
            "type": "string",
            "title": "Event"
          },
          "data": {
            "additionalProperties": true,
            "type": "object",
            "title": "Data"
          }
        },
        "type": "object",
        "required": [
          "event",
          "data"
        ],
        "title": "FirePayload"
      },
      "HTTPValidationError": {
        "properties": {
          "detail": {
            "items": {
              "$ref": "#/components/schemas/ValidationError"
            },
            "type": "array",
            "title": "Detail"
          }
        },
        "type": "object",
        "title": "HTTPValidationError"
      },
      "MetadataPatchResponse": {
        "properties": {
          "status": {
            "type": "string",
            "title": "Status"
          },
          "track_id": {
            "type": "string",
            "title": "Track Id"
          }
        },
        "type": "object",
        "required": [
          "status",
          "track_id"
        ],
        "title": "MetadataPatchResponse"
      },
      "MetadataResponse": {
        "properties": {
          "title": {
            "type": "string",
            "title": "Title"
          },
          "mood": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ],
            "title": "Mood"
          },
          "rating": {
            "anyOf": [
              {
                "type": "integer"
              },
              {
                "type": "null"
              }
            ],
            "title": "Rating"
          },
          "source": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ],
            "title": "Source"
          }
        },
        "type": "object",
        "required": [
          "title"
        ],
        "title": "MetadataResponse"
      },
      "MetadataUpdate": {
        "properties": {
          "mood": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ],
            "title": "Mood"
          },
          "rating": {
            "anyOf": [
              {
                "type": "integer"
              },
              {
                "type": "null"
              }
            ],
            "title": "Rating"
          },
          "source": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ],
            "title": "Source"
          }
        },
        "type": "object",
        "title": "MetadataUpdate"
      },
      "NetworkConfigResponse": {
        "properties": {
          "proxy_enabled": {
            "type": "boolean",
            "title": "Proxy Enabled"
          },
          "http_proxy": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ],
            "title": "Http Proxy"
          },
          "https_proxy": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ],
            "title": "Https Proxy"
          }
        },
        "type": "object",
        "required": [
          "proxy_enabled"
        ],
        "title": "NetworkConfigResponse"
      },
      "Notification": {
        "properties": {
          "id": {
            "type": "string",
            "title": "Id"
          },
          "user_id": {
            "type": "string",
            "title": "User Id"
          },
          "message": {
            "type": "string",
            "title": "Message"
          },
          "read": {
            "type": "boolean",
            "title": "Read"
          }
        },
        "type": "object",
        "required": [
          "id",
          "user_id",
          "message",
          "read"
        ],
        "title": "Notification"
      },
      "NotificationCreate": {
        "properties": {
          "user_id": {
            "type": "string",
            "title": "User Id"
          },
          "message": {
            "type": "string",
            "title": "Message"
          }
        },
        "type": "object",
        "required": [
          "user_id",
          "message"
        ],
        "title": "NotificationCreate"
      },
      "NotificationUpdate": {
        "properties": {
          "read": {
            "type": "boolean",
            "title": "Read"
          }
        },
        "type": "object",
        "required": [
          "read"
        ],
        "title": "NotificationUpdate"
      },
      "OAuthLoginResponse": {
        "properties": {
          "auth_url": {
            "type": "string",
            "title": "Auth Url"
          }
        },
        "type": "object",
        "required": [
          "auth_url"
        ],
        "title": "OAuthLoginResponse"
      },
      "PlaylistIn": {
        "properties": {
          "name": {
            "type": "string",
            "maxLength": 200,
            "minLength": 1,
            "title": "Name"
          },
          "description": {
            "anyOf": [
              {
                "type": "string",
                "maxLength": 1000
              },
              {
                "type": "null"
              }
            ],
            "title": "Description"
          }
        },
        "type": "object",
        "required": [
          "name"
        ],
        "title": "PlaylistIn"
      },
      "PlaylistOut": {
        "properties": {
          "id": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ],
            "title": "Id"
          },
          "name": {
            "type": "string",
            "title": "Name"
          },
          "description": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ],
            "title": "Description"
          }
        },
        "type": "object",
        "required": [
          "name"
        ],
        "title": "PlaylistOut"
      },
      "PlaylistsResponse": {
        "properties": {
          "data": {
            "items": {
              "$ref": "#/components/schemas/PlaylistOut"
            },
            "type": "array",
            "title": "Data"
          },
          "meta": {
            "additionalProperties": true,
            "type": "object",
            "title": "Meta"
          }
        },
        "type": "object",
        "required": [
          "data",
          "meta"
        ],
        "title": "PlaylistsResponse"
      },
      "ProxyConfig": {
        "properties": {
          "proxy_enabled": {
            "anyOf": [
              {
                "type": "boolean"
              },
              {
                "type": "null"
              }
            ],
            "title": "Proxy Enabled"
          },
          "http_proxy": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ],
            "title": "Http Proxy"
          },
          "https_proxy": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ],
            "title": "Https Proxy"
          }
        },
        "type": "object",
        "title": "ProxyConfig"
      },
      "RefreshResponse": {
        "properties": {
          "expires_at": {
            "type": "integer",
            "title": "Expires At"
          }
        },
        "type": "object",
        "required": [
          "expires_at"
        ],
        "title": "RefreshResponse"
      },
      "StandardResponse_CacheStatusResponse_": {
        "properties": {
          "status": {
            "type": "string",
            "title": "Status",
            "default": "success"
          },
          "data": {
            "$ref": "#/components/schemas/CacheStatusResponse"
          }
        },
        "type": "object",
        "required": [
          "data"
        ],
        "title": "StandardResponse[CacheStatusResponse]"
      },
      "StandardResponse_ConfigModel_": {
        "properties": {
          "status": {
            "type": "string",
            "title": "Status",
            "default": "success"
          },
          "data": {
            "$ref": "#/components/schemas/ConfigModel"
          }
        },
        "type": "object",
        "required": [
          "data"
        ],
        "title": "StandardResponse[ConfigModel]"
      },
      "StandardResponse_DownloadQueueStatus_": {
        "properties": {
          "status": {
            "type": "string",
            "title": "Status",
            "default": "success"
          },
          "data": {
            "$ref": "#/components/schemas/DownloadQueueStatus"
          }
        },
        "type": "object",
        "required": [
          "data"
        ],
        "title": "StandardResponse[DownloadQueueStatus]"
      },
      "StandardResponse_List_DownloadJob__": {
        "properties": {
          "status": {
            "type": "string",
            "title": "Status",
            "default": "success"
          },
          "data": {
            "items": {
              "$ref": "#/components/schemas/DownloadJob"
            },
            "type": "array",
            "title": "Data"
          }
        },
        "type": "object",
        "required": [
          "data"
        ],
        "title": "StandardResponse[List[DownloadJob]]"
      },
      "StandardResponse_NetworkConfigResponse_": {
        "properties": {
          "status": {
            "type": "string",
            "title": "Status",
            "default": "success"
          },
          "data": {
            "$ref": "#/components/schemas/NetworkConfigResponse"
          }
        },
        "type": "object",
        "required": [
          "data"
        ],
        "title": "StandardResponse[NetworkConfigResponse]"
      },
      "StandardResponse_Notification_": {
        "properties": {
          "status": {
            "type": "string",
            "title": "Status",
            "default": "success"
          },
          "data": {
            "$ref": "#/components/schemas/Notification"
          }
        },
        "type": "object",
        "required": [
          "data"
        ],
        "title": "StandardResponse[Notification]"
      },
      "StandardResponse_SyncLikedResponse_": {
        "properties": {
          "status": {
            "type": "string",
            "title": "Status",
            "default": "success"
          },
          "data": {
            "$ref": "#/components/schemas/SyncLikedResponse"
          }
        },
        "type": "object",
        "required": [
          "data"
        ],
        "title": "StandardResponse[SyncLikedResponse]"
      },
      "StandardResponse_SystemEnv_": {
        "properties": {
          "status": {
            "type": "string",
            "title": "Status",
            "default": "success"
          },
          "data": {
            "$ref": "#/components/schemas/SystemEnv"
          }
        },
        "type": "object",
        "required": [
          "data"
        ],
        "title": "StandardResponse[SystemEnv]"
      },
      "StandardResponse_SystemUptime_": {
        "properties": {
          "status": {
            "type": "string",
            "title": "Status",
            "default": "success"
          },
          "data": {
            "$ref": "#/components/schemas/SystemUptime"
          }
        },
        "type": "object",
        "required": [
          "data"
        ],
        "title": "StandardResponse[SystemUptime]"
      },
      "StandardResponse_Union_DownloadJob__NoneType__": {
        "properties": {
          "status": {
            "type": "string",
            "title": "Status",
            "default": "success"
          },
          "data": {
            "anyOf": [
              {
                "$ref": "#/components/schemas/DownloadJob"
              },
              {
                "type": "null"
              }
            ]
          }
        },
        "type": "object",
        "required": [
          "data"
        ],
        "title": "StandardResponse[Union[DownloadJob, NoneType]]"
      },
      "StandardResponse_UserPreferences_": {
        "properties": {
          "status": {
            "type": "string",
            "title": "Status",
            "default": "success"
          },
          "data": {
            "$ref": "#/components/schemas/UserPreferences"
          }
        },
        "type": "object",
        "required": [
          "data"
        ],
        "title": "StandardResponse[UserPreferences]"
      },
      "StandardResponse_UserProfileResponse_": {
        "properties": {
          "status": {
            "type": "string",
            "title": "Status",
            "default": "success"
          },
          "data": {
            "$ref": "#/components/schemas/UserProfileResponse"
          }
        },
        "type": "object",
        "required": [
          "data"
        ],
        "title": "StandardResponse[UserProfileResponse]"
      },
      "StandardResponse_Webhook_": {
        "properties": {
          "status": {
            "type": "string",
            "title": "Status",
            "default": "success"
          },
          "data": {
            "$ref": "#/components/schemas/Webhook"
          }
        },
        "type": "object",
        "required": [
          "data"
        ],
        "title": "StandardResponse[Webhook]"
      },
      "SyncLikedResponse": {
        "properties": {
          "status": {
            "type": "string",
            "title": "Status"
          },
          "synced": {
            "type": "integer",
            "title": "Synced"
          }
        },
        "type": "object",
        "required": [
          "status",
          "synced"
        ],
        "title": "SyncLikedResponse"
      },
      "SystemEnv": {
        "properties": {
          "version": {
            "type": "string",
            "title": "Version"
          },
          "python_version": {
            "type": "string",
            "title": "Python Version"
          },
          "platform": {
            "type": "string",
            "title": "Platform"
          }
        },
        "type": "object",
        "required": [
          "version",
          "python_version",
          "platform"
        ],
        "title": "SystemEnv"
      },
      "SystemUptime": {
        "properties": {
          "uptime_seconds": {
            "type": "number",
            "title": "Uptime Seconds"
          },
          "uptime_human": {
            "type": "string",
            "title": "Uptime Human"
          }
        },
        "type": "object",
        "required": [
          "uptime_seconds",
          "uptime_human"
        ],
        "title": "SystemUptime"
      },
      "TrackMetadataRequest": {
        "properties": {
          "track_ids": {
            "items": {
              "type": "string"
            },
            "type": "array",
            "title": "Track Ids"
          }
        },
        "type": "object",
        "required": [
          "track_ids"
        ],
        "title": "TrackMetadataRequest"
      },
      "TrackMetadataResponse": {
        "properties": {
          "metadata": {
            "items": {
              "additionalProperties": true,
              "type": "object"
            },
            "type": "array",
            "title": "Metadata"
          }
        },
        "type": "object",
        "required": [
          "metadata"
        ],
        "title": "TrackMetadataResponse"
      },
      "TrackResponseModel": {
        "properties": {
          "id": {
            "type": "string",
            "title": "Id"
          },
          "name": {
            "type": "string",
            "title": "Name"
          },
          "artist": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ],
            "title": "Artist"
          },
          "album": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ],
            "title": "Album"
          },
          "duration_seconds": {
            "anyOf": [
              {
                "type": "integer"
              },
              {
                "type": "null"
              }
            ],
            "title": "Duration Seconds"
          },
          "created_at": {
            "type": "string",
            "format": "date-time",
            "title": "Created At"
          },
          "updated_at": {
            "type": "string",
            "format": "date-time",
            "title": "Updated At"
          },
          "cover_url": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ],
            "title": "Cover Url"
          }
        },
        "type": "object",
        "required": [
          "id",
          "name",
          "created_at",
          "updated_at"
        ],
        "title": "TrackResponseModel"
      },
      "UpdateTrackModel": {
        "properties": {
          "name": {
            "anyOf": [
              {
                "type": "string",
                "maxLength": 200,
                "minLength": 1
              },
              {
                "type": "null"
              }
            ],
            "title": "Name"
          },
          "artist": {
            "anyOf": [
              {
                "type": "string",
                "maxLength": 200
              },
              {
                "type": "null"
              }
            ],
            "title": "Artist"
          },
          "album": {
            "anyOf": [
              {
                "type": "string",
                "maxLength": 200
              },
              {
                "type": "null"
              }
            ],
            "title": "Album"
          },
          "duration_seconds": {
            "anyOf": [
              {
                "type": "integer",
                "exclusiveMinimum": 0
              },
              {
                "type": "null"
              }
            ],
            "title": "Duration Seconds"
          },
          "path": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ],
            "title": "Path"
          }
        },
        "type": "object",
        "title": "UpdateTrackModel"
      },
      "UserPreferences": {
        "properties": {
          "theme": {
            "type": "string",
            "title": "Theme"
          },
          "language": {
            "type": "string",
            "title": "Language"
          }
        },
        "type": "object",
        "required": [
          "theme",
          "language"
        ],
        "title": "UserPreferences"
      },
      "UserPreferencesUpdate": {
        "properties": {
          "theme": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ],
            "title": "Theme"
          },
          "language": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ],
            "title": "Language"
          }
        },
        "type": "object",
        "title": "UserPreferencesUpdate"
      },
      "UserProfileResponse": {
        "properties": {
          "name": {
            "type": "string",
            "title": "Name"
          },
          "email": {
            "type": "string",
            "title": "Email"
          },
          "preferences": {
            "$ref": "#/components/schemas/UserPreferences"
          }
        },
        "type": "object",
        "required": [
          "name",
          "email",
          "preferences"
        ],
        "title": "UserProfileResponse"
      },
      "UserProfileUpdate": {
        "properties": {
          "name": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ],
            "title": "Name"
          },
          "email": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ],
            "title": "Email"
          }
        },
        "type": "object",
        "title": "UserProfileUpdate"
      },
      "ValidationError": {
        "properties": {
          "loc": {
            "items": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "integer"
                }
              ]
            },
            "type": "array",
            "title": "Location"
          },
          "msg": {
            "type": "string",
            "title": "Message"
          },
          "type": {
            "type": "string",
            "title": "Error Type"
          }
        },
        "type": "object",
        "required": [
          "loc",
          "msg",
          "type"
        ],
        "title": "ValidationError"
      },
      "Webhook": {
        "properties": {
          "url": {
            "type": "string",
            "title": "Url"
          },
          "events": {
            "items": {
              "type": "string"
            },
            "type": "array",
            "title": "Events"
          },
          "id": {
            "type": "string",
            "title": "Id"
          }
        },
        "type": "object",
        "required": [
          "url",
          "events",
          "id"
        ],
        "title": "Webhook"
      },
      "WebhookPayload": {
        "properties": {
          "url": {
            "type": "string",
            "title": "Url"
          },
          "events": {
            "items": {
              "type": "string"
            },
            "type": "array",
            "title": "Events"
          }
        },
        "type": "object",
        "required": [
          "url",
          "events"
        ],
        "title": "WebhookPayload"
      }
    }
  }
}
```

</details>
