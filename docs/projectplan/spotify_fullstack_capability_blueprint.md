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

| Capability          | Description                               | Module/Trait          | Zotify Usage (Y/N) | Recommended Zotify Exposure in API |
| ------------------- | ----------------------------------------- | --------------------- | ------------------ | ---------------------------------- |
| **Authentication**  | Authenticate with Spotify.                | `librespot.core`      | ✅                 | ✅                                 |
| **Audio Streaming** | Download audio streams.                   | `librespot.audio`     | ✅                 | ❌ (for now)                       |
| **Playback Control**| Control playback (play, pause, etc.).     | `librespot.player`    | ❌                 | ✅                                 |
| **Device Control**  | Manage playback devices.                  | `librespot.discovery` | ❌                 | ✅                                 |
| **Metadata**        | Fetch metadata for tracks, albums, etc.   | `librespot.metadata`  | ❌                 | ✅                                 |
| **Session Mgmt**    | Manage the user's session.                | `librespot.core`      | ✅                 | ❌                                 |
| **Caching**         | Cache audio and metadata.                 | `librespot.cache`     | ❌                 | ❌                                 |

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
| `GET /v1/albums/{id}`           | -                   | Get an album's metadata.                               | ✅                                            | `GET /spotify/albums/{id}`          | Spotify Web API        | -                                                                                 |
| `GET /v1/albums`                | -                   | Get several albums' metadata.                          | ✅                                            | `GET /spotify/albums`               | Spotify Web API        | -                                                                                 |
| `GET /v1/albums/{id}/tracks`    | -                   | Get an album's tracks.                                 | ✅                                            | `GET /spotify/albums/{id}/tracks`   | Spotify Web API        | -                                                                                 |
| `GET /v1/me/albums`             | `user-library-read` | Get the current user's saved albums.                   | ✅                                            | `GET /spotify/me/albums`            | Spotify Web API        | -                                                                                 |
| `PUT /v1/me/albums`             | `user-library-modify` | Save one or more albums to the current user's library. | ✅                                            | `PUT /spotify/me/albums`            | Spotify Web API        | -                                                                                 |
| `DELETE /v1/me/albums`          | `user-library-modify` | Remove one or more albums from the current user's library. | ✅                                            | `DELETE /spotify/me/albums`         | Spotify Web API        | -                                                                                 |
| `GET /v1/me/albums/contains`    | `user-library-read` | Check if one or more albums is already saved in the current user's library. | ✅                                            | `GET /spotify/me/albums/contains`   | Spotify Web API        | -                                                                                 |
| `GET /v1/new-releases`          | -                   | Get a list of new album releases featured in Spotify.  | ❌                                            | -                                   | Spotify Web API        | Low relevance to Zotify's core use case.                                          |

### Artists

| Spotify Endpoint                    | Auth Scope Required | Relevant Use Case(s)                                       | Zotify Internal Mapping (planned/implemented) | Target Zotify External API Endpoint     | Required Modules       | Feasibility Notes |
| ----------------------------------- | ------------------- | ---------------------------------------------------------- | --------------------------------------------- | --------------------------------------- | ---------------------- | ----------------- |
| `GET /v1/artists/{id}`              | -                   | Get an artist's metadata.                                  | ✅                                            | `GET /spotify/artists/{id}`             | Spotify Web API        | -                 |
| `GET /v1/artists`                   | -                   | Get several artists' metadata.                             | ✅                                            | `GET /spotify/artists`                  | Spotify Web API        | -                 |
| `GET /v1/artists/{id}/albums`       | -                   | Get an artist's albums.                                    | ✅                                            | `GET /spotify/artists/{id}/albums`      | Spotify Web API        | -                 |
| `GET /v1/artists/{id}/top-tracks`   | -                   | Get an artist's top tracks.                                | ✅                                            | `GET /spotify/artists/{id}/top-tracks`  | Spotify Web API        | -                 |
| `GET /v1/artists/{id}/related-artists`| -                   | Get artists similar to an artist.                          | ❌                                            | -                                       | Spotify Web API        | Low relevance.    |

### Tracks

