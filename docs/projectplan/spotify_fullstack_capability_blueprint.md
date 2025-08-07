# Spotify Integration Blueprint

This document provides a comprehensive blueprint for the Zotify API's integration with Spotify. It expands on the initial [Spotify Capability Audit](./spotify_capability_audit.md) and serves as the definitive guide for all future development work related to Spotify.

## 1. Expanded Feature Matrix

### 1.1. Spotify Web API Capabilities

| Capability          | Description                                       | Endpoint (Example)              | Auth Scope Required         | Known Limitations                               | Relevance to Zotify | Implemented | Target API Endpoint               |
| ------------------- | ------------------------------------------------- | ------------------------------- | --------------------------- | ----------------------------------------------- | ------------------- | ----------- | --------------------------------- |
| **Albums**          | Get album data.                                   | `GET /v1/albums/{id}`           | -                           | -                                               | High                | 🟡          | `GET /spotify/albums/{id}`        |
| **Artists**         | Get artist data.                                  | `GET /v1/artists/{id}`          | -                           | -                                               | High                | 🟡          | `GET /spotify/artists/{id}`       |
| **Tracks**          | Get track data.                                   | `GET /v1/tracks/{id}`           | -                           | -                                               | High                | ✅          | `GET /spotify/metadata/{track_id}` |
| **Search**          | Search for items on Spotify.                      | `GET /v1/search`                | -                           | -                                               | High                | ✅ (stub)   | `GET /search`                     |
| **User Profile**    | Get user profile data.                            | `GET /v1/me`                    | `user-read-private`         | -                                               | High                | ✅          | `GET /user/profile`               |
| **Playlists**       | Manage playlists.                                 | `GET /v1/me/playlists`          | `playlist-read-private`     | -                                               | High                | ✅          | `GET /playlists`                  |
| **Player**          | Control playback.                                 | `PUT /v1/me/player/play`        | `user-modify-playback-state` | Requires an active device.                      | High                | ❌          | `POST /spotify/player/play`       |
| **Shows**           | Get show data.                                    | `GET /v1/shows/{id}`            | -                           | -                                               | Medium              | ❌          | `GET /spotify/shows/{id}`         |
| **Episodes**        | Get episode data.                                 | `GET /v1/episodes/{id}`         | -                           | -                                               | Medium              | ❌          | `GET /spotify/episodes/{id}`      |
| **Audiobooks**      | Get audiobook data.                               | `GET /v1/audiobooks/{id}`       | -                           | -                                               | Medium              | ❌          | `GET /spotify/audiobooks/{id}`    |
| **Categories**      | Get browse categories.                            | `GET /v1/browse/categories`     | -                           | -                                               | Low                 | ❌          | -                                 |
| **Genres**          | Get available genre seeds.                        | `GET /v1/recommendations/available-genre-seeds` | -                           | -                                               | Low                 | ❌          | -                                 |
| **Markets**         | Get available markets.                            | `GET /v1/markets`               | -                           | -                                               | Low                 | ❌          | -                                 |
| **Player (Queue)**  | Add an item to the user's playback queue.         | `POST /v1/me/player/queue`      | `user-modify-playback-state` | -                                               | High                | ❌          | `POST /spotify/player/queue`      |
| **Follow**          | Manage user's followed artists and users.         | `PUT /v1/me/following`          | `user-follow-modify`        | -                                               | Medium              | ❌          | `POST /spotify/me/following`      |
| **Library**         | Manage user's saved tracks, albums, and shows.    | `PUT /v1/me/tracks`             | `user-library-modify`       | -                                               | High                | ✅          | `POST /user/sync_liked`           |

### 1.2. Librespot Capabilities

| Name | Description | Known limitations | Relevance to Zotify | Target API Endpoint | Implementation status |
| --- | --- | --- | --- | --- | --- |
| **Authentication** | Handles authentication with Spotify's backend using credentials. | Requires Spotify Premium. Does not support free-tier accounts. | High | `/librespot/auth` (internal) | ✅ |
| **Audio Streaming** | Fetches and decrypts raw audio data from Spotify's CDN. | Does not handle encoding to MP3/AAC; requires external library. | High | `/downloads` (existing) | ✅ |
| **Content Fetching** | Retrieves metadata for tracks, albums, playlists via Mercury. | Less comprehensive than Web API for some metadata types. | High | `/spotify/metadata` (internal) | ✅ |
| **Playback Control** | Manages a virtual player state (play, pause, seek). | Does not output audio directly; manages stream for download. | High | `/librespot/player/{action}` | ❌ |
| **Device Control** | Emulates a Spotify Connect device to be discoverable on the network. | Can be unstable; may not be detected by all Spotify clients. | Medium | `/librespot/device` | ❌ |
| **Session Management**| Manages the active user session and connection to Spotify. | Internal to Zotify's core operations. | High | N/A (internal only) | ✅ |
| **Caching** | Provides mechanisms for caching credentials and audio files. | Zotify implements its own caching logic on top. | High | N/A (internal only) | 🟡 |

