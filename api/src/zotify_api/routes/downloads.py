from fastapi import APIRouter
from zotify_api.models.downloads import RetryRequest

router = APIRouter()

# Simulated backend storage
download_state = {
    "in_progress": [],
    "failed": {"track_7": "Network error", "track_10": "404 not found"},
    "completed": ["track_3", "track_5"]
}

@router.get("/downloads", summary="Get status of download queue")
def download_status():
    return download_state

@router.post("/downloads/retry", summary="Retry failed downloads")
def retry_downloads(req: RetryRequest):
    for tid in req.track_ids:
        if tid in download_state["failed"]:
            download_state["in_progress"].append(tid)
            del download_state["failed"][tid]
    return {"retried": req.track_ids, "queued": True}
