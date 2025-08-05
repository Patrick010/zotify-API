from fastapi import APIRouter, UploadFile, File
from zotify_api.models.track import TrackMetadata

router = APIRouter()

@router.get("/tracks", summary="Get all tracks")
def get_tracks():
    return [{"id": "1", "title": "Demo Track 1"}, {"id": "2", "title": "Demo Track 2"}]

@router.get("/tracks/{track_id}/metadata", summary="Get metadata for a specific track")
def get_track_metadata(track_id: str):
    return {"id": track_id, "title": "Demo", "artist": "Artist", "album": "Album", "genre": "Rock", "year": 2020}

@router.patch("/tracks/{track_id}/metadata", summary="Update metadata fields for a track")
def update_track_metadata(track_id: str, metadata: TrackMetadata):
    return {**{"id": track_id}, **metadata.model_dump(exclude_unset=True)}

@router.post("/tracks/{track_id}/metadata/refresh", summary="Trigger metadata refresh for a track")
def refresh_track_metadata(track_id: str):
    return {"id": track_id, "title": "Updated", "artist": "New Artist", "album": "Updated Album"}

@router.post("/tracks/{track_id}/cover", summary="Embed or replace cover art for a track")
def upload_cover(track_id: str, cover_image: UploadFile = File(...)):
    return {
        "id": track_id,
        "cover": f"Embedded image: {cover_image.filename}",
    }
