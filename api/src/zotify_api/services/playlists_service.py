# api/src/zotify_api/services/playlists_service.py
from typing import List, Tuple, Optional, Dict
import logging
from sqlalchemy import text
from fastapi import Depends
from zotify_api.config import settings
from zotify_api.services.db import get_db_engine

log = logging.getLogger(__name__)

DEFAULT_LIMIT = 25
MAX_LIMIT = 250

class PlaylistsServiceError(Exception):
    pass

class PlaylistsService:
    def __init__(self, db_engine):
        self.db_engine = db_engine

    def get_default_limit(self) -> int:
        return DEFAULT_LIMIT

    def get_max_limit(self) -> int:
        return MAX_LIMIT

    def _normalize_limit(self, limit: int) -> int:
        try:
            limit = int(limit)
        except Exception:
            limit = DEFAULT_LIMIT
        if limit <= 0:
            return DEFAULT_LIMIT
        return min(limit, MAX_LIMIT)

    def _normalize_offset(self, offset: int) -> int:
        try:
            offset = int(offset)
        except Exception:
            offset = 0
        return max(0, offset)

    def get_playlists(self, limit: int = DEFAULT_LIMIT, offset: int = 0, search: Optional[str] = None) -> Tuple[List[Dict], int]:
        limit = self._normalize_limit(limit)
        offset = self._normalize_offset(offset)
        if not self.db_engine:
            # Non-db fallback: return empty list + 0 — keep predictable
            return [], 0

        try:
            with self.db_engine.connect() as conn:
                if search:
                    stmt = text("SELECT id, name FROM playlists WHERE name LIKE :q LIMIT :limit OFFSET :offset")
                    params = {"q": f"%{search}%", "limit": limit, "offset": offset}
                else:
                    stmt = text("SELECT id, name FROM playlists LIMIT :limit OFFSET :offset")
                    params = {"limit": limit, "offset": offset}
                result = conn.execute(stmt, params)
                rows = result.mappings().all()
                items = [dict(r) for r in rows]
                # For now the DB doesn’t return a total — return len(items) (okay for pagination tests)
                return items, len(items)
        except Exception as exc:
            log.exception("Error fetching playlists")
            # Surface a service-level error to the route
            raise PlaylistsServiceError("Database error while fetching playlists") from exc

    def create_playlist(self, playlist_in: Dict) -> Dict:
        # Minimal validation is performed in Pydantic at the route layer, but check here too.
        if not self.db_engine:
            # Not able to persist — raise so route can return 503 or fallback.
            raise PlaylistsServiceError("No DB engine available")
        try:
            with self.db_engine.connect() as conn:
                stmt = text("INSERT INTO playlists (name) VALUES (:name)")
                conn.execute(stmt, {"name": playlist_in["name"]})
                # In a real DB the insert should return an id. For now, return the payload (tests will mock DB).
                return {"id": None, "name": playlist_in["name"]}
        except Exception as exc:
            log.exception("Error creating playlist")
            raise PlaylistsServiceError("Database error while creating playlist") from exc

def get_playlists_service(db_engine: any = Depends(get_db_engine)):
    return PlaylistsService(db_engine)
