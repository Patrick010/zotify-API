from fastapi import APIRouter, Query, HTTPException, Depends
from zotify_api.config import settings
import zotify_api.services.db as db_service
import zotify_api.services.search as search_service
from zotify_api.services.deps import get_provider
from zotify_api.providers.base import BaseProvider
from typing import Literal

router = APIRouter(prefix="/search", tags=["search"])

def get_feature_flags():
    return {
        "fork_features": settings.enable_fork_features,
        "search_advanced": settings.feature_search_advanced
    }

def get_db_engine():
    return db_service.get_db_engine()

@router.get("")
async def search(
    q: str = Query(...),
    type: Literal["track", "album", "artist", "playlist", "all"] = "all",
    limit: int = 20,
    offset: int = 0,
    feature_flags: dict = Depends(get_feature_flags),
    db_engine: any = Depends(get_db_engine),
    provider: BaseProvider = Depends(get_provider)
):
    if not feature_flags["fork_features"] or not feature_flags["search_advanced"]:
        raise HTTPException(status_code=404, detail="Advanced search disabled")

    results, total = await search_service.perform_search(
        q,
        type=type,
        limit=limit,
        offset=offset,
        db_engine=db_engine,
        provider=provider,
    )
    return {"data": results, "meta": {"total": total, "limit": limit, "offset": offset}}
