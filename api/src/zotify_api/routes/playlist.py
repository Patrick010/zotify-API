# api/src/zotify_api/routes/playlists.py
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Any
from pydantic import BaseModel, Field
from zotify_api.services.playlists_service import get_playlists, create_playlist, PlaylistsServiceError, get_default_limit
from zotify_api.services.db import get_db_engine  # existing helper that returns None in dev when DB missing

router = APIRouter(prefix="/playlists", tags=["playlists"])

class PlaylistIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(None, max_length=1000)

class PlaylistOut(BaseModel):
    id: str | None = None
    name: str
    description: str | None = None

class PlaylistsResponse(BaseModel):
    data: List[PlaylistOut]
    meta: dict

@router.get("", response_model=PlaylistsResponse)
def list_playlists(
    limit: int = Query(get_default_limit(), ge=1),
    offset: int = Query(0, ge=0),
    search: str | None = Query(None),
    db_engine = Depends(get_db_engine),
):
    try:
        items, total = get_playlists(db_engine, limit=limit, offset=offset, search=search)
    except PlaylistsServiceError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    return {"data": items, "meta": {"total": total, "limit": limit, "offset": offset}}

@router.post("", response_model=PlaylistOut, status_code=201)
def create_new_playlist(payload: PlaylistIn, db_engine = Depends(get_db_engine)):
    try:
        out = create_playlist(db_engine, payload.model_dump())
    except PlaylistsServiceError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    return out