### 1.3. Zotify Platform (Current vs. Planned)

| Feature                               | Current Status | Planned Status | Notes                                                                                                                                                              |
| ------------------------------------- | -------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Search for tracks, albums, etc.**   | ✅ (stub)      | ✅             | The current implementation is a stub. The planned implementation will use the Spotify Web API.                                                                     |
| **Download tracks, albums, etc.**     | ✅             | ✅             | Zotify uses Librespot for this.                                                                                                                                    |
| **Manage playlists**                  | ✅             | ✅             | Zotify uses the Spotify Web API for this.                                                                                                                          |
| **Manage user profile & preferences** | ✅             | ✅             | This is a Zotify-specific feature.                                                                                                                                 |
| **Manage notifications**              | ✅             | ✅             | This is a Zotify-specific feature.                                                                                                                                 |
| **Control playback**                  | ❌             | ✅             | This will be implemented using Librespot.                                                                                                                          |
| **Manage devices**                    | ❌             | ✅             | This will be implemented using Librespot.                                                                                                                          |
| **Audio streaming via API**           | ❌             | 🟡             | This is a major undertaking that will be considered in a future phase.                                                                                             |

---

## 2. Exhaustive Spotify Web API Endpoint Mapping

### Albums

| Spotify Endpoint                | Auth Scope Required | Relevant Use Case(s)                                   | Zotify Internal Mapping (planned/implemented) | Target Zotify External API Endpoint | Required Modules       | Feasibility Notes                                                                 |
| ------------------------------- | ------------------- | ------------------------------------------------------ | --------------------------------------------- | ----------------------------------- | ---------------------- | --------------------------------------------------------------------------------- |
| `GET /v1/albums/{id}`           | -                   | Get an album's metadata.                               | 🟡                                            | `GET /spotify/albums/{id}`          | Spotify Web API        | -                                                                                 |
| `GET /v1/albums`                | -                   | Get several albums' metadata.                          | 🟡                                            | `GET /spotify/albums`               | Spotify Web API        | -                                                                                 |
| `GET /v1/albums/{id}/tracks`    | -                   | Get an album's tracks.                                 | 🟡                                            | `GET /spotify/albums/{id}/tracks`   | Spotify Web API        | -                                                                                 |
| `GET /v1/me/albums`             | `user-library-read` | Get the current user's saved albums.                   | ✅                                            | `GET /user/library/albums`            | Spotify Web API        | -                                                                                 |
| `PUT /v1/me/albums`             | `user-library-modify` | Save one or more albums to the current user's library. | 🟡                                            | `PUT /user/library/albums`            | Spotify Web API        | -                                                                                 |
| `DELETE /v1/me/albums`          | `user-library-modify` | Remove one or more albums from the current user's library. | 🟡                                            | `DELETE /user/library/albums`         | Spotify Web API        | -                                                                                 |
| `GET /v1/me/albums/contains`    | `user-library-read` | Check if one or more albums is already saved in the current user's library. | 🟡                                            | `GET /user/library/albums/contains`   | Spotify Web API        | -                                                                                 |
| `GET /v1/new-releases`          | -                   | Get a list of new album releases featured in Spotify.  | ❌                                            | -                                   | Spotify Web API        | Low relevance to Zotify's core use case.                                          |

### Artists

| Spotify Endpoint                    | Auth Scope Required | Relevant Use Case(s)                                       | Zotify Internal Mapping (planned/implemented) | Target Zotify External API Endpoint     | Required Modules       | Feasibility Notes |
| ----------------------------------- | ------------------- | ---------------------------------------------------------- | --------------------------------------------- | --------------------------------------- | ---------------------- | ----------------- |
| `GET /v1/artists/{id}`              | -                   | Get an artist's metadata.                                  | 🟡                                            | `GET /spotify/artists/{id}`             | Spotify Web API        | -                 |
| `GET /v1/artists`                   | -                   | Get several artists' metadata.                             | 🟡                                            | `GET /spotify/artists`                  | Spotify Web API        | -                 |
| `GET /v1/artists/{id}/albums`       | -                   | Get an artist's albums.                                    | 🟡                                            | `GET /spotify/artists/{id}/albums`      | Spotify Web API        | -                 |
| `GET /v1/artists/{id}/top-tracks`   | -                   | Get an artist's top tracks.                                | 🟡                                            | `GET /spotify/artists/{id}/top-tracks`  | Spotify Web API        | -                 |
| `GET /v1/artists/{id}/related-artists`| -                   | Get artists similar to an artist.                          | ❌                                            | -                                       | Spotify Web API        | Low relevance.    |

