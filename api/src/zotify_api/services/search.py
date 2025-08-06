from sqlalchemy import text
from zotify_api.services.db import get_db_engine
import zotify_api.services.spotify as spotify_service

def perform_search(q: str, type: str = "track", limit: int = 25, offset: int = 0, engine=None):
    engine = engine or get_db_engine()
    if not engine:
        return spotify_service.search_spotify(q, type=type, limit=limit, offset=offset)

    with engine.connect() as conn:
        query = text("SELECT id, name, type, artist, album FROM tracks WHERE name LIKE :q LIMIT :limit OFFSET :offset")
        result = conn.execute(query, {"q": f"%{q}%", "limit": limit, "offset": offset})
        rows = result.mappings().all()
        items = [dict(r) for r in rows]
        total = len(items)  # In a real app, you'd run a separate COUNT(*) query
        return items, total
