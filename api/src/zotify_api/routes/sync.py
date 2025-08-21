from typing import Callable

from fastapi import APIRouter, Depends, HTTPException

import zotify_api.services.sync_service as sync_service
from zotify_api.services.auth import require_admin_api_key

router = APIRouter(prefix="/sync", tags=["sync"])


def get_sync_runner() -> Callable:
    return sync_service.run_sync_job


@router.post("/trigger", status_code=202)
def trigger_sync(
    authorized: bool = Depends(require_admin_api_key),
    sync_runner: Callable = Depends(get_sync_runner),
):
    """
    Triggers a global synchronization job.
    In a real app, this would be a background task.
    """
    try:
        sync_runner()
        return {"status": "success", "message": "Synchronization job triggered."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
