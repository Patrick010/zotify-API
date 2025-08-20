from sqlalchemy import text

from zotify_api.providers.base import BaseProvider


async def perform_search(q: str, type: str, limit: int, offset: int, db_engine: any, provider: BaseProvider):
    search_type = type
    if type == "all":
        search_type = "track,album,artist,playlist"

    if not db_engine:
        return await provider.search(q, type=search_type, limit=limit, offset=offset)
    try:
        with db_engine.connect() as conn:
            sql_query = "SELECT id, name, type, artist, album FROM tracks WHERE name LIKE :q"
            params = {"q": f"%{q}%", "limit": limit, "offset": offset}
            if type != "all":
                sql_query += " AND type = :type"
                params["type"] = type
            sql_query += " LIMIT :limit OFFSET :offset"

            query = text(sql_query)
            result = conn.execute(query, params)
            rows = result.mappings().all()
            items = [dict(r) for r in rows]
            total = len(items)
            return items, total
    except Exception:
        # safe fallback to spotify search if DB fails
        return await provider.search(q, type=search_type, limit=limit, offset=offset)
