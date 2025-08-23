from typing import Any, Dict, List

from sqlalchemy.orm import Session

from zotify_api.schemas import download as schemas

from . import models

# --- DownloadJob CRUD ---


def create_download_job(
    db: Session, job: schemas.DownloadJobCreate
) -> models.DownloadJob:
    """
    Create a new download job in the database.
    """
    db_job = models.DownloadJob(track_id=job.track_id)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


def get_download_job(db: Session, job_id: str) -> models.DownloadJob | None:
    """
    Get a single download job by its ID.
    """
    return (
        db.query(models.DownloadJob).filter(models.DownloadJob.job_id == job_id).first()
    )


def get_all_download_jobs(db: Session) -> List[models.DownloadJob]:
    """
    Get all download jobs from the database.
    """
    return (
        db.query(models.DownloadJob)
        .order_by(models.DownloadJob.created_at.desc())
        .all()
    )


def get_next_pending_download_job(db: Session) -> models.DownloadJob | None:
    """
    Get the oldest pending download job from the database.
    """
    return (
        db.query(models.DownloadJob)
        .filter(models.DownloadJob.status == "pending")
        .order_by(models.DownloadJob.created_at.asc())
        .first()
    )


def update_download_job_status(
    db: Session,
    job: models.DownloadJob,
    status: schemas.DownloadJobStatus,
    error: str | None = None,
    progress: float | None = None,
) -> models.DownloadJob:
    """
    Update the status, error message, and progress of a download job.
    """
    job.status = status.value
    job.error_message = error
    if progress is not None:
        job.progress = progress
    db.commit()
    db.refresh(job)
    return job


def retry_failed_download_jobs(db: Session) -> int:
    """
    Reset the status of all failed jobs to 'pending' and return the count.
    """
    num_updated = (
        db.query(models.DownloadJob)
        .filter(models.DownloadJob.status == "failed")
        .update({"status": "pending", "error_message": None})
    )
    db.commit()
    return num_updated


# --- Playlist and Track CRUD ---


def get_or_create_track(
    db: Session, track_id: str, track_name: str | None = None
) -> models.Track:
    """
    Get a track by its ID, or create it if it doesn't exist.
    """
    track = db.query(models.Track).filter(models.Track.id == track_id).first()
    if not track:
        track = models.Track(id=track_id, name=track_name)
        db.add(track)
        db.commit()
        db.refresh(track)
    return track


def create_or_update_playlist(
    db: Session, playlist_id: str, playlist_name: str, track_ids: list[str]
) -> models.Playlist:
    """
    Create a new playlist or update an existing one with a new set of tracks.
    """
    playlist = (
        db.query(models.Playlist).filter(models.Playlist.id == playlist_id).first()
    )
    if not playlist:
        playlist = models.Playlist(id=playlist_id, name=playlist_name)
        db.add(playlist)

    # Get or create all the track objects
    tracks = [get_or_create_track(db, track_id=tid) for tid in track_ids]

    # Replace the existing tracks with the new ones
    playlist.tracks = tracks

    db.commit()
    db.refresh(playlist)
    return playlist


def clear_all_playlists_and_tracks(db: Session) -> None:
    """
    Deletes all records from the playlist and track tables.
    """
    db.query(models.playlist_track_association).delete(synchronize_session=False)
    db.query(models.Playlist).delete(synchronize_session=False)
    db.query(models.Track).delete(synchronize_session=False)
    db.commit()


# --- SpotifyToken CRUD ---


def get_spotify_token(db: Session) -> models.SpotifyToken | None:
    """
    Get the Spotify token from the database. Assumes a single token for the app.
    """
    return db.query(models.SpotifyToken).first()


def create_or_update_spotify_token(
    db: Session, token_data: Dict[str, Any]
) -> models.SpotifyToken:
    """
    Create or update the Spotify token in the database.
    """
    token = get_spotify_token(db)
    if not token:
        token = models.SpotifyToken(
            access_token=token_data["access_token"],
            refresh_token=token_data["refresh_token"],
            expires_at=token_data["expires_at"],
        )
        db.add(token)
    else:
        token.access_token = token_data["access_token"]
        token.refresh_token = token_data.get("refresh_token", token.refresh_token)
        token.expires_at = token_data["expires_at"]

    db.commit()
    db.refresh(token)
    return token


def delete_spotify_token(db: Session) -> None:
    """
    Deletes the Spotify token from the database.
    """
    token = get_spotify_token(db)
    if token:
        db.delete(token)
        db.commit()
