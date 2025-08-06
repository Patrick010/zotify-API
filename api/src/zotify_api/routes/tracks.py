from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from zotify_api.services.db import get_db_engine
from zotify_api.services import tracks_service
from zotify_api.schemas.tracks import CreateTrackModel, UpdateTrackModel, TrackResponseModel
from typing import List, Any

router = APIRouter(prefix="/tracks")

@router.get("", response_model=dict)
def list_tracks(limit: int = Query(25, ge=1, le=100), offset: int = 0, q: str | None = None, engine: Any = Depends(get_db_engine)):
    items, total = tracks_service.get_tracks(limit=limit, offset=offset, q=q, engine=engine)
    return {"data": items, "meta": {"total": total, "limit": limit, "offset": offset}}

@router.get("/{track_id}", response_model=TrackResponseModel)
def get_track(track_id: str, engine: Any = Depends(get_db_engine)):
    track = tracks_service.get_track(track_id, engine)
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    return track

@router.post("", response_model=TrackResponseModel, status_code=201)
def create_track(payload: CreateTrackModel, engine: Any = Depends(get_db_engine)):
    try:
        return tracks_service.create_track(payload.model_dump(), engine)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{track_id}", response_model=TrackResponseModel)
def update_track(track_id: str, payload: UpdateTrackModel, engine: Any = Depends(get_db_engine)):
    try:
        return tracks_service.update_track(track_id, payload.model_dump(exclude_unset=True), engine)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{track_id}", status_code=204)
def delete_track(track_id: str, engine: Any = Depends(get_db_engine)):
    try:
        tracks_service.delete_track(track_id, engine)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{track_id}/cover")
async def upload_track_cover(track_id: str, cover_image: UploadFile = File(...), engine: Any = Depends(get_db_engine)):
    try:
        file_bytes = await cover_image.read()
        return tracks_service.upload_cover(track_id, file_bytes, engine)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
