from unittest.mock import AsyncMock, MagicMock

import pytest

from zotify_api.main import app
from zotify_api.routes import search


@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Fixture to enable the search feature flag before each test."""
    # Setup: enable the feature flag
    app.dependency_overrides[search.get_feature_flags] = lambda: {"search_enabled": True}
    yield
    # Teardown: clear the override
    del app.dependency_overrides[search.get_feature_flags]


@pytest.mark.asyncio
async def test_search_disabled_by_default(monkeypatch):
    """Test that searching is disabled by default."""
    # Remove the autouse fixture's override
    del app.dependency_overrides[search.get_feature_flags]
    mock_provider = AsyncMock()
    monkeypatch.setattr(search, "get_provider", lambda: mock_provider)
    response = await search.search_zotify("test", "track", 0, 20, mock_provider)
    assert response == ([], 0)


@pytest.mark.asyncio
async def test_search_spotify_fallback(monkeypatch):
    """Test that searching falls back to spotify if the database is empty."""
    mock_provider = MagicMock()
    mock_provider.search.return_value = (
        [
            {
                "id": "local:track:1",
                "name": "test",
                "type": "track",
                "artist": "test",
                "album": "test",
            }
        ],
        1,
    )
    monkeypatch.setattr(search, "get_provider", lambda: mock_provider)
    monkeypatch.setattr(search, "db_search", lambda a, b, c, d: ([], 0))
    response = await search.search_zotify("test", "track", 0, 20, mock_provider)
    mock_provider.search.assert_called_once_with("test", "track", 0, 20)
    assert response[0][0]["id"] == "local:track:1"


@pytest.mark.asyncio
async def test_search_db_flow(monkeypatch):
    """Test that searching the database works as expected."""
    mock_provider = MagicMock()
    monkeypatch.setattr(search, "get_provider", lambda: mock_provider)
    monkeypatch.setattr(
        search,
        "db_search",
        lambda a, b, c, d: (
            [
                {
                    "id": "local:track:1",
                    "name": "test",
                    "type": "track",
                    "artist": "test",
                    "album": "test",
                }
            ]
        ),
    )
    response = await search.search_zotify("test", "track", 0, 20, mock_provider)
    mock_provider.search.assert_not_called()
    assert response[0]["id"] == "local:track:1"


@pytest.mark.asyncio
async def test_search_db_fails_fallback_to_spotify(monkeypatch):
    """Test that searching falls back to spotify if the database search fails."""
    mock_provider = MagicMock()
    monkeypatch.setattr(search, "get_provider", lambda: mock_provider)
    monkeypatch.setattr(
        search, "db_search", lambda a, b, c, d: (_ for _ in ()).throw(Exception("DB Error"))
    )
    mock_provider.search.return_value = (
        [
            {
                "id": "spotify:track:2",
                "name": "test2",
                "type": "track",
                "artist": "test2",
                "album": "test2",
            }
        ],
        1,
    )
    response = await search.search_zotify("test", "track", 0, 20, mock_provider)
    mock_provider.search.assert_called_once_with("test", "track", 0, 20)
    assert response[0][0]["id"] == "spotify:track:2"
