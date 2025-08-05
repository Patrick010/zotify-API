from fastapi import APIRouter
from zotify_api.models.sync import SyncRequest

router = APIRouter()

# Simulated backend storage
playlist_sync_state = {}

@router.get("/sync", summary="Get sync status")
def get_sync_status():
    return {"status": "Sync is active", "details": "Ready to sync."}

@router.post("/sync/playlist", summary="Initiate playlist synchronization")
def playlist_sync(req: SyncRequest):
    playlist_sync_state[req.playlist_id] = {
        "synced_tracks": 18,
        "conflicts": ["track_4", "track_9"]
    }
    return {"status": "ok", **playlist_sync_state[req.playlist_id]}
