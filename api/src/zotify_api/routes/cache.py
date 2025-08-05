from fastapi import APIRouter
from zotify_api.models.cache import CacheStats
from zotify_api.services.cache import get_cache_stats
import redis

router = APIRouter()

@router.get("/cache", response_model=CacheStats)
def cache_route():
    stats = get_cache_stats()
    # convert last_cleared to datetime if needed; set default
    from datetime import datetime
    if stats["last_cleared"] is None:
        stats["last_cleared"] = datetime.utcnow()
    return stats