### Audiobooks

| Spotify Endpoint                | Auth Scope Required | Relevant Use Case(s)                                   | Zotify Internal Mapping (planned/implemented) | Target Zotify External API Endpoint | Required Modules       | Feasibility Notes |
| ------------------------------- | ------------------- | ------------------------------------------------------ | --------------------------------------------- | ----------------------------------- | ---------------------- | ----------------- |
| `GET /v1/audiobooks/{id}`       | -                   | Get an audiobook's metadata.                           | ❌                                            | `GET /spotify/audiobooks/{id}`      | Spotify Web API        | Medium relevance. |
| `GET /v1/audiobooks`            | -                   | Get several audiobooks' metadata.                      | ❌                                            | `GET /spotify/audiobooks`           | Spotify Web API        | Medium relevance. |
| `GET /v1/audiobooks/{id}/chapters` | -                | Get an audiobook's chapters.                           | ❌                                            | `GET /spotify/audiobooks/{id}/chapters` | Spotify Web API      | Medium relevance. |
| `GET /v1/me/audiobooks`         | `user-library-read` | Get the current user's saved audiobooks.               | ❌                                            | `GET /user/library/audiobooks`      | Spotify Web API        | Low relevance.    |
| `PUT /v1/me/audiobooks`         | `user-library-modify`| Save audiobooks for the current user.                  | ❌                                            | `PUT /user/library/audiobooks`      | Spotify Web API        | Low relevance.    |
| `DELETE /v1/me/audiobooks`      | `user-library-modify`| Remove user's saved audiobooks.                        | ❌                                            | `DELETE /user/library/audiobooks`   | Spotify Web API        | Low relevance.    |
| `GET /v1/me/audiobooks/contains`| `user-library-read` | Check user's saved audiobooks.                         | ❌                                            | `GET /user/library/audiobooks/contains` | Spotify Web API    | Low relevance.    |

### Categories

| Spotify Endpoint                | Auth Scope Required | Relevant Use Case(s)                                   | Zotify Internal Mapping (planned/implemented) | Target Zotify External API Endpoint | Required Modules       | Feasibility Notes |
| ------------------------------- | ------------------- | ------------------------------------------------------ | --------------------------------------------- | ----------------------------------- | ---------------------- | ----------------- |
| `GET /v1/browse/categories`     | -                   | Get a list of categories.                              | ❌                                            | -                                   | Spotify Web API        | Low relevance.    |
| `GET /v1/browse/categories/{id}`| -                   | Get a single browse category.                          | ❌                                            | -                                   | Spotify Web API        | Low relevance.    |

### Chapters

| Spotify Endpoint                | Auth Scope Required | Relevant Use Case(s)                                   | Zotify Internal Mapping (planned/implemented) | Target Zotify External API Endpoint | Required Modules       | Feasibility Notes |
| ------------------------------- | ------------------- | ------------------------------------------------------ | --------------------------------------------- | ----------------------------------- | ---------------------- | ----------------- |
| `GET /v1/chapters/{id}`         | -                   | Get a chapter's metadata.                              | ❌                                            | `GET /spotify/chapters/{id}`        | Spotify Web API        | Medium relevance. |
| `GET /v1/chapters`              | -                   | Get several chapters' metadata.                        | ❌                                            | `GET /spotify/chapters`             | Spotify Web API        | Medium relevance. |

### Episodes

| Spotify Endpoint                | Auth Scope Required | Relevant Use Case(s)                                   | Zotify Internal Mapping (planned/implemented) | Target Zotify External API Endpoint | Required Modules       | Feasibility Notes |
| ------------------------------- | ------------------- | ------------------------------------------------------ | --------------------------------------------- | ----------------------------------- | ---------------------- | ----------------- |
| `GET /v1/episodes/{id}`         | -                   | Get an episode's metadata.                             | ❌                                            | `GET /spotify/episodes/{id}`        | Spotify Web API        | Medium relevance. |
| `GET /v1/episodes`              | -                   | Get several episodes' metadata.                        | ❌                                            | `GET /spotify/episodes`             | Spotify Web API        | Medium relevance. |
| `GET /v1/me/episodes`           | `user-library-read` | Get the current user's saved episodes.                 | ❌                                            | `GET /user/library/episodes`        | Spotify Web API        | Low relevance.    |
| `PUT /v1/me/episodes`           | `user-library-modify`| Save episodes for the current user.                    | ❌                                            | `PUT /user/library/episodes`        | Spotify Web API        | Low relevance.    |
| `DELETE /v1/me/episodes`        | `user-library-modify`| Remove user's saved episodes.                          | ❌                                            | `DELETE /user/library/episodes`     | Spotify Web API        | Low relevance.    |
| `GET /v1/me/episodes/contains`  | `user-library-read` | Check user's saved episodes.                           | ❌                                            | `GET /user/library/episodes/contains` | Spotify Web API    | Low relevance.    |

