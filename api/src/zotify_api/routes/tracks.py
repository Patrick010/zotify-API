from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from zotify_api.services.db import get_db_engine
from zotify_api.services import tracks_service
from zotify_api.schemas.tracks import CreateTrackModel, UpdateTrackModel, TrackResponseModel, TrackMetadataRequest, TrackMetadataResponse
from zotify_api.services.auth import require_admin_api_key
from typing import List, Any
from zotify_api.providers.base import BaseProvider
from zotify_api.services.deps import get_provider

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

@router.post("", response_model=TrackResponseModel, status_code=201, dependencies=[Depends(require_admin_api_key)])
def create_track(payload: CreateTrackModel, engine: Any = Depends(get_db_engine)):
    try:
        return tracks_service.create_track(payload.model_dump(), engine)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{track_id}", response_model=TrackResponseModel, dependencies=[Depends(require_admin_api_key)])
def update_track(track_id: str, payload: UpdateTrackModel, engine: Any = Depends(get_db_engine)):
    try:
        return tracks_service.update_track(track_id, payload.model_dump(exclude_unset=True), engine)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{track_id}", status_code=204, dependencies=[Depends(require_admin_api_key)])
def delete_track(track_id: str, engine: Any = Depends(get_db_engine)):
    try:
        tracks_service.delete_track(track_id, engine)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{track_id}/cover", dependencies=[Depends(require_admin_api_key)])
async def upload_track_cover(track_id: str, cover_image: UploadFile = File(...), engine: Any = Depends(get_db_engine)):
    try:
        file_bytes = await cover_image.read()
        return tracks_service.upload_cover(track_id, file_bytes, engine)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/metadata", response_model=TrackMetadataResponse, dependencies=[Depends(require_admin_api_key)])
async def get_metadata(request: TrackMetadataRequest, provider: BaseProvider = Depends(get_provider)):
    """ Returns metadata for all given tracks in one call. """
    if not request.track_ids:
        return TrackMetadataResponse(metadata=[])

    metadata = await tracks_service.get_tracks_metadata_from_spotify(request.track_ids, provider=provider)
    return TrackMetadataResponse(metadata=metadata)
