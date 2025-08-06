"""
Downloads service module.

This module contains the business logic for the downloads subsystem.
The functions in this module are designed to be called from the API layer.
"""
from typing import Dict, Any, List

class DownloadsService:
    def __init__(self, download_state: Dict[str, Any]):
        self._download_state = download_state

    def get_download_status(self) -> Dict[str, Any]:
        return self._download_state

    def retry_downloads(self, track_ids: List[str]) -> Dict[str, Any]:
        for tid in track_ids:
            if tid in self._download_state["failed"]:
                self._download_state["in_progress"].append(tid)
                del self._download_state["failed"][tid]
        return {"retried": track_ids, "queued": True}

def get_downloads_service():
    # This is a placeholder for a real implementation that would get the download state from a persistent storage.
    download_state = {
        "in_progress": [],
        "failed": {"track_7": "Network error", "track_10": "404 not found"},
        "completed": ["track_3", "track_5"]
    }
    return DownloadsService(download_state)