### Genres

| Spotify Endpoint                  | Auth Scope Required | Relevant Use Case(s)             | Zotify Internal Mapping (planned/implemented) | Target Zotify External API Endpoint | Required Modules | Feasibility Notes |
| --------------------------------- | ------------------- | -------------------------------- | --------------------------------------------- | ----------------------------------- | ---------------- | ----------------- |
| `GET /v1/recommendations/available-genre-seeds` | -       | Get available genre seeds.       | ❌                                            | -                                   | Spotify Web API  | Low relevance.    |

### Markets

| Spotify Endpoint    | Auth Scope Required | Relevant Use Case(s)     | Zotify Internal Mapping (planned/implemented) | Target Zotify External API Endpoint | Required Modules | Feasibility Notes |
| ------------------- | ------------------- | ------------------------ | --------------------------------------------- | ----------------------------------- | ---------------- | ----------------- |
| `GET /v1/markets`   | -                   | Get available markets.   | ❌                                            | -                                   | Spotify Web API  | Low relevance.    |

### Player

| Spotify Endpoint                | Auth Scope Required | Relevant Use Case(s)                                   | Zotify Internal Mapping (planned/implemented) | Target Zotify External API Endpoint | Required Modules       | Feasibility Notes |
| ------------------------------- | ------------------- | ------------------------------------------------------ | --------------------------------------------- | ----------------------------------- | ---------------------- | ----------------- |
| `GET /v1/me/player`             | `user-read-playback-state` | Get the user's current playback state.                 | ❌                                            | `GET /spotify/player`            | Spotify Web API        | Requires active device. |
| `PUT /v1/me/player`             | `user-modify-playback-state` | Transfer playback to a new device.                     | ❌                                            | `PUT /spotify/player`            | Spotify Web API        | Requires active device. |
| `GET /v1/me/player/devices`     | `user-read-playback-state` | Get a user's available devices.                        | ❌                                            | `GET /spotify/player/devices`    | Spotify Web API        | -                 |
| `GET /v1/me/player/currently-playing` | `user-read-currently-playing` | Get the user's currently playing track.                | ❌                                            | `GET /spotify/player/currently-playing` | Spotify Web API      | -                 |
| `PUT /v1/me/player/play`        | `user-modify-playback-state` | Start or resume playback.                              | ❌                                            | `PUT /spotify/player/play`       | Spotify Web API        | Requires active device. |
| `PUT /v1/me/player/pause`       | `user-modify-playback-state` | Pause playback.                                        | ❌                                            | `PUT /spotify/player/pause`      | Spotify Web API        | Requires active device. |
| `POST /v1/me/player/next`       | `user-modify-playback-state` | Skip to the next track.                                | ❌                                            | `POST /spotify/player/next`      | Spotify Web API        | Requires active device. |
| `POST /v1/me/player/previous`   | `user-modify-playback-state` | Skip to the previous track.                            | ❌                                            | `POST /spotify/player/previous`  | Spotify Web API        | Requires active device. |
| `PUT /v1/me/player/seek`        | `user-modify-playback-state` | Seek to a position in the current track.               | ❌                                            | `PUT /spotify/player/seek`       | Spotify Web API        | Requires active device. |
| `PUT /v1/me/player/repeat`      | `user-modify-playback-state` | Set the repeat mode.                                   | ❌                                            | `PUT /spotify/player/repeat`     | Spotify Web API        | Requires active device. |
| `PUT /v1/me/player/volume`      | `user-modify-playback-state` | Set the volume.                                        | ❌                                            | `PUT /spotify/player/volume`     | Spotify Web API        | Requires active device. |
| `PUT /v1/me/player/shuffle`     | `user-modify-playback-state` | Toggle shuffle.                                        | ❌                                            | `PUT /spotify/player/shuffle`    | Spotify Web API        | Requires active device. |
| `GET /v1/me/player/recently-played` | `user-read-recently-played` | Get the user's recently played tracks.                 | 🟡                                            | `GET /user/player/recently-played` | Spotify Web API      | -                 |
| `GET /v1/me/player/queue`       | `user-read-playback-state` | Get the contents of the user's queue.                  | ❌                                            | `GET /spotify/player/queue`      | Spotify Web API        | Requires active device. |
| `POST /v1/me/player/queue`      | `user-modify-playback-state` | Add an item to the user's playback queue.              | ❌                                            | `POST /spotify/player/queue`     | Spotify Web API        | Requires active device. |

### Playlists

