# ID: API-099
from typing import Any, Dict, List, Tuple, cast

from sqlalchemy import Engine, text

from zotify_api.providers.base import BaseProvider


async def perform_search(
    q: str,
    type: str,
    limit: int,
    offset: int,
    db_engine: Engine | None,
    provider: BaseProvider,
) -> Tuple[List[Dict[str, Any]], int]:
    search_type = type
    if type == "all":
        search_type = "track,album,artist,playlist"

    if not db_engine:
        return cast(
            Tuple[List[Dict[str, Any]], int],
            await provider.search(q, type=search_type, limit=limit, offset=offset),
        )
    try:
        with db_engine.connect() as conn:
            sql_query = (
                "SELECT id, name, type, artist, album " "FROM tracks WHERE name LIKE :q"
            )
            params: Dict[str, Any] = {"q": f"%{q}%", "limit": limit, "offset": offset}
            if type != "all":
                sql_query += " AND type = :type"
                params["type"] = type
            sql_query += " LIMIT :limit OFFSET :offset"

            query = text(sql_query)
            result = conn.execute(query, params)
            items = [dict(row) for row in result.mappings()]
            total = len(items)
            return items, total
    except Exception:
        # safe fallback to spotify search if DB fails
        return cast(
            Tuple[List[Dict[str, Any]], int],
            await provider.search(q, type=search_type, limit=limit, offset=offset),
        )
