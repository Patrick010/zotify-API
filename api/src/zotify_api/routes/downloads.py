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
        id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
        filename="album1.zip",
        status=DownloadStatus.in_progress,
        progress=42.5,
        started_at="2025-08-01T09:12:34Z",
        finished_at=None,
    ),
    DownloadItem(
        id="7c9e6679-7425-40de-944b-e07fc1f90ae7",
        filename="single_track.mp3",
        status=DownloadStatus.completed,
        progress=100.0,
        started_at="2025-07-30T14:00:00Z",
        finished_at="2025-07-30T14:01:10Z",
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
