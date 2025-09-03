import logging
from typing import Any, Dict, List, Tuple, cast

from sqlalchemy.orm import Session

from zotify_api.database import crud
from zotify_api.providers.base import BaseProvider

log = logging.getLogger(__name__)


def get_tracks(
    db: Session, limit: int = 25, offset: int = 0, q: str | None = None
) -> Tuple[List[Dict[str, Any]], int]:
    """
    Get all tracks from the database with optional search query.
    """
    if not db:
        return [], 0
    db_tracks = crud.get_tracks(db, skip=offset, limit=limit, q=q)
    items = [
        {
            "id": t.id,
            "name": t.name,
            "artist": t.artist,
            "album": t.album,
            "created_at": t.created_at,
            "updated_at": t.updated_at,
        }
        for t in db_tracks
    ]
    return items, len(items)


def get_track(db: Session, track_id: str) -> Dict[str, Any] | None:
    """
    Get a single track by its ID.
    """
    if not db:
        return None
    db_track = crud.get_track(db, track_id)
    if db_track:
        return {
            "id": db_track.id,
            "name": db_track.name,
            "artist": db_track.artist,
            "album": db_track.album,
            "created_at": db_track.created_at,
            "updated_at": db_track.updated_at,
        }
    return None


def create_track(db: Session, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a new track in the database.
    """
    db_track = crud.create_track(db, payload)
    return {
        "id": db_track.id,
        "name": db_track.name,
        "artist": db_track.artist,
        "album": db_track.album,
        "created_at": db_track.created_at,
        "updated_at": db_track.updated_at,
    }


def update_track(
    db: Session, track_id: str, payload: Dict[str, Any]
) -> Dict[str, Any] | None:
    """
    Update a track's information.
    """
    allowed_columns = ["name", "artist", "album", "duration_seconds", "path"]
    update_payload = {key: payload[key] for key in payload if key in allowed_columns}

    if not update_payload:
        raise ValueError("No valid fields to update.")

    db_track = crud.update_track(db, track_id, update_payload)
    if db_track:
        return {
            "id": db_track.id,
            "name": db_track.name,
            "artist": db_track.artist,
            "album": db_track.album,
            "created_at": db_track.created_at,
            "updated_at": db_track.updated_at,
        }
    return None


def delete_track(db: Session, track_id: str) -> None:
    """
    Delete a track from the database.
    """
    crud.delete_track(db, track_id)


def search_tracks(
    db: Session, q: str, limit: int, offset: int
) -> Tuple[List[Dict[str, Any]], int]:
    return get_tracks(db, limit, offset, q)


def upload_cover(
    track_id: str, file_bytes: bytes
) -> Dict[str, Any]:
    # This is a stub for now
    return {"track_id": track_id, "cover_url": f"/static/covers/{track_id}.jpg"}


async def get_tracks_metadata_from_spotify(
    track_ids: List[str], provider: BaseProvider
) -> List[Dict[str, Any]]:
    """
    Retrieves track metadata from the configured provider.
    """
    if hasattr(provider, "client"):
        metadata = await provider.client.get_tracks_metadata(track_ids)
        return cast(List[Dict[str, Any]], metadata)
    return []
