from fastapi import APIRouter
from zotify_api.models.metadata import MetadataUpdate

router = APIRouter()

# Simulated backend storage
track_metadata = {
    "abc123": {
        "title": "Track Title",
        "mood": "Chill",
        "rating": 4,
        "source": "Manual Import"
    }
}

@router.get("/metadata/{track_id}", summary="Get extended metadata for a track")
def get_metadata(track_id: str):
    return track_metadata.get(track_id, {"track_id": track_id, "status": "not found"})

@router.patch("/metadata/{track_id}", summary="Update extended metadata for a track")
def patch_metadata(track_id: str, meta: MetadataUpdate):
    if track_id not in track_metadata:
        track_metadata[track_id] = {"title": f"Track {track_id}"}
    for k, v in meta.model_dump(exclude_unset=True).items():
        track_metadata[track_id][k] = v
    return {"status": "updated", "track_id": track_id}
