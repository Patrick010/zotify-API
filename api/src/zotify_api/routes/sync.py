from fastapi import APIRouter, Depends
from zotify_api.models.sync import SyncRequest
from zotify_api.deps.auth import require_admin_api_key
import zotify_api.services.sync as sync_service

router = APIRouter(prefix="/sync")

# Simulated backend storage
playlist_sync_state = {}

@router.post("/playlist/sync", summary="Initiate playlist synchronization")
def playlist_sync(req: SyncRequest):
    playlist_sync_state[req.playlist_id] = {
        "synced_tracks": 18,
        "conflicts": ["track_4", "track_9"]
    }
    return {"status": "ok", **playlist_sync_state[req.playlist_id]}

@router.post("/trigger", status_code=200)
def trigger_sync(authorized: bool = Depends(require_admin_api_key)):
    # In a real app, this would be a background task
    sync_service.run_sync_job()
    return {"status": "scheduled"}