| Spotify Endpoint                | Auth Scope Required | Relevant Use Case(s)                                   | Zotify Internal Mapping (planned/implemented) | Target Zotify External API Endpoint | Required Modules       | Feasibility Notes |
| ------------------------------- | ------------------- | ------------------------------------------------------ | --------------------------------------------- | ----------------------------------- | ---------------------- | ----------------- |
| `GET /v1/playlists/{playlist_id}` | `playlist-read-private` | Get a playlist's details.                              | ✅                                            | `GET /playlists/{playlist_id}` | Spotify Web API        | -                 |
| `PUT /v1/playlists/{playlist_id}` | `playlist-modify-public`, `playlist-modify-private` | Change a playlist's name, description, and public status. | ✅                                            | `PUT /playlists/{playlist_id}` | Spotify Web API        | -                 |
| `GET /v1/playlists/{playlist_id}/tracks` | `playlist-read-private` | Get a playlist's items. | ✅ | `GET /playlists/{playlist_id}/tracks` | Spotify Web API | - |
| `POST /v1/playlists/{playlist_id}/tracks` | `playlist-modify-public`, `playlist-modify-private` | Add one or more items to a playlist.                   | ✅                                            | `POST /playlists/{playlist_id}/tracks` | Spotify Web API        | -                 |
| `PUT /v1/playlists/{playlist_id}/tracks` | `playlist-modify-public`, `playlist-modify-private` | Reorder or replace a playlist's items.                 | ✅                                            | `PUT /playlists/{playlist_id}/tracks` | Spotify Web API        | -                 |
| `DELETE /v1/playlists/{playlist_id}/tracks` | `playlist-modify-public`, `playlist-modify-private` | Remove one or more items from a playlist.              | ✅                                            | `DELETE /playlists/{playlist_id}/tracks` | Spotify Web API        | -                 |
| `GET /v1/me/playlists`          | `playlist-read-private` | Get a list of the current user's playlists.            | ✅                                            | `GET /user/playlists`         | Spotify Web API        | -                 |
| `GET /v1/users/{user_id}/playlists` | `playlist-read-private` | Get a list of a user's playlists.                      | ✅                                            | `GET /users/{user_id}/playlists` | Spotify Web API        | -                 |
| `POST /v1/users/{user_id}/playlists` | `playlist-modify-public`, `playlist-modify-private` | Create a new playlist.                                 | ✅                                            | `POST /users/{user_id}/playlists` | Spotify Web API        | -                 |
| `GET /v1/browse/featured-playlists` | -                   | Get a list of featured playlists.                      | ❌                                            | -                                   | Spotify Web API        | Low relevance.    |
| `GET /v1/browse/categories/{category_id}/playlists` | -                   | Get a list of playlists for a specific category.       | ❌                                            | -                                   | Spotify Web API        | Low relevance.    |
| `GET /v1/playlists/{playlist_id}/images` | -                   | Get the cover image for a playlist.                    | 🟡                                            | `GET /playlists/{playlist_id}/images` | Spotify Web API        | -    |
| `PUT /v1/playlists/{playlist_id}/images` | `ugc-image-upload`, `playlist-modify-public`, `playlist-modify-private` | Upload a custom playlist cover image.                  | ❌                                            | -                                   | Spotify Web API        | Low relevance.    |

### Search

| Spotify Endpoint                | Auth Scope Required | Relevant Use Case(s)                                   | Zotify Internal Mapping (planned/implemented) | Target Zotify External API Endpoint | Required Modules       | Feasibility Notes |
| ------------------------------- | ------------------- | ------------------------------------------------------ | --------------------------------------------- | ----------------------------------- | ---------------------- | ----------------- |
| `GET /v1/search`                | -                   | Search for an item.                                    | ✅ (stub)                                     | `GET /search`               | Spotify Web API        | -                 |

### Shows

| Spotify Endpoint                | Auth Scope Required | Relevant Use Case(s)                                   | Zotify Internal Mapping (planned/implemented) | Target Zotify External API Endpoint | Required Modules       | Feasibility Notes |
| ------------------------------- | ------------------- | ------------------------------------------------------ | --------------------------------------------- | ----------------------------------- | ---------------------- | ----------------- |
| `GET /v1/shows/{id}`            | -                   | Get a show's metadata.                                 | ❌                                            | `GET /spotify/shows/{id}`           | Spotify Web API        | Medium relevance. |
| `GET /v1/shows`                 | -                   | Get several shows' metadata.                           | ❌                                            | `GET /spotify/shows`                | Spotify Web API        | Medium relevance. |
| `GET /v1/shows/{id}/episodes`   | -                   | Get a show's episodes.                                 | ❌                                            | `GET /spotify/shows/{id}/episodes`  | Spotify Web API        | Medium relevance. |
| `GET /v1/me/shows`              | `user-library-read` | Get the current user's saved shows.                    | ❌                                            | `GET /user/library/shows`           | Spotify Web API        | Low relevance.    |
| `PUT /v1/me/shows`              | `user-library-modify`| Save shows for the current user.                       | ❌                                            | `PUT /user/library/shows`           | Spotify Web API        | Low relevance.    |
| `DELETE /v1/me/shows`           | `user-library-modify`| Remove user's saved shows.                             | ❌                                            | `DELETE /user/library/shows`        | Spotify Web API        | Low relevance.    |
| `GET /v1/me/shows/contains`     | `user-library-read` | Check user's saved shows.                              | ❌                                            | `GET /user/library/shows/contains`  | Spotify Web API        | Low relevance.    |

