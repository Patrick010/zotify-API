# Zotify API Manual

This manual provides an overview of the components of the Zotify API.

## API Endpoints

The Zotify API provides a set of endpoints for interacting with the Zotify service and Spotify. All endpoints are available under the `/api` prefix.

### Authentication

These endpoints are used to manage the authentication with Spotify.

*   `GET /auth/status`: Check the current authentication status.
*   `POST /auth/logout`: Log out from Spotify and clear credentials.
*   `GET /auth/refresh`: Refresh the Spotify access token.

### Spotify

These endpoints provide direct access to certain Spotify API features.

*   `GET /spotify/me`: Get the current user's Spotify profile.
*   `GET /spotify/devices`: List the user's available Spotify devices.

### Search

The search endpoint allows you to search for tracks, albums, artists, and playlists.

*   `GET /search`: Search for items on Spotify. Supports filtering by `type` and pagination with `limit` and `offset`.

### Tracks

Endpoints for managing tracks.

*   `POST /tracks/metadata`: Get metadata for multiple tracks at once.

### System

Endpoints for monitoring and diagnostics.

*   `GET /system/uptime`: Get the server's uptime.
*   `GET /system/env`: Get environment information about the server.
*   `GET /schema`: Get the OpenAPI schema for the API.


## Snitch

Snitch is a local OAuth callback listener used to securely capture the authorization code from Spotify during the authentication process.

For detailed installation and usage instructions, please refer to the [Snitch Installation Manual](../snitch/docs/INSTALLATION.md).
