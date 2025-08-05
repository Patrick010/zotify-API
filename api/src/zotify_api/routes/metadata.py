from fastapi import APIRouter
from zotify_api.models.metadata import MetadataUpdate, MetadataResponse
from datetime import datetime

router = APIRouter()

mock_metadata = MetadataResponse(
    total_tracks=1234,
    total_playlists=56,
    last_updated=datetime.now(),
    library_size_mb=5678.9
)

@router.get("/metadata", response_model=MetadataResponse, summary="Get all metadata")
def get_all_metadata():
    return mock_metadata

@router.get("/metadata/{track_id}", summary="Get extended metadata for a track")
def get_metadata(track_id: str):
    return {"track_id": track_id, "mood": "Chill", "rating": 4}

@router.patch("/metadata/{track_id}", summary="Update extended metadata for a track")
def patch_metadata(track_id: str, meta: MetadataUpdate):
    return {"status": "updated", "track_id": track_id}
