from sqlalchemy import text
from typing import Callable

def perform_search(q: str, type: str, limit: int, offset: int, db_engine: any, spotify_search_func: Callable):
    if not db_engine:
        return spotify_search_func(q, type=type, limit=limit, offset=offset)
    try:
        with db_engine.connect() as conn:
            query = text("SELECT id, name, type, artist, album FROM tracks WHERE name LIKE :q LIMIT :limit OFFSET :offset")
            result = conn.execute(query, {"q": f"%{q}%", "limit": limit, "offset": offset})
            rows = result.mappings().all()
            items = [dict(r) for r in rows]
            total = len(items)
            return items, total
    except Exception:
        # safe fallback to spotify search if DB fails
        return spotify_search_func(q, type=type, limit=limit, offset=offset)
