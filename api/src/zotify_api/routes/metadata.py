from fastapi import APIRouter
from zotify_api.models.metadata import MetadataUpdate, MetadataResponse
from datetime import datetime

router = APIRouter()

mock_metadata = MetadataResponse(
    total_tracks=5421,
    total_playlists=128,
    last_updated="2025-08-04T18:00:00Z",
    library_size_mb=12345.67
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