### Tracks

| Spotify Endpoint                | Auth Scope Required | Relevant Use Case(s)                                   | Zotify Internal Mapping (planned/implemented) | Target Zotify External API Endpoint | Required Modules       | Feasibility Notes |
| ------------------------------- | ------------------- | ------------------------------------------------------ | --------------------------------------------- | ----------------------------------- | ---------------------- | ----------------- |
| `GET /v1/tracks/{id}`           | -                   | Get a track's metadata.                                | ✅                                            | `GET /spotify/tracks/{id}`          | Spotify Web API        | -                 |
| `GET /v1/tracks`                | -                   | Get several tracks' metadata.                          | ✅                                            | `GET /spotify/tracks`               | Spotify Web API        | -                 |
| `GET /v1/me/tracks`             | `user-library-read` | Get the current user's saved tracks.                   | ✅                                            | `GET /user/library/tracks`            | Spotify Web API        | Core Zotify feature. |
| `PUT /v1/me/tracks`             | `user-library-modify` | Save one or more tracks to the current user's library. | ✅                                            | `PUT /user/library/tracks`            | Spotify Web API        | Core Zotify feature. |
| `DELETE /v1/me/tracks`          | `user-library-modify` | Remove one or more tracks from the current user's library. | ✅                                            | `DELETE /user/library/tracks`         | Spotify Web API        | Core Zotify feature. |
| `GET /v1/me/tracks/contains`    | `user-library-read` | Check if one or more tracks is already saved in the current user's library. | ✅                                            | `GET /user/library/tracks/contains`   | Spotify Web API        | Core Zotify feature. |
| `GET /v1/audio-features/{id}`   | -                   | Get audio features for a track.                        | ❌                                            | -                                   | Spotify Web API        | Low relevance.    |
| `GET /v1/audio-features`        | -                   | Get audio features for several tracks.                 | ❌                                            | -                                   | Spotify Web API        | Low relevance.    |
| `GET /v1/audio-analysis/{id}`   | -                   | Get a detailed audio analysis for a track.             | ❌                                            | -                                   | Spotify Web API        | Low relevance.    |
| `GET /v1/recommendations`       | -                   | Get recommendations based on seeds.                    | ❌                                            | -                                   | Spotify Web API        | Low relevance.    |

### Users

| Spotify Endpoint                | Auth Scope Required | Relevant Use Case(s)                                   | Zotify Internal Mapping (planned/implemented) | Target Zotify External API Endpoint | Required Modules       | Feasibility Notes |
| ------------------------------- | ------------------- | ------------------------------------------------------ | --------------------------------------------- | ----------------------------------- | ---------------------- | ----------------- |
| `GET /v1/me`                    | `user-read-private`, `user-read-email` | Get the current user's profile.                        | ✅                                            | `GET /user/profile`                   | Spotify Web API        | -                 |
| `GET /v1/users/{user_id}`       | -                   | Get a user's public profile.                           | ✅                                            | `GET /users/{user_id}/profile`      | Spotify Web API        | -                 |
| `GET /v1/me/top/{type}`         | `user-top-read`     | Get the user's top artists or tracks.                  | 🟡                                            | `GET /user/top/{type}`           | Spotify Web API        | -                 |
| `GET /v1/me/following`          | `user-follow-read`  | Get the user's followed artists.                       | 🟡                                            | `GET /user/following`         | Spotify Web API        | -                 |
| `PUT /v1/me/following`          | `user-follow-modify`| Follow artists or users.                               | 🟡                                            | `PUT /user/following`         | Spotify Web API        | -                 |
| `DELETE /v1/me/following`       | `user-follow-modify`| Unfollow artists or users.                             | 🟡                                            | `DELETE /user/following`      | Spotify Web API        | -                 |
| `GET /v1/me/following/contains` | `user-follow-read`  | Check if the user follows artists or users.            | 🟡                                            | `GET /user/following/contains`| Spotify Web API        | -                 |
| `GET /v1/playlists/{id}/followers/contains` | `playlist-read-private` | Check if users follow a playlist. | ❌ | - | Spotify Web API | Low relevance. |
| `PUT /v1/playlists/{id}/followers` | `playlist-modify-public` | Follow a playlist. | 🟡 | `PUT /playlists/{id}/followers` | Spotify Web API | - |
| `DELETE /v1/playlists/{id}/followers` | `playlist-modify-public` | Unfollow a playlist. | 🟡 | `DELETE /playlists/{id}/followers` | Spotify Web API | - |

