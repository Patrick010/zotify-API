from fastapi import APIRouter, Query, HTTPException
from zotify_api.config import settings
import zotify_api.services.db as db_service
import zotify_api.services.search as search_service

router = APIRouter(prefix="/search")

@router.get("")
def search(q: str = Query(...), type: str = "track", limit: int = 25, offset: int = 0):
    # feature flags checked at runtime
    if not settings.enable_fork_features or not settings.feature_search_advanced:
        raise HTTPException(status_code=404, detail="Advanced search disabled")

    # resolve engine at call time; tests will monkeypatch services.db.get_db_engine
    engine = db_service.get_db_engine()
    if engine:
        results, total = search_service.perform_search(
            q, type=type, limit=limit, offset=offset, engine=engine
        )
    else:
        results, total = search_service.search_spotify(
            q, type=type, limit=limit, offset=offset
        )
    return {"data": results, "meta": {"total": total, "limit": limit, "offset": offset}}
