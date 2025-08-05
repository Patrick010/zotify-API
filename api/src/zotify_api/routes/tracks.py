from fastapi import APIRouter, UploadFile, File
from zotify_api.models.track import Track, TrackMetadata
from typing import List

router = APIRouter()

mock_tracks = [
    Track(id="1", title="Demo Track 1", artist="Artist 1", album="Album 1"),
    Track(id="2", title="Demo Track 2", artist="Artist 2", album="Album 2", genre="Rock", year=2021),
]

@router.get("/tracks", response_model=List[Track], summary="Get all tracks")
def get_tracks():
    return mock_tracks

@router.get("/tracks/{track_id}/metadata", response_model=TrackMetadata, summary="Get metadata for a specific track")
def get_track_metadata(track_id: str):
    track = next((t for t in mock_tracks if t.id == track_id), None)
    if not track:
        return {"track_id": track_id, "status": "not found"}
    return TrackMetadata(
        title=track.title,
        artist=track.artist,
        album=track.album,
        genre=track.genre,
        year=track.year,
    )

@router.patch("/tracks/{track_id}/metadata", response_model=TrackMetadata, summary="Update metadata fields for a track")
def update_track_metadata(track_id: str, metadata: TrackMetadata):
    return metadata

@router.post("/tracks/{track_id}/metadata/refresh", response_model=TrackMetadata, summary="Trigger metadata refresh for a track")
def refresh_track_metadata(track_id: str):
    return TrackMetadata(title="Updated Title", artist="Updated Artist", album="Updated Album")

@router.post("/tracks/{track_id}/cover", summary="Embed or replace cover art for a track")
def upload_cover(track_id: str, cover_image: UploadFile = File(...)):
    return {
        "id": track_id,
        "cover": f"Embedded image: {cover_image.filename}",
    }