| Spotify Endpoint                | Auth Scope Required | Relevant Use Case(s)                                   | Zotify Internal Mapping (planned/implemented) | Target Zotify External API Endpoint | Required Modules       | Feasibility Notes |
| ------------------------------- | ------------------- | ------------------------------------------------------ | --------------------------------------------- | ----------------------------------- | ---------------------- | ----------------- |
| `GET /v1/tracks/{id}`           | -                   | Get a track's metadata.                                | ✅                                            | `GET /spotify/tracks/{id}`          | Spotify Web API        | -                 |
| `GET /v1/tracks`                | -                   | Get several tracks' metadata.                          | ✅                                            | `GET /spotify/tracks`               | Spotify Web API        | -                 |
| `GET /v1/me/tracks`             | `user-library-read` | Get the current user's saved tracks.                   | ✅                                            | `GET /spotify/me/tracks`            | Spotify Web API        | -                 |
| `PUT /v1/me/tracks`             | `user-library-modify` | Save one or more tracks to the current user's library. | ✅                                            | `PUT /spotify/me/tracks`            | Spotify Web API        | -                 |
| `DELETE /v1/me/tracks`          | `user-library-modify` | Remove one or more tracks from the current user's library. | ✅                                            | `DELETE /spotify/me/tracks`         | Spotify Web API        | -                 |
| `GET /v1/me/tracks/contains`    | `user-library-read` | Check if one or more tracks is already saved in the current user's library. | ✅                                            | `GET /spotify/me/tracks/contains`   | Spotify Web API        | -                 |
| `GET /v1/audio-features/{id}`   | -                   | Get audio features for a track.                        | ❌                                            | -                                   | Spotify Web API        | Low relevance.    |
| `GET /v1/audio-features`        | -                   | Get audio features for several tracks.                 | ❌                                            | -                                   | Spotify Web API        | Low relevance.    |
| `GET /v1/audio-analysis/{id}`   | -                   | Get a detailed audio analysis for a track.             | ❌                                            | -                                   | Spotify Web API        | Low relevance.    |
| `GET /v1/recommendations`       | -                   | Get recommendations based on seeds.                    | ❌                                            | -                                   | Spotify Web API        | Low relevance.    |

### Playlists

| Spotify Endpoint                | Auth Scope Required | Relevant Use Case(s)                                   | Zotify Internal Mapping (planned/implemented) | Target Zotify External API Endpoint | Required Modules       | Feasibility Notes |
| ------------------------------- | ------------------- | ------------------------------------------------------ | --------------------------------------------- | ----------------------------------- | ---------------------- | ----------------- |
| `GET /v1/playlists/{playlist_id}` | `playlist-read-private` | Get a playlist's details.                              | ✅                                            | `GET /spotify/playlists/{playlist_id}` | Spotify Web API        | -                 |
| `PUT /v1/playlists/{playlist_id}` | `playlist-modify-public`, `playlist-modify-private` | Change a playlist's name, description, and public status. | ✅                                            | `PUT /spotify/playlists/{playlist_id}` | Spotify Web API        | -                 |
| `POST /v1/playlists/{playlist_id}/tracks` | `playlist-modify-public`, `playlist-modify-private` | Add one or more items to a playlist.                   | ✅                                            | `POST /spotify/playlists/{playlist_id}/tracks` | Spotify Web API        | -                 |
| `PUT /v1/playlists/{playlist_id}/tracks` | `playlist-modify-public`, `playlist-modify-private` | Reorder or replace a playlist's items.                 | ✅                                            | `PUT /spotify/playlists/{playlist_id}/tracks` | Spotify Web API        | -                 |
| `DELETE /v1/playlists/{playlist_id}/tracks` | `playlist-modify-public`, `playlist-modify-private` | Remove one or more items from a playlist.              | ✅                                            | `DELETE /spotify/playlists/{playlist_id}/tracks` | Spotify Web API        | -                 |
| `GET /v1/me/playlists`          | `playlist-read-private` | Get a list of the current user's playlists.            | ✅                                            | `GET /spotify/me/playlists`         | Spotify Web API        | -                 |
| `GET /v1/users/{user_id}/playlists` | `playlist-read-private` | Get a list of a user's playlists.                      | ✅                                            | `GET /spotify/users/{user_id}/playlists` | Spotify Web API        | -                 |
| `POST /v1/users/{user_id}/playlists` | `playlist-modify-public`, `playlist-modify-private` | Create a new playlist.                                 | ✅                                            | `POST /spotify/users/{user_id}/playlists` | Spotify Web API        | -                 |
| `GET /v1/browse/featured-playlists` | -                   | Get a list of featured playlists.                      | ❌                                            | -                                   | Spotify Web API        | Low relevance.    |
| `GET /v1/browse/categories/{category_id}/playlists` | -                   | Get a list of playlists for a specific category.       | ❌                                            | -                                   | Spotify Web API        | Low relevance.    |
| `GET /v1/playlists/{playlist_id}/images` | -                   | Get the cover image for a playlist.                    | ❌                                            | -                                   | Spotify Web API        | Low relevance.    |
| `PUT /v1/playlists/{playlist_id}/images` | `ugc-image-upload`, `playlist-modify-public`, `playlist-modify-private` | Upload a custom playlist cover image.                  | ❌                                            | -                                   | Spotify Web API        | Low relevance.    |

