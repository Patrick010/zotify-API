# Project API Endpoints Reference

## Overview

This file lists all public API endpoints for the Zotify and Snitch projects. It provides high-level information for developers, operators, and auditors, linking to detailed documentation where necessary.

### Notes:

- All endpoints require authentication unless noted.
- Rate limits and auditing apply as documented per endpoint in the detailed guides.
- Always update this file when adding, modifying, or deprecating endpoints.

---

## Zotify API Endpoints

### Media Control
| Endpoint | Method | Path | Auth Required | Purpose | Notes / Links |
|---|---|---|---|---|---|
| Play Track | POST | `/api/media/play` | Yes | Play a track on the server | See [Developer Guide](../api/docs/manuals/DEVELOPER_GUIDE.md) |
| Pause Track | POST | `/api/media/pause` | Yes | Pause current playback | See [Developer Guide](../api/docs/manuals/DEVELOPER_GUIDE.md) |
| Get Queue | GET | `/api/media/queue` | Yes | Retrieve current playback queue | See [Full API Reference](../api/docs/reference/full_api_reference.md) |
| Add to Queue | POST | `/api/media/queue` | Yes | Add a track to playback queue | See [Developer Guide](../api/docs/manuals/DEVELOPER_GUIDE.md) |
| Skip Track | POST | `/api/media/skip` | Yes | Skip to next track | See [Developer Guide](../api/docs/manuals/DEVELOPER_GUIDE.md) |

### User Management
| Endpoint | Method | Path | Auth Required | Purpose | Notes / Links |
|---|---|---|---|---|---|
| Get User | GET | `/api/users/{id}` | Yes | Retrieve user information | See [Developer Guide](../api/docs/manuals/DEVELOPER_GUIDE.md) |
| Create User | POST | `/api/users` | Yes | Add a new user | Payload: `{name,email}` |
| Update User | PATCH | `/api/users/{id}` | Yes | Modify existing user data | See [Privacy Compliance](../api/docs/system/PRIVACY_COMPLIANCE.md) |
| Delete User | DELETE | `/api/users/{id}` | Yes | Remove a user | Audit logging required |

### Playlist / Library
| Endpoint | Method | Path | Auth Required | Purpose | Notes / Links |
|---|---|---|---|---|---|
| Get Playlists | GET | `/api/playlists` | Yes | List all user playlists | See [Full API Reference](../api/docs/reference/full_api_reference.md) |
| Create Playlist | POST | `/api/playlists` | Yes | Create new playlist | Requires payload: `{name,description}` |
| Add Track to Playlist | POST | `/api/playlists/{id}/tracks` | Yes | Add track(s) to playlist | Batch payload supported |

---

## Snitch API Endpoints

### OAuth / Authentication
| Endpoint | Method | Path | Auth Required | Purpose | Notes / Links |
|---|---|---|---|---|---|
| Start OAuth | GET | `/snitch/oauth/start` | No | Initiate OAuth flow | See [Secure Callback Design](../snitch/docs/PHASE_2_SECURE_CALLBACK.md) |
| Complete OAuth | POST | `/snitch/oauth/complete` | No | Complete OAuth callback | Returns access token, short-lived session |

### IPC / Event Tracking
| Endpoint | Method | Path | Auth Required | Purpose | Notes / Links |
|---|---|---|---|---|---|
| Send IPC Event | POST | `/snitch/ipc/event` | Yes | Submit IPC event to server | See [IPC Communication Doc](../snitch/docs/phase5-ipc.md) |
| Get Event Status | GET | `/snitch/ipc/status/{event_id}` | Yes | Retrieve status of submitted event | Audit-logged |

---

## Additional Notes

- All sensitive endpoints enforce RBAC and least-privilege policies.
- Privacy-sensitive endpoints are fully GDPR/CCPA compliant.
- Endpoint coverage in automated tests is tracked in `docs/snitch/TEST_RUNBOOK.md` and `project/reports/`.
- When adding a new endpoint:
    - Document here with method, path, auth, purpose, and links.
    - Update developer/operator guides as necessary.
    - Update automated tests and CI validation.
- This draft covers all currently known Zotify and Snitch endpoints. Maintaining it involves:
    - Adding new endpoints immediately.
    - Cross-linking to detailed docs.
    - Auditing periodically for deprecated or changed endpoints.
