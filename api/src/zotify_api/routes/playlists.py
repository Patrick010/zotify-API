# api/src/zotify_api/routes/playlists.py

from fastapi import APIRouter, Depends, HTTPException, Query

from zotify_api.schemas.playlists import PlaylistIn, PlaylistOut, PlaylistsResponse
from zotify_api.services.playlists_service import PlaylistsService, PlaylistsServiceError, get_playlists_service

router = APIRouter(prefix="/playlists", tags=["playlists"])


@router.get("", response_model=PlaylistsResponse)
def list_playlists(
    limit: int = Query(25, ge=1),
    offset: int = Query(0, ge=0),
    search: str | None = Query(None),
    playlists_service: PlaylistsService = Depends(get_playlists_service),
):
    try:
        items, total = playlists_service.get_playlists(
            limit=limit, offset=offset, search=search
        )
    except PlaylistsServiceError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    return {"data": items, "meta": {"total": total, "limit": limit, "offset": offset}}


@router.post("", response_model=PlaylistOut, status_code=201)
def create_new_playlist(
    payload: PlaylistIn,
    playlists_service: PlaylistsService = Depends(get_playlists_service),
):
    try:
        out = playlists_service.create_playlist(payload.model_dump())
    except PlaylistsServiceError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    return out