### Search

| Spotify Endpoint                | Auth Scope Required | Relevant Use Case(s)                                   | Zotify Internal Mapping (planned/implemented) | Target Zotify External API Endpoint | Required Modules       | Feasibility Notes |
| ------------------------------- | ------------------- | ------------------------------------------------------ | --------------------------------------------- | ----------------------------------- | ---------------------- | ----------------- |
| `GET /v1/search`                | -                   | Search for an item.                                    | ✅                                            | `GET /spotify/search`               | Spotify Web API        | -                 |

### User Profile

| Spotify Endpoint                | Auth Scope Required | Relevant Use Case(s)                                   | Zotify Internal Mapping (planned/implemented) | Target Zotify External API Endpoint | Required Modules       | Feasibility Notes |
| ------------------------------- | ------------------- | ------------------------------------------------------ | --------------------------------------------- | ----------------------------------- | ---------------------- | ----------------- |
| `GET /v1/me`                    | `user-read-private`, `user-read-email` | Get the current user's profile.                        | ✅                                            | `GET /spotify/me`                   | Spotify Web API        | -                 |
| `GET /v1/users/{user_id}`       | -                   | Get a user's public profile.                           | ✅                                            | `GET /spotify/users/{user_id}`      | Spotify Web API        | -                 |

### Player

