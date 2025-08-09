from typing import List, Tuple, Dict, Any
import logging
from sqlalchemy import text
from zotify_api.config import settings
from zotify_api.services.db import get_db_engine
from zotify_api.services.spotify import search_spotify

log = logging.getLogger(__name__)

def get_tracks(limit: int = 25, offset: int = 0, q: str | None = None, engine: Any = None) -> Tuple[List[Dict], int]:
    engine = engine or get_db_engine()
    if not engine:
        # no DB — return safe empty response
        return [], 0

    try:
        with engine.connect() as conn:
            if q:
                stmt = text("SELECT id, name, artist, album FROM tracks WHERE name LIKE :q LIMIT :limit OFFSET :offset")
                result = conn.execute(stmt, {"q": f"%{q}%", "limit": limit, "offset": offset})
            else:
                stmt = text("SELECT id, name, artist, album FROM tracks LIMIT :limit OFFSET :offset")
                result = conn.execute(stmt, {"limit": limit, "offset": offset})
            rows = result.mappings().all()
            items = [dict(r) for r in rows]
            return items, len(items)
    except Exception as exc:
        if settings.app_env == "development":
            log.exception("get_tracks DB failed")
        else:
            log.error("get_tracks DB failed: %s", str(exc))
        # fallback to empty list (or spotify search if q is present)
        if q:
            return search_spotify(q, type="track", limit=limit, offset=offset)
        return [], 0

def get_track(track_id: str, engine: Any = None) -> Dict | None:
    engine = engine or get_db_engine()
    if not engine:
        return None

    try:
        with engine.connect() as conn:
            stmt = text("SELECT id, name, artist, album FROM tracks WHERE id = :track_id")
            result = conn.execute(stmt, {"track_id": track_id}).mappings().first()
            if result:
                now = datetime.now()
                return {**dict(result), "created_at": now, "updated_at": now}
            return None
    except Exception as exc:
        if settings.app_env == "development":
            log.exception("get_track DB failed")
        else:
            log.error("get_track DB failed: %s", str(exc))
        return None

from datetime import datetime

def create_track(payload: Dict, engine: Any = None) -> Dict:
    engine = engine or get_db_engine()
    if not engine:
        raise Exception("No DB engine available")

    try:
        with engine.connect() as conn:
            stmt = text("INSERT INTO tracks (name, artist, album, duration_seconds, path) VALUES (:name, :artist, :album, :duration_seconds, :path)")
            result = conn.execute(stmt, payload)
            now = datetime.now()
            return {"id": str(result.lastrowid), **payload, "created_at": now, "updated_at": now}
    except Exception as exc:
        if settings.app_env == "development":
            log.exception("create_track DB failed")
        else:
            log.error("create_track DB failed: %s", str(exc))
        raise

def update_track(track_id: str, payload: Dict, engine: Any = None) -> Dict:
    engine = engine or get_db_engine()
    if not engine:
        raise Exception("No DB engine available")

    try:
        with engine.connect() as conn:
            set_clause = ", ".join([f"{key} = :{key}" for key in payload.keys()])
            stmt = text(f"UPDATE tracks SET {set_clause} WHERE id = :track_id")
            conn.execute(stmt, {"track_id": track_id, **payload})
            now = datetime.now()
            # We need to fetch the full track to get all the fields
            track = get_track(track_id, engine)
            track.update(payload)
            track["updated_at"] = now
            return track
    except Exception as exc:
        if settings.app_env == "development":
            log.exception("update_track DB failed")
        else:
            log.error("update_track DB failed: %s", str(exc))
        raise

def delete_track(track_id: str, engine: Any = None) -> None:
    engine = engine or get_db_engine()
    if not engine:
        raise Exception("No DB engine available")

    try:
        with engine.connect() as conn:
            stmt = text("DELETE FROM tracks WHERE id = :track_id")
            conn.execute(stmt, {"track_id": track_id})
    except Exception as exc:
        if settings.app_env == "development":
            log.exception("delete_track DB failed")
        else:
            log.error("delete_track DB failed: %s", str(exc))
        raise

def search_tracks(q: str, limit: int, offset: int, engine: Any = None) -> Tuple[List[Dict], int]:
    return get_tracks(limit, offset, q, engine)

from zotify_api.services.spotify_client import SpotifyClient

def upload_cover(track_id: str, file_bytes: bytes, engine: Any = None) -> Dict:
    # This is a stub for now
    return {"track_id": track_id, "cover_url": f"/static/covers/{track_id}.jpg"}


async def get_tracks_metadata_from_spotify(track_ids: List[str]) -> List[Dict[str, Any]]:
    """
    Retrieves track metadata from Spotify using the dedicated client.
    """
    client = SpotifyClient()
    try:
        metadata = await client.get_tracks_metadata(track_ids)
        return metadata
    finally:
        await client.close()
