import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi import HTTPException
from datetime import datetime, timedelta, timezone

from zotify_api.services import deps
from zotify_api.config import settings
from zotify_api.database.models import SpotifyToken
from zotify_api.providers.spotify_connector import SpotifyConnector

def test_get_settings():
    """ Test that get_settings returns the global settings object. """
    assert deps.get_settings() is settings

@pytest.mark.asyncio
@patch("zotify_api.services.deps.crud")
async def test_get_spoti_client_success(mock_crud):
    """ Test successfully getting a SpotiClient with a valid token. """
    mock_token = SpotifyToken(
        access_token="valid_token",
        expires_at=datetime.now(timezone.utc) + timedelta(hours=1)
    )
    mock_crud.get_spotify_token.return_value = mock_token

    client = await deps.get_spoti_client(db=MagicMock())

    assert client._access_token == "valid_token"

@pytest.mark.asyncio
@patch("zotify_api.services.deps.crud")
async def test_get_spoti_client_no_token(mock_crud):
    """ Test that get_spoti_client raises HTTPException if no token is found. """
    mock_crud.get_spotify_token.return_value = None

    with pytest.raises(HTTPException) as exc:
        await deps.get_spoti_client(db=MagicMock())
    assert exc.value.status_code == 401

@pytest.mark.asyncio
@patch("zotify_api.services.deps.SpotiClient.refresh_access_token", new_callable=AsyncMock)
@patch("zotify_api.services.deps.crud")
async def test_get_spoti_client_refreshes_token(mock_crud, mock_refresh):
    """ Test that get_spoti_client refreshes an expired token. """
    expired_token = SpotifyToken(
        access_token="expired_token",
        refresh_token="has_refresh",
        expires_at=datetime.now(timezone.utc) - timedelta(hours=1)
    )
    mock_crud.get_spotify_token.return_value = expired_token

    new_token_data = {"access_token": "new_fresh_token", "expires_in": 3600}
    mock_refresh.return_value = new_token_data

    refreshed_token = SpotifyToken(
        access_token="new_fresh_token",
        expires_at=datetime.now(timezone.utc) + timedelta(hours=1)
    )
    mock_crud.create_or_update_spotify_token.return_value = refreshed_token

    client = await deps.get_spoti_client(db=MagicMock())

    mock_refresh.assert_called_once_with("has_refresh")
    mock_crud.create_or_update_spotify_token.assert_called_once()
    assert client._access_token == "new_fresh_token"

@pytest.mark.asyncio
@patch("zotify_api.services.deps.crud")
async def test_get_spoti_client_expired_no_refresh(mock_crud):
    """ Test get_spoti_client fails if token is expired and has no refresh token. """
    expired_token = SpotifyToken(
        access_token="expired_token",
        refresh_token=None,
        expires_at=datetime.now(timezone.utc) - timedelta(hours=1)
    )
    mock_crud.get_spotify_token.return_value = expired_token

    with pytest.raises(HTTPException) as exc:
        await deps.get_spoti_client(db=MagicMock())
    assert exc.value.status_code == 401
    assert "no refresh token" in exc.value.detail

def test_get_provider_no_auth_success():
    """ Test getting a provider without auth succeeds for a valid provider. """
    provider = deps.get_provider_no_auth("spotify", db=MagicMock())
    assert isinstance(provider, SpotifyConnector)

def test_get_provider_no_auth_not_found():
    """ Test getting a provider without auth fails for an invalid provider. """
    with pytest.raises(HTTPException) as exc:
        deps.get_provider_no_auth("tidal", db=MagicMock())
    assert exc.value.status_code == 404

@pytest.mark.asyncio
async def test_get_provider():
    """ Test the authenticated get_provider dependency. """
    mock_client = MagicMock()
    mock_db = MagicMock()
    provider = await deps.get_provider(db=mock_db, client=mock_client)
    assert isinstance(provider, SpotifyConnector)
    assert provider.client is mock_client
    assert provider.db is mock_db
