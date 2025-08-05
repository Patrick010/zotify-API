from datetime import datetime
import os
from sqlalchemy import text
from zotify_api.config import settings

def get_db_counts(db_engine) -> tuple[int,int,datetime]:
    # Example using SQLAlchemy core connection
    with db_engine.connect() as conn:
        total_tracks = conn.execute(text("SELECT COUNT(1) FROM tracks")).scalar() or 0
        total_playlists = conn.execute(text("SELECT COUNT(1) FROM playlists")).scalar() or 0
        last_track = conn.execute(text("SELECT MAX(updated_at) FROM tracks")).scalar()
    last_updated = last_track or datetime.utcnow()
    return total_tracks, total_playlists, last_updated

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
