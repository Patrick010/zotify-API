from fastapi import APIRouter, Depends
from zotify_api.schemas.cache import CacheClearRequest, CacheStatusResponse
from zotify_api.schemas.generic import StandardResponse
from zotify_api.services.cache_service import CacheService, get_cache_service
from zotify_api.services.auth import require_admin_api_key

router = APIRouter(prefix="/cache")

@router.get("", response_model=StandardResponse[CacheStatusResponse], summary="Get Cache Stats", description="Returns statistics about the cache.", response_description="Cache statistics.")
def get_cache(cache_service: CacheService = Depends(get_cache_service)):
    return {"data": cache_service.get_cache_status()}

@router.delete("", summary="Clear Cache", description="Clear entire cache or by type.", response_description="Cache statistics after clearing.", dependencies=[Depends(require_admin_api_key)], response_model=StandardResponse[CacheStatusResponse])
def clear_cache(
    req: CacheClearRequest,
    cache_service: CacheService = Depends(get_cache_service)
):
    return {"data": cache_service.clear_cache(req.type)}
