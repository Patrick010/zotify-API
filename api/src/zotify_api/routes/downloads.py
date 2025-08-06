from fastapi import APIRouter, Depends
from zotify_api.schemas.downloads import RetryRequest, DownloadStatusResponse
from zotify_api.schemas.generic import StandardResponse
from zotify_api.services.downloads_service import DownloadsService, get_downloads_service
from zotify_api.services.auth import require_admin_api_key

router = APIRouter(prefix="/downloads")

@router.get("/status", response_model=StandardResponse[DownloadStatusResponse])
def download_status(downloads_service: DownloadsService = Depends(get_downloads_service)):
    return {"data": downloads_service.get_download_status()}

@router.post("/retry", summary="Retry failed downloads", dependencies=[Depends(require_admin_api_key)], response_model=StandardResponse)
def retry_downloads(
    req: RetryRequest,
    downloads_service: DownloadsService = Depends(get_downloads_service)
):
    return {"data": downloads_service.retry_downloads(req.track_ids)}
