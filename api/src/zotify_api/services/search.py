from sqlalchemy import text
from zotify_api.services.db import get_db_engine
from zotify_api.services.spotify import search_spotify

def perform_search(q: str, type: str = "track", limit: int = 25, offset: int = 0, engine=None):
    engine = engine or get_db_engine()
    if not engine:
        return search_spotify(q, type=type, limit=limit, offset=offset)
    try:
        with engine.connect() as conn:
            query = text("SELECT id, name, type, artist, album FROM tracks WHERE name LIKE :q LIMIT :limit OFFSET :offset")
            result = conn.execute(query, {"q": f"%{q}%", "limit": limit, "offset": offset})
            rows = result.mappings().all()
            items = [dict(r) for r in rows]
            total = len(items)
            return items, total
    except Exception:
        # safe fallback to spotify search if DB fails
        return search_spotify(q, type=type, limit=limit, offset=offset)
