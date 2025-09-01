# Project API Endpoints Reference

## Overview

This file lists all public API endpoints for the Zotify API project, generated from the OpenAPI schema. It provides a high-level reference for developers, operators, and auditors.

### Notes:

-   Authentication requirements are noted for each endpoint.
-   This file is auto-generated. Do not edit it manually.

---

## Zotify API Endpoints

### `auth`
| Method | Path | Summary | Auth Required |
|---|---|---|---|
| GET | `/api/auth/refresh` | Refresh | Yes |
| GET | `/api/auth/spotify/callback` | Spotify Callback | No |
| GET | `/api/auth/spotify/login` | Spotify Login | No |
| GET | `/api/auth/status` | Get Status | Yes |
| POST | `/api/auth/logout` | Logout | Yes |

### `cache`
| Method | Path | Summary | Auth Required |
|---|---|---|---|
| DELETE | `/api/cache` | Clear Cache | Yes |
| GET | `/api/cache` | Get Cache Stats | No |

### `config`
| Method | Path | Summary | Auth Required |
|---|---|---|---|
| GET | `/api/config` | Get Config | No |
| PATCH | `/api/config` | Update Config | Yes |
| POST | `/api/config/reset` | Reset Config | Yes |

### `downloads`
| Method | Path | Summary | Auth Required |
|---|---|---|---|
| GET | `/api/downloads/status` | Get Download Queue Status | No |
| POST | `/api/downloads/process` | Process Job | Yes |
| POST | `/api/downloads/retry` | Retry Failed Downloads | No |
| POST | `/api/downloads` | Download | Yes |

### `health`
| Method | Path | Summary | Auth Required |
|---|---|---|---|
| GET | `/health` | Health Check | No |

### `network`
| Method | Path | Summary | Auth Required |
|---|---|---|---|
| GET | `/api/network` | Get Network | No |
| PATCH | `/api/network` | Update Network | Yes |

### `notifications`
| Method | Path | Summary | Auth Required |
|---|---|---|---|
| GET | `/api/notifications/{user_id}` | Get Notifications | No |
| PATCH | `/api/notifications/{notification_id}` | Mark Notification As Read | Yes |
| POST | `/api/notifications` | Create Notification | Yes |

### `playlists`
| Method | Path | Summary | Auth Required |
|---|---|---|---|
| GET | `/api/playlists` | List Playlists | No |
| POST | `/api/playlists` | Create New Playlist | No |

### `search`
| Method | Path | Summary | Auth Required |
|---|---|---|---|
| GET | `/api/search` | Search | No |

### `sync`
| Method | Path | Summary | Auth Required |
|---|---|---|---|
| POST | `/api/sync/trigger` | Trigger Sync | Yes |

### `system`
| Method | Path | Summary | Auth Required |
|---|---|---|---|
| GET | `/api/schema` | Get Schema | Yes |
| GET | `/api/system/env` | Get Env | Yes |
| GET | `/api/system/logs` | Get System Logs | Yes |
| GET | `/api/system/status` | Get System Status | Yes |
| GET | `/api/system/storage` | Get System Storage | Yes |
| GET | `/api/system/uptime` | Get Uptime | Yes |
| POST | `/api/system/logging/reload` | Reload Logging Config | Yes |
| POST | `/api/system/reload` | Reload System Config | Yes |
| POST | `/api/system/reset` | Reset System State | Yes |

### `tracks`
| Method | Path | Summary | Auth Required |
|---|---|---|---|
| DELETE | `/api/tracks/{track_id}` | Delete Track | Yes |
| GET | `/api/tracks/{track_id}/metadata` | Get extended metadata for a track | No |
| GET | `/api/tracks/{track_id}` | Get Track | No |
| GET | `/api/tracks` | List Tracks | No |
| PATCH | `/api/tracks/{track_id}/metadata` | Update extended metadata for a track | No |
| PATCH | `/api/tracks/{track_id}` | Update Track | Yes |
| POST | `/api/tracks/metadata` | Get Tracks Metadata | Yes |
| POST | `/api/tracks/{track_id}/cover` | Upload Track Cover | Yes |
| POST | `/api/tracks` | Create Track | Yes |

### `user`
| Method | Path | Summary | Auth Required |
|---|---|---|---|
| DELETE | `/api/user/history` | Delete User History | No |
| GET | `/api/user/history` | Get User History | No |
| GET | `/api/user/liked` | Get User Liked | No |
| GET | `/api/user/preferences` | Get User Preferences | No |
| GET | `/api/user/profile` | Get User Profile | No |
| PATCH | `/api/user/preferences` | Update User Preferences | No |
| PATCH | `/api/user/profile` | Update User Profile | No |
| POST | `/api/user/sync_liked` | Sync User Liked | No |

### `webhooks`
| Method | Path | Summary | Auth Required |
|---|---|---|---|
| DELETE | `/api/webhooks/{hook_id}` | Unregister Webhook | Yes |
| GET | `/api/webhooks` | List Webhooks | Yes |
| POST | `/api/webhooks/fire` | Fire Webhook | Yes |
| POST | `/api/webhooks/register` | Register Webhook | Yes |
