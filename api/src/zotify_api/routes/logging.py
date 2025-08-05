from fastapi import APIRouter, HTTPException
from zotify_api.models.logging import LogUpdate, LoggingResponse, LogEntry
from typing import List

router = APIRouter()

mock_logs = [
    LogEntry(
        timestamp="2025-08-05T08:00:00Z",
        level="INFO",
        message="Server started",
    ),
    LogEntry(
        timestamp="2025-08-05T08:05:12Z",
        level="WARNING",
        message="Cache nearing capacity",
    ),
]

@router.get("/logging", response_model=LoggingResponse, summary="Get current logging settings")
def get_logging(limit: int = 10, offset: int = 0):
    total = len(mock_logs)
    logs = mock_logs[offset : offset + limit]
    return {"data": logs, "meta": {"total": total, "limit": limit, "offset": offset}}

@router.patch("/logging", summary="Update logging level or target")
def update_logging(update: LogUpdate):
    return {"status": "updated"}
