import logging
from typing import List, Optional

from sqlalchemy import text
from sqlalchemy.orm import Session

from .. import models
from ..core.utils import get_local_track_path
from ..schemas import TrackCreate

log = logging.getLogger(__name__)

def get_track(db: Session, track_id: int) -> Optional[models.Track]:
    return db.query(models.Track).filter(models.Track.id == track_id).first()

def get_tracks(db: Session, skip: int = 0, limit: int = 100) -> List[models.Track]:
    return db.query(models.Track).offset(skip).limit(limit).all()

def create_track(db: Session, track: TrackCreate) -> models.Track:
    db_track = models.Track(**track.dict())
    db.add(db_track)
    db.commit()
    db.refresh(db_track)
    return db_track

def get_track_by_name(db: Session, name: str) -> Optional[models.Track]:
    return db.query(models.Track).filter(models.Track.name == name).first()

def get_track_by_artist(db: Session, artist: str) -> List[models.Track]:
    return db.query(models.Track).filter(models.Track.artist == artist).all()

def get_track_by_album(db: Session, album: str) -> List[models.Track]:
    return db.query(models.Track).filter(models.Track.album == album).all()

def get_track_by_spotify_id(db: Session, spotify_id: str) -> Optional[models.Track]:
    return db.query(models.Track).filter(models.Track.spotify_id == spotify_id).first()

def get_local_path(track_id: int, db: Session) -> Optional[str]:
    track = get_track(db, track_id)
    if track:
        return get_local_track_path(track.name, track.artist, track.album)
    return None

def log_download(db: Session, name: str, artist: str, album: str, duration_seconds: int, path: str):
    """
    Logs a downloaded track to the database.
    """
    stmt = text(
        "INSERT INTO tracks (name, artist, album, duration_seconds, path) "
        "VALUES (:name, :artist, :album, :duration_seconds, :path)"
    )
    db.execute(
        stmt,
        {
            "name": name,
            "artist": artist,
            "album": album,
            "duration_seconds": duration_seconds,
            "path": path,
        },
    )
    db.commit()
