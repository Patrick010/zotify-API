import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException

from zotify_api.services import deps
from zotify_api.config import settings
from zotify_api.providers.spotify_connector import SpotifyConnector


def test_get_settings():
    """ Tests that the get_settings dependency returns the global settings object. """
    assert deps.get_settings() is settings


def test_get_provider_no_auth_success():
    """ Tests that the correct provider is returned without authentication. """
    provider = deps.get_provider_no_auth(provider_name="spotify", db=MagicMock())
    assert isinstance(provider, SpotifyConnector)


def test_get_provider_no_auth_not_found():
    """ Tests that an HTTPException is raised for an unknown provider. """
    with pytest.raises(HTTPException) as exc:
        deps.get_provider_no_auth(provider_name="tidal", db=MagicMock())
    assert exc.value.status_code == 404


from unittest.mock import patch, AsyncMock
from zotify_api.database import models
from datetime import datetime, timedelta, timezone

@pytest.mark.asyncio
@patch("zotify_api.services.deps.crud")
async def test_get_spoti_client_success(mock_crud):
    """ Tests that a SpotiClient is returned when a valid token exists. """
    mock_db = MagicMock()
    mock_token = models.SpotifyToken(
        access_token="valid_token",
        expires_at=datetime.now(timezone.utc) + timedelta(hours=1)
    )
    mock_crud.get_spotify_token.return_value = mock_token

    client = await deps.get_spoti_client(db=mock_db)

    assert client._access_token == "valid_token"


@pytest.mark.asyncio
@patch("zotify_api.services.deps.crud")
async def test_get_spoti_client_no_token(mock_crud):
    """ Tests that an HTTPException is raised when no token is found. """
    mock_db = MagicMock()
    mock_crud.get_spotify_token.return_value = None

    with pytest.raises(HTTPException) as exc:
        await deps.get_spoti_client(db=mock_db)

    assert exc.value.status_code == 401
    assert "Not authenticated" in exc.value.detail


@pytest.mark.asyncio
@patch("zotify_api.services.deps.SpotiClient.refresh_access_token", new_callable=AsyncMock)
@patch("zotify_api.services.deps.crud")
async def test_get_spoti_client_refreshes_token(mock_crud, mock_refresh):
    """ Tests that the client dependency successfully refreshes an expired token. """
    mock_db = MagicMock()
    mock_expired_token = models.SpotifyToken(
        access_token="expired_token",
        refresh_token="valid_refresh_token",
        expires_at=datetime.now(timezone.utc) - timedelta(hours=1)
    )
    mock_crud.get_spotify_token.return_value = mock_expired_token
    mock_refresh.return_value = {"access_token": "refreshed_token", "expires_in": 3600}

    # This mock is for the final return value after the refresh
    mock_crud.create_or_update_spotify_token.return_value = models.SpotifyToken(
        access_token="refreshed_token",
        refresh_token="valid_refresh_token",
        expires_at=datetime.now(timezone.utc) + timedelta(hours=1)
    )

    client = await deps.get_spoti_client(db=mock_db)

    mock_refresh.assert_awaited_once_with("valid_refresh_token")
    mock_crud.create_or_update_spotify_token.assert_called_once()
    assert client._access_token == "refreshed_token"


@pytest.mark.asyncio
@patch("zotify_api.services.deps.crud")
async def test_get_spoti_client_expired_no_refresh(mock_crud):
    """ Tests that an HTTPException is raised for an expired token with no refresh token. """
    mock_db = MagicMock()
    mock_expired_token = models.SpotifyToken(
        access_token="expired_token",
        refresh_token=None,
        expires_at=datetime.now(timezone.utc) - timedelta(hours=1)
    )
    mock_crud.get_spotify_token.return_value = mock_expired_token

    with pytest.raises(HTTPException) as exc:
        await deps.get_spoti_client(db=mock_db)

    assert exc.value.status_code == 401
    assert "no refresh token is available" in exc.value.detail
