from unittest.mock import AsyncMock, MagicMock

import pytest

from zotify_api.main import app
from zotify_api.routes import search


def test_search_disabled_by_default(client, mock_provider):
    app.dependency_overrides[search.get_feature_flags] = lambda: {
        "fork_features": False,
        "search_advanced": False,
    }
    response = client.get(
        "/api/search", params={"q": "test"}, headers={"X-API-Key": "test_key"}
    )
    assert response.status_code == 404
    del app.dependency_overrides[search.get_feature_flags]


@pytest.mark.asyncio
async def test_search_spotify_fallback(client):
    app.dependency_overrides[search.get_feature_flags] = lambda: {
        "fork_features": True,
        "search_advanced": True,
    }
    app.dependency_overrides[search.get_db_engine] = lambda: None
    mock_provider = MagicMock()
    mock_provider.search = AsyncMock(
        return_value=(
            [
                {
                    "id": "spotify:track:1",
                    "name": "test",
                    "type": "track",
                    "artist": "test",
                    "album": "test",
                }
            ],
            1,
        )
    )
    app.dependency_overrides[search.get_provider] = lambda: mock_provider

    response = client.get(
        "/api/search", params={"q": "test"}, headers={"X-API-Key": "test_key"}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["data"][0]["id"] == "spotify:track:1"
    mock_provider.search.assert_awaited_once()

    del app.dependency_overrides[search.get_feature_flags]
    del app.dependency_overrides[search.get_db_engine]
    del app.dependency_overrides[search.get_provider]


def test_search_db_flow(client, mock_provider):
    app.dependency_overrides[search.get_feature_flags] = lambda: {
        "fork_features": True,
        "search_advanced": True,
    }
    mock_engine = MagicMock()
    mock_conn = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = mock_conn
    mock_conn.execute.return_value.mappings.return_value.all.return_value = [
        {
            "id": "local:track:1",
            "name": "test",
            "type": "track",
            "artist": "test",
            "album": "test",
        }
    ]
    app.dependency_overrides[search.get_db_engine] = lambda: mock_engine

    response = client.get(
        "/api/search", params={"q": "test"}, headers={"X-API-Key": "test_key"}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["data"][0]["id"] == "local:track:1"

    del app.dependency_overrides[search.get_feature_flags]
    del app.dependency_overrides[search.get_db_engine]


@pytest.mark.asyncio
async def test_search_db_fails_fallback_to_spotify(client):
    app.dependency_overrides[search.get_feature_flags] = lambda: {
        "fork_features": True,
        "search_advanced": True,
    }
    mock_engine = MagicMock()
    mock_engine.connect.side_effect = Exception("DB error")
    app.dependency_overrides[search.get_db_engine] = lambda: mock_engine
    mock_provider = MagicMock()
    mock_provider.search = AsyncMock(
        return_value=(
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
    )
    app.dependency_overrides[search.get_provider] = lambda: mock_provider

    response = client.get(
        "/api/search", params={"q": "test"}, headers={"X-API-Key": "test_key"}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["data"][0]["id"] == "spotify:track:2"
    mock_provider.search.assert_awaited_once()

    del app.dependency_overrides[search.get_feature_flags]
    del app.dependency_overrides[search.get_db_engine]
    del app.dependency_overrides[search.get_provider]
