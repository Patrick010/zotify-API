from fastapi import APIRouter
from zotify_api.models.sync import SyncJob, SyncStatus, SyncResponse
from typing import List

router = APIRouter()

mock_sync_jobs = [
    SyncJob(
        id="c9bf9e57-1685-4c89-bafb-ff5af830be8a",
        status=SyncStatus.running,
        progress=23.7,
        started_at="2025-08-05T07:00:00Z",
        finished_at=None,
    ),
    SyncJob(
        id="a3bb189e-8bf9-3888-9912-ace4e6543002",
        status=SyncStatus.completed,
        progress=100.0,
        started_at="2025-07-28T10:00:00Z",
        finished_at="2025-07-28T10:10:00Z",
    ),
]

@router.get("/sync", response_model=SyncResponse, summary="Get sync status")
def get_sync_status(limit: int = 10, offset: int = 0):
    total = len(mock_sync_jobs)
    jobs = mock_sync_jobs[offset : offset + limit]
    return {"data": jobs, "meta": {"total": total, "limit": limit, "offset": offset}}
