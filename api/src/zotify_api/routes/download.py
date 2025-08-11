from fastapi import APIRouter, Depends
from typing import List
from pydantic import BaseModel
from zotify_api.schemas.download import DownloadQueueStatus, DownloadJob
from zotify_api.services.download_service import DownloadsService, get_downloads_service
from zotify_api.services.auth import require_admin_api_key

router = APIRouter(prefix="/download", tags=["download"])

class DownloadRequest(BaseModel):
    track_ids: List[str]

@router.post("/", response_model=List[DownloadJob])
def download(
    payload: DownloadRequest,
    downloads_service: DownloadsService = Depends(get_downloads_service),
    _admin: bool = Depends(require_admin_api_key),
):
    """ Queue one or more tracks for download. """
    return downloads_service.add_downloads_to_queue(payload.track_ids)


@router.get("/status", response_model=DownloadQueueStatus)
def get_download_queue_status(
    downloads_service: DownloadsService = Depends(get_downloads_service)
):
    """ Get the current status of the download queue. """
    return downloads_service.get_queue_status()


@router.post("/retry", response_model=DownloadQueueStatus)
def retry_failed_downloads(
    downloads_service: DownloadsService = Depends(get_downloads_service)
):
    """ Retry all failed downloads in the queue. """
    return downloads_service.retry_failed_jobs()
