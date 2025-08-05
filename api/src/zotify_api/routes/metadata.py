from fastapi import APIRouter
from zotify_api.models.metadata import MetadataResponse
from zotify_api.services.metadata import get_db_counts, get_library_size_mb
from zotify_api.services.db import get_db_engine

router = APIRouter()

@router.get("/metadata", response_model=MetadataResponse)
def metadata_route():
    engine = get_db_engine()
    if engine is None:
        return {
            "total_tracks": 0,
            "total_playlists": 0,
            "last_updated": None,
            "library_size_mb": 0.0,
            "warning": "metadata backend unavailable"
        }
    total_tracks, total_playlists, last_updated = get_db_counts()
    library_size = get_library_size_mb()
    return {
        "total_tracks": total_tracks,
        "total_playlists": total_playlists,
        "last_updated": last_updated,
        "library_size_mb": library_size
    }
