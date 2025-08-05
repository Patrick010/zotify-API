from fastapi import APIRouter, Query
from zotify_api.models.logging import LoggingResponse, LogEntry
from zotify_api.services.logs import read_recent_logs

router = APIRouter()

@router.get("/logging", response_model=LoggingResponse)
def logging_route(limit: int = Query(10, ge=1, le=100), offset: int = 0, level: str | None = None):
    logs = read_recent_logs(limit=limit, level=level)
    meta = {"total": len(logs), "limit": limit, "offset": offset}
    return {"data": logs, "meta": meta}
