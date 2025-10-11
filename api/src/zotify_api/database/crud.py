# ID: API-045
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


from zotify_api.services import jwt_service
from zotify_api.schemas import user as user_schemas

# --- User CRUD ---

def get_user_by_username(db: Session, username: str) -> models.User | None:
    return db.query(models.User).filter(models.User.username == username).first()


def get_user(db: Session, user_id: str) -> models.User | None:
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user: user_schemas.UserCreate) -> models.User:
    hashed_password = jwt_service.pwd_context.hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


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


# --- UserProfile CRUD ---

def create_user_profile(db: Session, user: models.User, name: str, email: str | None = None) -> models.UserProfile:
    db_profile = models.UserProfile(user_id=user.id, name=name, email=email)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def get_user_profile(db: Session, user_id: str) -> models.UserProfile | None:
    return db.query(models.UserProfile).filter(models.UserProfile.user_id == user_id).first()

def update_user_profile(db: Session, db_profile: models.UserProfile, name: str | None = None, email: str | None = None) -> models.UserProfile:
    if name is not None:
        db_profile.name = name
    if email is not None:
        db_profile.email = email
    db.commit()
    db.refresh(db_profile)
    return db_profile

# --- UserPreferences CRUD ---

def create_user_preferences(db: Session, user: models.User, theme: str = "dark", language: str = "en", notifications_enabled: bool = True) -> models.UserPreferences:
    db_preferences = models.UserPreferences(user_id=user.id, theme=theme, language=language, notifications_enabled=notifications_enabled)
    db.add(db_preferences)
    db.commit()
    db.refresh(db_preferences)
    return db_preferences

def get_user_preferences(db: Session, user_id: str) -> models.UserPreferences | None:
    return db.query(models.UserPreferences).filter(models.UserPreferences.user_id == user_id).first()

def update_user_preferences(db: Session, db_preferences: models.UserPreferences, theme: str | None = None, language: str | None = None, notifications_enabled: bool | None = None) -> models.UserPreferences:
    if theme is not None:
        db_preferences.theme = theme
    if language is not None:
        db_preferences.language = language
    if notifications_enabled is not None:
        db_preferences.notifications_enabled = notifications_enabled
    db.commit()
    db.refresh(db_preferences)
    return db_preferences

# --- LikedSong CRUD ---

def add_liked_song(db: Session, user: models.User, track_id: str) -> models.LikedSong:
    db_liked_song = models.LikedSong(user_id=user.id, track_id=track_id)
    db.add(db_liked_song)
    db.commit()
    db.refresh(db_liked_song)
    return db_liked_song

def get_liked_songs(db: Session, user_id: str) -> List[models.LikedSong]:
    return db.query(models.LikedSong).filter(models.LikedSong.user_id == user_id).all()

# --- History CRUD ---

def add_history(db: Session, user: models.User, track_id: str) -> models.History:
    db_history = models.History(user_id=user.id, track_id=track_id)
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history

def get_history(db: Session, user_id: str) -> List[models.History]:
    return db.query(models.History).filter(models.History.user_id == user_id).order_by(models.History.played_at.desc()).all()

def delete_history(db: Session, user_id: str) -> int:
    num_deleted = db.query(models.History).filter(models.History.user_id == user_id).delete()
    db.commit()
    return num_deleted


# --- Notification CRUD ---

def create_notification(db: Session, user: models.User, message: str) -> models.Notification:
    db_notification = models.Notification(user_id=user.id, message=message)
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

def get_notifications(db: Session, user_id: str) -> List[models.Notification]:
    return db.query(models.Notification).filter(models.Notification.user_id == user_id).order_by(models.Notification.created_at.desc()).all()

def mark_notification_as_read(db: Session, notification_id: int, read: bool = True) -> models.Notification | None:
    db_notification = db.query(models.Notification).filter(models.Notification.id == notification_id).first()
    if db_notification:
        db_notification.read = read
        db.commit()
        db.refresh(db_notification)
    return db_notification
