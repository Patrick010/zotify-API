from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from zotify_api.database.session import get_db
from zotify_api.schemas import download as schemas
from zotify_api.schemas.generic import StandardResponse
from zotify_api.services import download_service
from zotify_api.services.auth import require_admin_api_key

router = APIRouter(prefix="/downloads", tags=["downloads"])


class DownloadRequest(BaseModel):
    track_ids: List[str]


@router.post("", response_model=StandardResponse[List[schemas.DownloadJob]])
def download(
    payload: DownloadRequest,
    db: Session = Depends(get_db),
    _admin: bool = Depends(require_admin_api_key),
) -> Dict[str, Any]:
    """Queue one or more tracks for download."""
    jobs = download_service.add_downloads_to_queue(db=db, track_ids=payload.track_ids)
    return {"data": jobs}


@router.get("/status", response_model=StandardResponse[schemas.DownloadQueueStatus])
def get_download_queue_status(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Get the current status of the download queue."""
    status = download_service.get_queue_status(db=db)
    return {"data": status}


@router.post("/retry", response_model=StandardResponse[schemas.DownloadQueueStatus])
def retry_failed_downloads(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Retry all failed downloads in the queue."""
    download_service.retry_failed_jobs(db=db)
    status = download_service.get_queue_status(db=db)
    return {"data": status}


@router.post("/process", response_model=StandardResponse[Optional[schemas.DownloadJob]])
def process_job(
    db: Session = Depends(get_db),
    _admin: bool = Depends(require_admin_api_key),
) -> Dict[str, Any]:
    """Manually process one job from the download queue."""
    job = download_service.process_download_queue(db=db)
    return {"data": job}