| Spotify Endpoint                | Auth Scope Required | Relevant Use Case(s)                                   | Zotify Internal Mapping (planned/implemented) | Target Zotify External API Endpoint | Required Modules       | Feasibility Notes |
| ------------------------------- | ------------------- | ------------------------------------------------------ | --------------------------------------------- | ----------------------------------- | ---------------------- | ----------------- |
| `GET /v1/me/player`             | `user-read-playback-state` | Get the user's current playback state.                 | ✅                                            | `GET /spotify/me/player`            | Spotify Web API        | -                 |
| `PUT /v1/me/player`             | `user-modify-playback-state` | Transfer playback to a new device.                     | ✅                                            | `PUT /spotify/me/player`            | Spotify Web API        | -                 |
| `GET /v1/me/player/devices`     | `user-read-playback-state` | Get a user's available devices.                        | ✅                                            | `GET /spotify/me/player/devices`    | Spotify Web API        | -                 |
| `GET /v1/me/player/currently-playing` | `user-read-currently-playing` | Get the user's currently playing track.                | ✅                                            | `GET /spotify/me/player/currently-playing` | Spotify Web API        | -                 |
| `PUT /v1/me/player/play`        | `user-modify-playback-state` | Start or resume playback.                              | ✅                                            | `PUT /spotify/me/player/play`       | Spotify Web API        | -                 |
| `PUT /v1/me/player/pause`       | `user-modify-playback-state` | Pause playback.                                        | ✅                                            | `PUT /spotify/me/player/pause`      | Spotify Web API        | -                 |
| `POST /v1/me/player/next`       | `user-modify-playback-state` | Skip to the next track.                                | ✅                                            | `POST /spotify/me/player/next`      | Spotify Web API        | -                 |
| `POST /v1/me/player/previous`   | `user-modify-playback-state` | Skip to the previous track.                            | ✅                                            | `POST /spotify/me/player/previous`  | Spotify Web API        | -                 |
| `PUT /v1/me/player/seek`        | `user-modify-playback-state` | Seek to a position in the current track.               | ✅                                            | `PUT /spotify/me/player/seek`       | Spotify Web API        | -                 |
| `PUT /v1/me/player/repeat`      | `user-modify-playback-state` | Set the repeat mode.                                   | ✅                                            | `PUT /spotify/me/player/repeat`     | Spotify Web API        | -                 |
| `PUT /v1/me/player/volume`      | `user-modify-playback-state` | Set the volume.                                        | ✅                                            | `PUT /spotify/me/player/volume`     | Spotify Web API        | -                 |
| `PUT /v1/me/player/shuffle`     | `user-modify-playback-state` | Toggle shuffle.                                        | ✅                                            | `PUT /spotify/me/player/shuffle`    | Spotify Web API        | -                 |
| `GET /v1/me/player/recently-played` | `user-read-recently-played` | Get the user's recently played tracks.                 | ✅                                            | `GET /spotify/me/player/recently-played` | Spotify Web API        | -                 |
| `POST /v1/me/player/queue`      | `user-modify-playback-state` | Add an item to the user's playback queue.              | ✅                                            | `POST /spotify/me/player/queue`     | Spotify Web API        | -                 |

### Browse

| Spotify Endpoint                | Auth Scope Required | Relevant Use Case(s)                                   | Zotify Internal Mapping (planned/implemented) | Target Zotify External API Endpoint | Required Modules       | Feasibility Notes |
| ------------------------------- | ------------------- | ------------------------------------------------------ | --------------------------------------------- | ----------------------------------- | ---------------------- | ----------------- |
| `GET /v1/browse/new-releases`   | -                   | Get a list of new releases.                            | ❌                                            | -                                   | Spotify Web API        | Low relevance.    |
| `GET /v1/browse/featured-playlists` | -                   | Get a list of featured playlists.                      | ❌                                            | -                                   | Spotify Web API        | Low relevance.    |
| `GET /v1/browse/categories`     | -                   | Get a list of categories.                              | ❌                                            | -                                   | Spotify Web API        | Low relevance.    |
| `GET /v1/browse/categories/{category_id}` | -                   | Get a single category.                                 | ❌                                            | -                                   | Spotify Web API        | Low relevance.    |
| `GET /v1/browse/categories/{category_id}/playlists` | -                   | Get a list of playlists for a specific category.       | ❌                                            | -                                   | Spotify Web API        | Low relevance.    |
| `GET /v1/recommendations/available-genre-seeds` | -                   | Get a list of available genre seeds.                   | ❌                                            | -                                   | Spotify Web API        | Low relevance.    |

### Follow

| Spotify Endpoint                | Auth Scope Required | Relevant Use Case(s)                                   | Zotify Internal Mapping (planned/implemented) | Target Zotify External API Endpoint | Required Modules       | Feasibility Notes |
| ------------------------------- | ------------------- | ------------------------------------------------------ | --------------------------------------------- | ----------------------------------- | ---------------------- | ----------------- |
| `GET /v1/me/following`          | `user-follow-read`  | Get the user's followed artists.                       | ✅                                            | `GET /spotify/me/following`         | Spotify Web API        | -                 |
| `PUT /v1/me/following`          | `user-follow-modify`| Follow artists or users.                               | ✅                                            | `PUT /spotify/me/following`         | Spotify Web API        | -                 |
| `DELETE /v1/me/following`       | `user-follow-modify`| Unfollow artists or users.                             | ✅                                            | `DELETE /spotify/me/following`      | Spotify Web API        | -                 |
| `GET /v1/me/following/contains` | `user-follow-read`  | Check if the user follows artists or users.            | ✅                                            | `GET /spotify/me/following/contains`| Spotify Web API        | -                 |
| `GET /v1/playlists/{playlist_id}/followers` | `playlist-read-private` | Get a playlist's followers.                            | ❌                                            | -                                   | Spotify Web API        | Low relevance.    |
| `PUT /v1/playlists/{playlist_id}/followers` | `playlist-modify-public`, `playlist-modify-private` | Add the current user as a follower of a playlist.      | ✅                                            | `PUT /spotify/playlists/{playlist_id}/followers` | Spotify Web API        | -                 |
| `DELETE /v1/playlists/{playlist_id}/followers` | `playlist-modify-public`, `playlist-modify-private` | Remove the current user as a follower of a playlist.   | ✅                                            | `DELETE /spotify/playlists/{playlist_id}/followers` | Spotify Web API        | -                 |

