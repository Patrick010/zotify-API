from fastapi import APIRouter, Depends
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
from zotify_api.schemas import download as schemas
from zotify_api.services import download_service
from zotify_api.database.session import get_db
from zotify_api.services.auth import require_admin_api_key

router = APIRouter(prefix="/download", tags=["download"])

class DownloadRequest(BaseModel):
    track_ids: List[str]

@router.post("/", response_model=List[schemas.DownloadJob])
def download(
    payload: DownloadRequest,
    db: Session = Depends(get_db),
    _admin: bool = Depends(require_admin_api_key),
):
    """ Queue one or more tracks for download. """
    return download_service.add_downloads_to_queue(db=db, track_ids=payload.track_ids)


@router.get("/status", response_model=schemas.DownloadQueueStatus)
def get_download_queue_status(db: Session = Depends(get_db)):
    """ Get the current status of the download queue. """
    return download_service.get_queue_status(db=db)


@router.post("/retry", response_model=schemas.DownloadQueueStatus)
def retry_failed_downloads(db: Session = Depends(get_db)):
    """ Retry all failed downloads in the queue. """
    download_service.retry_failed_jobs(db=db)
    return download_service.get_queue_status(db=db)


@router.post("/process", response_model=Optional[schemas.DownloadJob])
def process_job(
    db: Session = Depends(get_db),
    _admin: bool = Depends(require_admin_api_key),
):
    """ Manually process one job from the download queue. """
    return download_service.process_download_queue(db=db)
