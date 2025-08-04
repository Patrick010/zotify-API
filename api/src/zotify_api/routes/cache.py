from fastapi import APIRouter
from zotify_api.models.cache import CacheClearRequest

router = APIRouter()

# In-memory state
cache_state = {
    "search": 80,
    "metadata": 222
}

@router.get("/cache", summary="Get cache statistics")
def get_cache():
    return {
        "total_items": sum(cache_state.values()),
        "by_type": cache_state
    }

@router.delete("/cache", summary="Clear entire cache or by type")
def clear_cache(req: CacheClearRequest):
    if req.type:
        if req.type in cache_state:
            cache_state[req.type] = 0
        else:
            # Or raise an error, depending on desired behavior
            pass
    else:
        for k in cache_state:
            cache_state[k] = 0
    return {"status": "cleared", "by_type": cache_state}
