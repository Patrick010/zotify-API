# Spotify Provider Connector

This document describes the implementation of the Spotify provider connector, which is the first provider to be integrated into the new provider-agnostic architecture.

## Module Location

`api/src/zotify_api/providers/spotify_connector.py`

## Interface Implementation

The `SpotifyConnector` class implements the `BaseProvider` interface defined in `base.py`. It provides concrete implementations for all the abstract methods, such as `search`, `get_playlist`, etc.

## Key Dependencies

-   **`SpotiClient`**: The connector uses the `SpotiClient` to make the actual calls to the Spotify Web API. The `SpotiClient` is provided to the connector via the `get_spoti_client` dependency, which ensures that it is always initialized with a valid, non-expired access token.
-   **Database Session**: The connector receives a database session, which it uses to interact with the database via the CRUD layer (e.g., for syncing playlists).

## Provider-Specific Quirks & Limitations

-   **Authentication**: The current authentication flow is specific to Spotify's OAuth 2.0 implementation with PKCE. A more generic authentication manager will be needed to support other providers with different authentication mechanisms.
-   **Data Models**: The current database models are closely based on the data returned by the Spotify API. A future iteration will involve creating more normalized, provider-agnostic Pydantic schemas, and the connector will be responsible for translating between the Spotify API format and the normalized format.
-   **Rate Limiting**: The connector does not currently implement any specific rate limiting logic. It relies on the `SpotiClient`'s basic retry mechanism.