### Library

| Spotify Endpoint                | Auth Scope Required | Relevant Use Case(s)                                   | Zotify Internal Mapping (planned/implemented) | Target Zotify External API Endpoint | Required Modules       | Feasibility Notes |
| ------------------------------- | ------------------- | ------------------------------------------------------ | --------------------------------------------- | ----------------------------------- | ---------------------- | ----------------- |
| `GET /v1/me/albums`             | `user-library-read` | Get the current user's saved albums.                   | ✅                                            | `GET /spotify/me/albums`            | Spotify Web API        | -                 |
| `PUT /v1/me/albums`             | `user-library-modify` | Save one or more albums to the current user's library. | ✅                                            | `PUT /spotify/me/albums`            | Spotify Web API        | -                 |
| `DELETE /v1/me/albums`          | `user-library-modify` | Remove one or more albums from the current user's library. | ✅                                            | `DELETE /spotify/me/albums`         | Spotify Web API        | -                 |
| `GET /v1/me/albums/contains`    | `user-library-read` | Check if one or more albums is already saved in the current user's library. | ✅                                            | `GET /spotify/me/albums/contains`   | Spotify Web API        | -                 |
| `GET /v1/me/tracks`             | `user-library-read` | Get the current user's saved tracks.                   | ✅                                            | `GET /spotify/me/tracks`            | Spotify Web API        | -                 |
| `PUT /v1/me/tracks`             | `user-library-modify` | Save one or more tracks to the current user's library. | ✅                                            | `PUT /spotify/me/tracks`            | Spotify Web API        | -                 |
| `DELETE /v1/me/tracks`          | `user-library-modify` | Remove one or more tracks from the current user's library. | ✅                                            | `DELETE /spotify/me/tracks`         | Spotify Web API        | -                 |
| `GET /v1/me/tracks/contains`    | `user-library-read` | Check if one or more tracks is already saved in the current user's library. | ✅                                            | `GET /spotify/me/tracks/contains`   | Spotify Web API        | -                 |
| `GET /v1/me/shows`              | `user-library-read` | Get the current user's saved shows.                    | ❌                                            | -                                   | Spotify Web API        | Low relevance.    |
| `PUT /v1/me/shows`              | `user-library-modify` | Save one or more shows to the current user's library.  | ❌                                            | -                                   | Spotify Web API        | Low relevance.    |
| `DELETE /v1/me/shows`           | `user-library-modify` | Remove one or more shows from the current user's library. | ❌                                            | -                                   | Spotify Web API        | Low relevance.    |
| `GET /v1/me/shows/contains`     | `user-library-read` | Check if one or more shows is already saved in the current user's library. | ❌                                            | -                                   | Spotify Web API        | Low relevance.    |
| `GET /v1/me/episodes`           | `user-library-read` | Get the current user's saved episodes.                 | ❌                                            | -                                   | Spotify Web API        | Low relevance.    |
| `PUT /v1/me/episodes`           | `user-library-modify` | Save one or more episodes to the current user's library. | ❌                                            | -                                   | Spotify Web API        | Low relevance.    |
| `DELETE /v1/me/episodes`        | `user-library-modify` | Remove one or more episodes from the current user's library. | ❌                                            | -                                   | Spotify Web API        | Low relevance.    |
| `GET /v1/me/episodes/contains`  | `user-library-read` | Check if one or more episodes is already saved in the current user's library. | ❌                                            | -                                   | Spotify Web API        | Low relevance.    |

