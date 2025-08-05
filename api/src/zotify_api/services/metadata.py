# api/src/zotify_api/services/metadata.py
from datetime import datetime
import os
from sqlalchemy import text
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from zotify_api.services.db import get_db_engine
from zotify_api.config import settings
import logging

log = logging.getLogger(__name__)

def get_db_counts():
    """
    Return (total_tracks:int, total_playlists:int, last_updated:datetime|None)
    Falls back to safe defaults if DB or tables are missing.
    """
    engine = get_db_engine()
    # If no engine available (shouldn't happen with dev default), return fallback
    if engine is None:
        log.warning("get_db_counts: no DB engine available — returning fallback counts")
        return 0, 0, None

    try:
        with engine.connect() as conn:
            total_tracks = conn.execute(text("SELECT COUNT(1) FROM tracks")).scalar() or 0
            total_playlists = conn.execute(text("SELECT COUNT(1) FROM playlists")).scalar() or 0
            last_track = conn.execute(text("SELECT MAX(updated_at) FROM tracks")).scalar()
            last_updated = last_track if last_track is not None else None
            return int(total_tracks), int(total_playlists), last_updated
    except (OperationalError, SQLAlchemyError) as e:
        # Expected when table is missing or DB schema not created
        exc_info = settings.app_env == "development"
        log.warning(
            "DB error in get_db_counts — returning fallback. Error: %s",
            e,
            exc_info=exc_info,
        )
        return 0, 0, None

def get_library_size_mb(path: str | None = None) -> float:
    path = path or settings.library_path
    total_bytes = 0
    for root, _, files in os.walk(path):
        for f in files:
            try:
                total_bytes += os.path.getsize(os.path.join(root,f))
            except OSError:
                continue
    return round(total_bytes / (1024*1024), 2)
