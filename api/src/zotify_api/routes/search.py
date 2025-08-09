"""
Search route with dependency injection for feature flags, database engine, and Spotify search function.

This module provides a search endpoint that can use either a local database or Spotify as a search backend.
The choice of backend is determined by the availability of a database engine.
The advanced search feature can be enabled or disabled using feature flags.

Dependencies are injected using FastAPI's dependency injection system, which makes the route easy to test.
To test the different code paths, you can override the dependencies in your tests.

Example of overriding the feature flags dependency:
    def get_feature_flags_override():
        return {"fork_features": False, "search_advanced": False}
    app.dependency_overrides[search.get_feature_flags] = get_feature_flags_override

Example of overriding the database engine dependency:
    def get_db_engine_override():
        return None
    app.dependency_overrides[search.get_db_engine] = get_db_engine_override

Example of overriding the Spotify search function dependency:
    def get_spotify_search_func_override():
        return lambda q, type, limit, offset: ([{"id": "spotify:track:1"}], 1)
    app.dependency_overrides[search.get_spotify_search_func] = get_spotify_search_func_override
"""
from fastapi import APIRouter, Query, HTTPException, Depends
from zotify_api.config import settings
import zotify_api.services.db as db_service
import zotify_api.services.search as search_service
from zotify_api.services.spotify import search_spotify
from typing import Callable

router = APIRouter(prefix="/search")

def get_feature_flags():
    return {
        "fork_features": settings.enable_fork_features,
        "search_advanced": settings.feature_search_advanced
    }

def get_db_engine():
    return db_service.get_db_engine()

def get_spotify_search_func():
    return search_spotify

from typing import Literal

@router.get("")
def search(
    q: str = Query(...),
    type: Literal["track", "album", "artist", "playlist", "all"] = "all",
    limit: int = 20,
    offset: int = 0,
    feature_flags: dict = Depends(get_feature_flags),
    db_engine: any = Depends(get_db_engine),
    spotify_search_func: Callable = Depends(get_spotify_search_func)
):
    if not feature_flags["fork_features"] or not feature_flags["search_advanced"]:
        raise HTTPException(status_code=404, detail="Advanced search disabled")

    results, total = search_service.perform_search(
        q,
        type=type,
        limit=limit,
        offset=offset,
        db_engine=db_engine,
        spotify_search_func=spotify_search_func,
    )
    return {"data": results, "meta": {"total": total, "limit": limit, "offset": offset}}