---

## 3. Librespot Module Breakdown

| Name | Purpose | Zotify Usage (Y/N) | Exposure plan (Y/N) | API Endpoint (if relevant) |
| --- | --- | --- | --- | --- |
| **Auth/Session** | Handles the initial authentication handshake and manages the session lifecycle. | Y | N | N/A (Internal) |
| **Audio Streaming** | Fetches raw, encrypted audio chunks from Spotify's CDN. This is the core of Zotify's download functionality. | Y | Y | `POST /downloads` |
| **Content Fetching** | Uses the internal Mercury protocol to fetch metadata for tracks, albums, and playlists. | Y | N | N/A (Internal, superseded by Web API for external exposure) |
| **Playback** | Simulates a player to enable audio streaming. Can report playback events (e.g., track played). | Y | Y | `POST /librespot/player/event` |
| **Device Control** | Emulates a Spotify Connect device, allowing Zotify to be controlled by other Spotify clients. | N | Y | `POST /librespot/device/command` |
| **Caching/Buffering** | Manages caching of credentials, metadata, and audio files to reduce redundant requests. | Y | N | N/A (Internal) |

---

## 4. Planned API Feature List (with Use Cases)

### Feature: Advanced Search & Metadata Proxy

*   **Description**: Provide a unified search endpoint that proxies Spotify's search capabilities and enriches results with Zotify-specific data (e.g., download availability). Expose direct metadata lookups for all Spotify object types.
*   **Target User Type**: Developer, End-user
*   **APIs Involved**: Spotify Web API, Zotify Internal
*   **Concrete Use Cases**:
    *   A mobile client uses `/search?q=...` to find a track and immediately see if it's available for download.
    *   A script uses `/spotify/tracks/{id}` to fetch official metadata for a locally stored file.
    *   An admin tool queries `/spotify/artists/{id}/albums` to check for new releases from a specific artist.

### Feature: Comprehensive Library Management

*   **Description**: Allow full two-way synchronization of a user's Spotify library, including saved tracks, albums, playlists, and followed artists.
*   **Target User Type**: End-user, Developer
*   **APIs Involved**: Spotify Web API, Zotify Internal
*   **Concrete Use Cases**:
    *   An end-user clicks a "Sync Library" button in the Zotify UI, which calls `POST /user/sync` to pull all their latest liked songs from Spotify.
    *   A developer builds a tool that automatically adds any track downloaded via Zotify to the user's Spotify library by calling `PUT /user/library/tracks`.
    *   A user can manage their playlists directly through Zotify's API, with changes reflected back to Spotify.

### Feature: Librespot-Powered Download Control

*   **Description**: Expose fine-grained control over the Librespot download queue. Allow programmatic starting, stopping, and monitoring of track/album/playlist downloads.
*   **Target User Type**: Developer, Admin
*   **APIs Involved**: Librespot, Zotify Internal
*   **Concrete Use Cases**:
    *   A developer creates a "download manager" UI that shows real-time progress of downloads via a WebSocket connection.
    *   An admin script queues up a large batch of playlists for download by hitting `POST /downloads` with a list of Spotify URIs.
    *   A user can set download quality and format preferences via `PUT /downloads/config`.

### Feature: Real-time Player & Device Emulation

*   **Description**: Expose Librespot's Spotify Connect capabilities, allowing Zotify to appear as a valid playback device and receive commands from the official Spotify app. Provide endpoints to control this virtual player.
*   **Target User Type**: End-user, Developer
*   **APIs Involved**: Librespot, Zotify Internal (potentially WebSockets)
*   **Concrete Use Cases**:
    *   An end-user opens their Spotify app, selects "Zotify" from the device list, and hits play. Zotify begins downloading the track.
    *   A developer builds a custom hardware device (e.g., a smart speaker) that uses the Zotify API to become a Spotify Connect target.
    *   A script can pause or resume the virtual player by calling `PUT /librespot/player/pause`.

### Feature: Webhook & Notification System

*   **Description**: Allow developers to subscribe to events within the Zotify ecosystem, such as download completion, metadata changes, or player state changes.
*   **Target User Type**: Developer
*   **APIs Involved**: Zotify Internal
*   **Concrete Use Cases**:
    *   A developer registers a webhook at `POST /webhooks` to receive a notification whenever a download finishes.
    *   A media server application (like Plex) listens for "track downloaded" events to trigger a library scan.
    *   A user receives a push notification on their phone when a new episode of a followed podcast is downloaded.

