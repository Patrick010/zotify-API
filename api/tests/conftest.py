import pytest
from fastapi.testclient import TestClient

from zotify_api.main import app
from zotify_api.config import Settings
from zotify_api.services.deps import get_settings


@pytest.fixture
def client():
    """
    A TestClient instance that can be used in all tests.
    It has the authentication dependency overridden to use a static test API key.
    This fixture is function-scoped to ensure test isolation.
    """
    def get_settings_override():
        # Use app_env='testing' to match the pytest commandline argument
        return Settings(admin_api_key="test_key", app_env="testing")

    # Apply the override
    app.dependency_overrides[get_settings] = get_settings_override

    with TestClient(app) as c:
        yield c

    # Clear all overrides after the test has run
    app.dependency_overrides.clear()


from zotify_api.providers.base import BaseProvider
from zotify_api.services.deps import get_provider
from typing import List, Dict, Any, Tuple
from unittest.mock import AsyncMock

class FakeProvider(BaseProvider):
    """
    A mock provider for testing purposes.
    Implements the BaseProvider interface and returns mock data.
    """
    async def search(self, q: str, type: str, limit: int, offset: int) -> Tuple[List[Dict[str, Any]], int]:
        return [{"id": "test_track"}], 1

    async def get_playlist(self, playlist_id: str) -> Dict[str, Any]:
        return {"id": playlist_id, "name": "Test Playlist"}

    async def get_playlist_tracks(self, playlist_id: str, limit: int, offset: int) -> Dict[str, Any]:
        return {"items": [{"track": {"id": "test_track"}}]}

    async def sync_playlists(self) -> Dict[str, Any]:
        return {"status": "success", "count": 1}


@pytest.fixture
def mock_provider(monkeypatch):
    """
    Fixture to override the get_provider dependency with the FakeProvider.
    """
    fake_provider = FakeProvider()
    app.dependency_overrides[get_provider] = lambda: fake_provider
    yield fake_provider
    app.dependency_overrides.clear()
