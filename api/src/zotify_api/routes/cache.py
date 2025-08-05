from fastapi import APIRouter
from zotify_api.models.cache import CacheClearRequest, CacheResponse
from datetime import datetime

router = APIRouter()

mock_cache_data = CacheResponse(
    total_items=421,
    memory_usage_mb=128.5,
    hit_rate=87.3,
    last_cleared="2025-08-01T00:00:00Z",
)

@router.get("/cache", response_model=CacheResponse, summary="Get cache statistics")
def get_cache():
    return mock_cache_data

@router.delete("/cache", summary="Clear entire cache or by type")
def clear_cache(req: CacheClearRequest):
    return {"status": "cleared"}
