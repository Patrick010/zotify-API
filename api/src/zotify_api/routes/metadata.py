from fastapi import APIRouter
from zotify_api.models.metadata import MetadataResponse
from zotify_api.services.metadata import get_db_counts, get_library_size_mb
from datetime import datetime

router = APIRouter()

@router.get("/metadata", response_model=MetadataResponse)
def metadata_route():
    total_tracks, total_playlists, last_updated = get_db_counts()
    library_size = get_library_size_mb()
    # Ensure last_updated is a datetime or None; Pydantic can accept None if the model uses Optional[datetime]
    return {
        "total_tracks": total_tracks,
        "total_playlists": total_playlists,
        "last_updated": last_updated,
        "library_size_mb": library_size
    }
