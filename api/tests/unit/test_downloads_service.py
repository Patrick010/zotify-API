import pytest
from zotify_api.services.downloads_service import DownloadsService

@pytest.fixture
def download_state():
    return {
        "in_progress": [],
        "failed": {"track_7": "Network error", "track_10": "404 not found"},
        "completed": ["track_3", "track_5"]
    }

def test_get_download_status(download_state):
    service = DownloadsService(download_state)
    status = service.get_download_status()
    assert status == download_state

def test_retry_downloads(download_state):
    service = DownloadsService(download_state)
    result = service.retry_downloads(["track_7"])
    assert result == {"retried": ["track_7"], "queued": True}
    assert "track_7" in service.get_download_status()["in_progress"]
    assert "track_7" not in service.get_download_status()["failed"]

def test_retry_downloads_no_failed(download_state):
    service = DownloadsService(download_state)
    result = service.retry_downloads(["track_1"])
    assert result == {"retried": ["track_1"], "queued": True}
    assert "track_1" not in service.get_download_status()["in_progress"]