### Personalization

| Spotify Endpoint                | Auth Scope Required | Relevant Use Case(s)                                   | Zotify Internal Mapping (planned/implemented) | Target Zotify External API Endpoint | Required Modules       | Feasibility Notes |
| ------------------------------- | ------------------- | ------------------------------------------------------ | --------------------------------------------- | ----------------------------------- | ---------------------- | ----------------- |
| `GET /v1/me/top/artists`        | `user-top-read`     | Get the user's top artists.                            | ✅                                            | `GET /spotify/me/top/artists`       | Spotify Web API        | -                 |
| `GET /v1/me/top/tracks`         | `user-top-read`     | Get the user's top tracks.                             | ✅                                            | `GET /spotify/me/top/tracks`        | Spotify Web API        | -                 |

---

## 3. Librespot Module Breakdown

| Librespot Module | Description | Zotify Integration Point | Relevant Spotify Features |
| --- | --- | --- | --- |
| `audio` | Handles audio decoding and output. | `zotify.audio` | Playback |
| `caching` | Caches audio and other data. | `zotify.cache` | Caching |
| `cdn` | Fetches audio from Spotify's CDN. | `zotify.cdn` | Playback |
| `crypto` | Handles encryption and decryption. | `zotify.crypto` | Authentication, Playback |
| `discovery` | Discovers Spotify Connect devices. | `zotify.discovery` | Connect |
| `mercury` | Handles communication with Spotify's Mercury service. | `zotify.mercury` | Metadata, Playlists, Search |
| `metadata` | Fetches metadata for tracks, albums, artists, and playlists. | `zotify.metadata` | Metadata |
| `player` | Manages the playback queue and player state. | `zotify.player` | Playback |
| `protocol` | Implements Spotify's protocol. | `zotify.protocol` | Core |
| `session` | Manages the user's session. | `zotify.session` | Authentication |
| `spclient` | High-level client for interacting with Spotify. | `zotify.spclient` | Core |

---

## 4. Planned API Feature List (with Use Cases)

| Feature | Use Case |
| --- | --- |
| **Search** | Search for tracks, albums, artists, and playlists. |
| **Download** | Download tracks, albums, and playlists. |
| **Playlist Management** | Create, read, update, and delete playlists. |
| **User Management** | Manage user accounts and preferences. |
| **Playback Control** | Control playback of tracks. |
| **Device Management** | Manage playback devices. |
| **Notifications** | Receive notifications about events. |
| **Real-time Updates** | Receive real-time updates about playback and other events. |

---

## 5. Creative Use Case Inventory

| Use Case | Description |
| --- | --- |
| **Automatic Playlist Generation** | Automatically generate playlists based on user preferences, listening history, and other factors. |
| **Social Listening** | Share what you're listening to with friends and see what they're listening to in real-time. |
| **Music Discovery** | Discover new music based on your taste and what's popular in your area. |
| **Personalized Radio** | Create personalized radio stations based on your favorite artists, genres, and tracks. |
| **Music Visualizer** | Visualize music with a variety of effects. |
| **Karaoke Mode** | Sing along to your favorite songs with lyrics displayed on the screen. |
| **DJ Mode** | Mix and scratch tracks like a professional DJ. |
| **Music-based Games** | Play games that are synchronized with the music. |

---

## 6. API Design Guidelines for Full Feature Exposure

| Guideline | Description |
| --- | --- |
| **Consistency** | The API should be consistent with the Spotify Web API. |
| **Simplicity** | The API should be simple and easy to use. |
| **Flexibility** | The API should be flexible enough to support a variety of use cases. |
| **Extensibility** | The API should be extensible so that new features can be added easily. |
| **Reliability** | The API should be reliable and always available. |
| **Scalability** | The API should be scalable to support a large number of users. |
| **Security** | The API should be secure and protect user data. |
