# Source Code Documentation: `tracks_service.py`

## 1. Module Description

This module, `tracks_service.py`, is responsible for all business logic related to track management. It provides a service layer that directly interacts with the database to perform CRUD (Create, Read, Update, Delete) operations on tracks. It also includes functionality to search for tracks and retrieve metadata from external providers like Spotify.

This service is primarily designed to be called by the API routes defined in `api/src/zotify_api/routes/tracks.py`.

## 2. Functions

### `get_tracks(...)`
-   **Description:** Retrieves a paginated list of tracks from the database. It can optionally filter the results based on a search query.
-   **Parameters:**
    -   `limit (int)`: The maximum number of tracks to return. Defaults to 25.
    -   `offset (int)`: The starting position from which to return tracks. Defaults to 0.
    -   `q (str | None)`: An optional search query to filter tracks by name.
    -   `engine (Any)`: An optional database engine connection. If not provided, it will get a new one.
-   **Returns:** A tuple containing a list of track dictionaries and the total count of returned items.

### `get_track(...)`
-   **Description:** Retrieves a single track from the database by its ID.
-   **Parameters:**
    -   `track_id (str)`: The unique identifier for the track.
    -   `engine (Any)`: An optional database engine connection.
-   **Returns:** A dictionary representing the track if found, otherwise `None`.

### `create_track(...)`
-   **Description:** Inserts a new track into the database.
-   **Parameters:**
    -   `payload (Dict[str, Any])`: A dictionary containing the track's data (`name`, `artist`, `album`, etc.).
    -   `engine (Any)`: An optional database engine connection.
-   **Returns:** A dictionary representing the newly created track, including its new ID.

### `update_track(...)`
-   **Description:** Updates the details of an existing track in the database.
-   **Parameters:**
    -   `track_id (str)`: The ID of the track to update.
    -   `payload (Dict[str, Any])`: A dictionary containing the fields to update.
    -   `engine (Any)`: An optional database engine connection.
-   **Returns:** A dictionary representing the updated track if successful, otherwise `None`.
-   **Note:** This function uses dynamic SQL generation based on the keys in the payload. The `# nosec B608` comment is used to suppress a Bandit warning for SQL injection, as the query parameters are handled safely by SQLAlchemy.

### `delete_track(...)`
-   **Description:** Deletes a track from the database.
-   **Parameters:**
    -   `track_id (str)`: The ID of the track to delete.
    -   `engine (Any)`: An optional database engine connection.
-   **Returns:** `None`.

### `search_tracks(...)`
-   **Description:** A simple alias for the `get_tracks` function, intended for search-specific use cases.
-   **Parameters:** Same as `get_tracks`.
-   **Returns:** Same as `get_tracks`.

### `upload_cover(...)`
-   **Description:** A stub function for handling cover art uploads. This feature is not fully implemented.
-   **Parameters:**
    -   `track_id (str)`: The ID of the track.
    -   `file_bytes (bytes)`: The image data.
    -   `engine (Any)`: An optional database engine connection.
-   **Returns:** A dictionary with a placeholder URL for the cover art.

### `get_tracks_metadata_from_spotify(...)`
-   **Description:** Retrieves detailed track metadata for a list of track IDs from an external provider (e.g., Spotify).
-   **Parameters:**
    -   `track_ids (List[str])`: A list of track IDs to fetch metadata for.
    -   `provider (BaseProvider)`: An instance of a provider connector that will be used to make the external API call.
-   **Returns:** A list of dictionaries, where each dictionary contains the metadata for a track.
-   **Note:** As noted in the source code comments, this function's implementation reveals a gap in the provider abstraction layer and contains a temporary workaround.

## 3. Usage Example

```python
# This is a conceptual example of how the service might be used.
# It does not include the full FastAPI context.

from tracks_service import create_track, get_track

# Create a new track
new_track_payload = {
    "name": "Bohemian Rhapsody",
    "artist": "Queen",
    "album": "A Night at the Opera",
    "duration_seconds": 355,
    "path": "/music/queen/bohemian_rhapsody.mp3"
}
created_track = create_track(new_track_payload)
print(f"Created track: {created_track}")

# Retrieve the track
if created_track:
    retrieved_track = get_track(created_track['id'])
    print(f"Retrieved track: {retrieved_track}")
```