---

## 5. Creative Use Case Inventory

*   **Automated Music Archiving**: A script runs nightly, checks the user's "Liked Songs" and "Discover Weekly" playlists, and automatically downloads any new tracks that haven't been downloaded before.
*   **YouTube-to-Spotify Playlist Conversion**: A tool that accepts a YouTube playlist URL, uses a third-party service to identify the tracks, finds them on Spotify using the `/search` endpoint, creates a new Spotify playlist via `POST /users/{user_id}/playlists`, and then queues it for download in Zotify.
*   **Smart Playlist Generator**: A service that creates a new playlist daily by combining the user's top 10 tracks from the last month (`GET /me/top/tracks`) with 10 recommended tracks based on those seeds (`GET /recommendations`).
*   **Plex/Jellyfin Integration**: A companion service that listens for "download complete" webhooks from Zotify and then uses the Plex/Jellyfin APIs to trigger a library scan, ensuring new music is available immediately.
*   **Public Metadata API**: A self-hosted instance of Zotify could expose a public, read-only API for track/album metadata, allowing developers to build music-related websites or bots without requiring their own Spotify API keys.
*   **Advanced Download Rules**: A UI that allows users to set up complex download rules, such as "Download any song by Artist X, but only if the album has a rating of 4 stars or higher on Metacritic," which would involve Zotify calling external APIs for enrichment.
*   **Collaborative Playlist Queue**: A web app that uses WebSockets to allow multiple users to vote on which track should be added to a shared Spotify Connect queue next, using `POST /me/player/queue`.
*   **Multi-format Playlist Exporters**: A tool to export a user's playlists into various formats like M3U, JSON, or XML for compatibility with other music players or for backup purposes.
*   **Personal Listening Analytics**: A dashboard that consumes a user's listening history (`GET /me/player/recently-played`) and top tracks/artists to generate personalized analytics and charts about their listening habits over time.
*   **Discord Music Bot**: A Discord bot that uses Zotify's API to search for and download tracks, then stream them into a voice channel, effectively creating a self-hosted music bot that isn't reliant on YouTube.

---

## 6. API Design Guidelines

*   **Namespacing**: To maintain clarity and avoid conflicts, the API will be namespaced as follows:
    *   `/spotify/...`: For endpoints that are direct proxies of the Spotify Web API. These should mirror the official Spotify endpoint structure where possible.
    *   `/librespot/...`: For endpoints that expose raw or direct Librespot functionality, such as player control or device emulation.
    *   `/zotify/...` or `/...`: For Zotify's own composite features, such as search, downloads, and library management.

*   **Authentication Strategy**:
    *   **Spotify OAuth**: Endpoints under `/spotify/` and those requiring user-specific actions (e.g., managing playlists, accessing user library) will be protected by a standard Spotify OAuth 2.0 flow. Zotify will manage token acquisition and refresh on behalf of the user.
    *   **Internal API Keys**: For admin-level actions or services that don't have a user context (e.g., system monitoring, managing all downloads), a separate internal API key system will be used. These keys will be configurable by the Zotify administrator.

*   **REST vs. WebSocket**:
    *   **REST**: The majority of the API will be RESTful, using standard HTTP verbs (GET, POST, PUT, DELETE) for predictable, stateless interactions. This is suitable for metadata lookups, searching, and one-off actions like queueing a download.
    *   **WebSockets**: For real-time features, a WebSocket endpoint (`/ws`) will be provided. Clients can connect to this to receive live updates on download progress, player status changes, and notifications. This avoids the need for constant polling.

*   **Streaming Endpoint Structure**:
    *   Direct audio streaming will not be a primary goal initially.
    *   The `/downloads` endpoint will accept a request to begin a download and return a task ID.
    *   Clients can then either poll a `/downloads/{task_id}/status` endpoint or listen for updates on the WebSocket connection to monitor progress.

*   **Token Refresh Logic**:
    *   Zotify's backend will be responsible for securely storing the user's Spotify refresh token.
    *   It will automatically refresh the access token when it expires and handle any errors related to token expiration gracefully, without requiring user intervention.
    *   The API will expose an endpoint (`/auth/status`) for clients to check the validity of the current user's authentication.

*   **Caching and Rate Limiting**:
    *   **Caching**: Zotify will implement a caching layer (e.g., using Redis) for responses from the Spotify API to reduce redundant calls and improve performance. Metadata that changes infrequently (e.g., track details) will be cached more aggressively than data that changes often (e.g., playlists).
    *   **Rate Limiting**: To prevent abuse and stay within Spotify's API limits, Zotify will implement its own rate limiting on a per-user and/or per-IP basis for all external-facing endpoints.
