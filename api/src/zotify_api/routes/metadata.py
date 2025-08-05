from fastapi import APIRouter, Depends
from sqlalchemy import create_engine
from zotify_api.config import settings
from zotify_api.models.metadata import MetadataResponse
from zotify_api.services.metadata import get_db_counts, get_library_size_mb

router = APIRouter()

@router.get("/metadata", response_model=MetadataResponse)
def metadata_route():
    try:
        engine = create_engine(settings.database_url)
        total_tracks, total_playlists, last_updated = get_db_counts(engine)
        library_size = get_library_size_mb()
        return {
            "total_tracks": total_tracks,
            "total_playlists": total_playlists,
            "last_updated": last_updated,
            "library_size_mb": library_size
        }
    except Exception as e:
        return {
            "total_tracks": 0,
            "total_playlists": 0,
            "last_updated": None,
            "library_size_mb": 0.0,
            "warning": "metadata backend unavailable"
        }
