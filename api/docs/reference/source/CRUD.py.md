# Source Code Documentation: `crud.py`

**Module:** `api.src.zotify_api.database.crud`

## 1. Purpose

This module provides a comprehensive set of **CRUD** (Create, Read, Update, Delete) operations for all database models used in the Zotify API. It acts as a dedicated data access layer, abstracting the raw SQLAlchemy queries away from the business logic in the service layer.

By centralizing all database interactions here, we ensure that:
-   The logic for database queries is consistent and reusable.
-   The rest of the application is decoupled from the specifics of the ORM.
-   Finding and optimizing database operations is straightforward.

All functions in this module require an active SQLAlchemy `Session` object to be passed as the `db` parameter.

---

## 2. Functions

### DownloadJob CRUD

---

#### `create_download_job`
```python
def create_download_job(db: Session, job: schemas.DownloadJobCreate) -> models.DownloadJob:
```
**Description:** Creates a new download job in the database.

-   **Parameters:**
    -   `db` (Session): The SQLAlchemy database session.
    -   `job` (schemas.DownloadJobCreate): A Pydantic schema containing the `track_id` for the new job.
-   **Returns:**
    -   The newly created `models.DownloadJob` ORM object.

---

#### `get_download_job`
```python
def get_download_job(db: Session, job_id: str) -> models.DownloadJob | None:
```
**Description:** Retrieves a single download job by its unique `job_id`.

-   **Parameters:**
    -   `db` (Session): The SQLAlchemy database session.
    -   `job_id` (str): The UUID of the job to retrieve.
-   **Returns:**
    -   The `models.DownloadJob` object if found, otherwise `None`.

---

#### `get_all_download_jobs`
```python
def get_all_download_jobs(db: Session) -> List[models.DownloadJob]:
```
**Description:** Retrieves all download jobs from the database, ordered by creation time (newest first).

-   **Parameters:**
    -   `db` (Session): The SQLAlchemy database session.
-   **Returns:**
    -   A list of all `models.DownloadJob` objects.

---

#### `get_next_pending_download_job`
```python
def get_next_pending_download_job(db: Session) -> models.DownloadJob | None:
```
**Description:** Retrieves the oldest job currently in the 'pending' state. This is used by the download worker to pick the next job to process.

-   **Parameters:**
    -   `db` (Session): The SQLAlchemy database session.
-   **Returns:**
    -   The next pending `models.DownloadJob` object if one exists, otherwise `None`.

---

#### `update_download_job_status`
```python
def update_download_job_status(db: Session, job: models.DownloadJob, status: schemas.DownloadJobStatus, error: str | None = None, progress: float | None = None) -> models.DownloadJob:
```
**Description:** Updates the status, error message, and progress percentage of a specific download job.

-   **Parameters:**
    -   `db` (Session): The SQLAlchemy database session.
    -   `job` (models.DownloadJob): The job object to update.
    -   `status` (schemas.DownloadJobStatus): The new status enum.
    -   `error` (str, optional): An error message if the job failed.
    -   `progress` (float, optional): The new progress value (0.0 to 1.0).
-   **Returns:**
    -   The updated `models.DownloadJob` object.

---

#### `retry_failed_download_jobs`
```python
def retry_failed_download_jobs(db: Session) -> int:
```
**Description:** Finds all jobs with a 'failed' status and resets them to 'pending' so they can be re-processed by the worker.

-   **Parameters:**
    -   `db` (Session): The SQLAlchemy database session.
-   **Returns:**
    -   An integer count of the number of jobs that were updated.

---

### Playlist and Track CRUD

---

#### `get_or_create_track`
```python
def get_or_create_track(db: Session, track_id: str, track_name: str | None = None) -> models.Track:
```
**Description:** A utility function that retrieves a track by its ID if it exists in the database, or creates a new entry if it does not.

-   **Parameters:**
    -   `db` (Session): The SQLAlchemy database session.
    -   `track_id` (str): The Spotify ID of the track.
    -   `track_name` (str, optional): The name of the track.
-   **Returns:**
    -   The existing or newly created `models.Track` object.

---

#### `create_or_update_playlist`
```python
def create_or_update_playlist(db: Session, playlist_id: str, playlist_name: str, track_ids: list[str]) -> models.Playlist:
```
**Description:** Creates a new playlist or completely replaces the tracks of an existing one. This is the core function for the playlist sync operation.

-   **Parameters:**
    -   `db` (Session): The SQLAlchemy database session.
    -   `playlist_id` (str): The Spotify ID of the playlist.
    -   `playlist_name` (str): The name of the playlist.
    -   `track_ids` (list[str]): A list of Spotify track IDs to associate with the playlist.
-   **Returns:**
    -   The newly created or updated `models.Playlist` object.

---

#### `clear_all_playlists_and_tracks`
```python
def clear_all_playlists_and_tracks(db: Session) -> None:
```
**Description:** A destructive operation that deletes all records from the `playlists` and `tracks` tables, as well as their associations. Used to clear local state before a full sync.

-   **Parameters:**
    -   `db` (Session): The SQLAlchemy database session.
-   **Returns:**
    -   `None`.

---

### SpotifyToken CRUD

---

#### `get_spotify_token`
```python
def get_spotify_token(db: Session) -> models.SpotifyToken | None:
```
**Description:** Retrieves the Spotify token from the database. This function assumes a single-user, single-token system.

-   **Parameters:**
    -   `db` (Session): The SQLAlchemy database session.
-   **Returns:**
    -   The `models.SpotifyToken` object if it exists, otherwise `None`.

---

#### `create_or_update_spotify_token`
```python
def create_or_update_spotify_token(db: Session, token_data: Dict[str, Any]) -> models.SpotifyToken:
```
**Description:** Creates or updates the single Spotify token in the database. This is used after a successful OAuth2 flow or token refresh.

-   **Parameters:**
    -   `db` (Session): The SQLAlchemy database session.
    -   `token_data` (Dict[str, Any]): A dictionary containing token information (`access_token`, `refresh_token`, `expires_at`).
-   **Returns:**
    -   The created or updated `models.SpotifyToken` object.

---

#### `delete_spotify_token`
```python
def delete_spotify_token(db: Session) -> None:
```
**Description:** Deletes the Spotify token from the database, effectively logging the user out.

-   **Parameters:**
    -   `db` (Session): The SQLAlchemy database session.
-   **Returns:**
    -   `None`.
