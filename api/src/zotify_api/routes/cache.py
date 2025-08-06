from fastapi import APIRouter, Depends
from zotify_api.schemas.cache import CacheClearRequest, CacheStatusResponse
from zotify_api.services.cache_service import CacheService, get_cache_service
from zotify_api.services.auth import require_admin_api_key

router = APIRouter(prefix="/cache")

@router.get("", response_model=CacheStatusResponse)
def get_cache(cache_service: CacheService = Depends(get_cache_service)):
    return cache_service.get_cache_status()

@router.delete("", summary="Clear entire cache or by type", dependencies=[Depends(require_admin_api_key)])
def clear_cache(
    req: CacheClearRequest,
    cache_service: CacheService = Depends(get_cache_service)
):
    return cache_service.clear_cache(req.type)
