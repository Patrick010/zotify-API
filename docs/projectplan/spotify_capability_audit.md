# Spotify Capability Audit

This document outlines the Spotify capabilities available through the Zotify stack and compares them to the features exposed by our API.

## Feature Matrix

| Spotify Feature      | Available in Spotify API | Covered by Librespot | Used by Zotify | Exposed in our API | Notes                                                                                             |
| -------------------- | ------------------------ | -------------------- | -------------- | ------------------ | ------------------------------------------------------------------------------------------------- |
| **Authentication**   | ✅                       | ✅                   | ✅             | ✅                 | Zotify uses Librespot's OAuth implementation. Our API has stubs for the OAuth flow.               |
| **Playback Control** | ✅                       | ✅                   | ❌             | ❌                 | Librespot supports playback control, but Zotify does not use it.                                    |
| **Search**           | ✅                       | ❌                   | ✅             | ✅ (stub)          | Zotify uses the Spotify Web API for search. Our API has a stub for search.                        |
| **User Profile**     | ✅                       | ✅                   | ✅             | ✅                 | Zotify uses the Spotify Web API to get the user's profile. Our API has a user profile endpoint.   |
| **Audio Analysis**   | ✅                       | ❌                   | ❌             | ❌                 | Not used by Zotify.                                                                               |
| **Playlists**        | ✅                       | ✅                   | ✅             | ✅                 | Zotify uses the Spotify Web API for playlist management. Our API has playlist management endpoints. |
| **Device Switching** | ✅                       | ✅                   | ❌             | ❌                 | Librespot supports device switching, but Zotify does not use it.                                    |
| **Audio Streaming**  | ❌                       | ✅                   | ✅             | ❌                 | Zotify uses Librespot's `content_feeder` to download audio streams. Our API does not expose this. |

## Investigation Queries

**What Spotify authentication or session context does Librespot/Zotify use?**

Zotify uses `librespot`'s OAuth implementation to authenticate with Spotify. It can either use a refresh token or an interactive login flow.

**Does Zotify expose playback state? Queue state? Device state?**

No, Zotify does not expose any of these features.

**Which Librespot modules are actively used by Zotify?**

Zotify primarily uses the `content_feeder` for audio streaming and the OAuth implementation for authentication.

**What are the current API endpoints related to Spotify functionality in our own stack?**

Our API currently has the following Spotify-related endpoints:
- `GET /spotify/login`
- `GET /spotify/callback`
- `GET /spotify/token_status`
- `POST /spotify/sync_playlists` (admin-only)
- `GET /spotify/metadata/{track_id}`
- Stubs for playlist management

**Are there Spotify Web API features that are not feasible through Librespot?**

Yes, Librespot does not cover all the features of the Spotify Web API. For example, it does not have a search feature.

**What functionality does Zotify intentionally leave out or override?**

Zotify does not seem to intentionally leave out or override any functionality. It uses `librespot` for what it's good at (authentication and audio streaming) and the Spotify Web API for everything else.

**Does the current API surface reflect user needs or internal convenience?**

The current API surface is a mix of both. The Spotify-related endpoints are mostly stubs that were created for internal convenience. The other endpoints, such as user and playlist management, are more user-focused.

## Architectural and Functional Consequences

The current implementation has the following consequences:

*   **Limited Spotify Integration:** Our API's Spotify integration is very limited. We are not exposing many of the features that are available through Zotify and Librespot.
*   **Inconsistent API Surface:** The API surface is inconsistent, with some endpoints being well-developed and others being stubs.
*   **Lack of Playback Control:** The lack of playback control means that our API cannot be used to build a full-featured Spotify client.

## Integration Plans

To address these issues, we need to create a plan for integrating the remaining Spotify features into our API. This will involve:

*   **Implementing Playback Control:** We need to add endpoints for controlling playback, such as play, pause, next, and previous.
*   **Implementing Device Switching:** We need to add endpoints for switching playback between different devices.
*   **Implementing Audio Streaming:** We need to decide if we want to expose audio streaming through our API. This would be a major undertaking, but it would allow us to build a full-featured Spotify client.
*   **Completing the Playlist Management Endpoints:** We need to complete the implementation of the playlist management endpoints.
*   **Improving the Search Endpoint:** We need to improve the search endpoint to provide more accurate and complete results.

## Exclusions

For now, we will exclude the following features from our API:

*   **Audio Analysis:** This is a niche feature that is not essential for our core use case.
*   **Other non-essential features:** We will focus on implementing the core Spotify features first and then consider adding other features in the future.
