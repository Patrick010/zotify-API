from fastapi import APIRouter, Depends, HTTPException
from zotify_api.models.sync import SyncRequest
from zotify_api.services.auth import require_admin_api_key
import zotify_api.services.sync_service as sync_service
from typing import Callable

router = APIRouter(prefix="/sync")

def get_sync_runner() -> Callable:
    return sync_service.run_sync_job

@router.post("/trigger", status_code=200)
def trigger_sync(
    authorized: bool = Depends(require_admin_api_key),
    sync_runner: Callable = Depends(get_sync_runner)
):
    try:
        # In a real app, this would be a background task
        sync_runner()
        return {"status": "scheduled"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Simulated backend storage
playlist_sync_state = {}

@router.post("/playlist/sync", summary="Initiate playlist synchronization")
def playlist_sync(req: SyncRequest):
    playlist_sync_state[req.playlist_id] = {
        "synced_tracks": 18,
        "conflicts": ["track_4", "track_9"]
    }
    return {"status": "ok", **playlist_sync_state[req.playlist_id]}
