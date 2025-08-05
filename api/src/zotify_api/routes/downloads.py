from fastapi import APIRouter
from zotify_api.models.downloads import (
    RetryRequest,
    DownloadItem,
    DownloadStatus,
    DownloadsResponse,
)
from typing import List
from uuid import uuid4
from datetime import datetime, timedelta

router = APIRouter()

# Simulated backend storage
mock_downloads = [
    DownloadItem(
        id=uuid4(),
        filename="track1.mp3",
        status=DownloadStatus.completed,
        progress=100.0,
        started_at=datetime.now() - timedelta(minutes=5),
        finished_at=datetime.now() - timedelta(minutes=4),
    ),
    DownloadItem(
        id=uuid4(),
        filename="track2.mp3",
        status=DownloadStatus.in_progress,
        progress=50.0,
        started_at=datetime.now() - timedelta(minutes=2),
    ),
    DownloadItem(
        id=uuid4(),
        filename="track3.mp3",
        status=DownloadStatus.failed,
        progress=0.0,
        started_at=datetime.now() - timedelta(minutes=1),
    ),
    DownloadItem(
        id=uuid4(),
        filename="track4.mp3",
        status=DownloadStatus.pending,
        progress=0.0,
        started_at=datetime.now(),
    ),
]

@router.get("/downloads", response_model=DownloadsResponse, summary="Get status of download queue")
def download_status(
    limit: int = 10, offset: int = 0, status: DownloadStatus = None
):
    downloads = mock_downloads
    if status:
        downloads = [d for d in downloads if d.status == status]
    total = len(downloads)
    downloads = downloads[offset : offset + limit]
    return {"data": downloads, "meta": {"total": total, "limit": limit, "offset": offset}}

@router.post("/downloads/retry", summary="Retry failed downloads")
def retry_downloads(req: RetryRequest):
    return {"retried": req.track_ids, "queued": True}
