import pytest
from fastapi import HTTPException
from zotify_api.services.auth import require_admin_api_key
from zotify_api.config import settings
from zotify_api.database import models

def test_no_admin_key_config(monkeypatch):
    monkeypatch.setattr(settings, "admin_api_key", None)
    with pytest.raises(HTTPException) as exc:
        require_admin_api_key(x_api_key=None, settings=settings)
    assert exc.value.status_code == 503

def test_wrong_key(monkeypatch):
    monkeypatch.setattr(settings, "admin_api_key", "test_key")
    with pytest.raises(HTTPException) as exc:
        require_admin_api_key(x_api_key="bad", settings=settings)
    assert exc.value.status_code == 401

from fastapi.testclient import TestClient
from zotify_api.main import app
from unittest.mock import patch, AsyncMock, ANY, MagicMock
from zotify_api.services import deps
from zotify_api.providers.base import BaseProvider

client = TestClient(app)

def test_correct_key(monkeypatch):
    monkeypatch.setattr(settings, "admin_api_key", "test_key")
    assert require_admin_api_key(x_api_key="test_key", settings=settings) is True

def test_provider_callback_route(monkeypatch):
    """
    Tests that the generic provider callback route correctly invokes the
    provider's handle_oauth_callback method.
    """
    mock_provider = AsyncMock(spec=BaseProvider)
    mock_provider.handle_oauth_callback.return_value = "<html>Success</html>"

    def mock_get_provider_no_auth(provider_name: str):
        return mock_provider

    app.dependency_overrides[deps.get_provider_no_auth] = mock_get_provider_no_auth

    response = client.get("/api/auth/spotify/callback?code=test_code&state=test_state&error=test_error")

    assert response.status_code == 200
    assert response.text == "<html>Success</html>"
    mock_provider.handle_oauth_callback.assert_awaited_once_with(
        code="test_code", state="test_state", error="test_error"
    )

    # Clean up the override
    app.dependency_overrides = {}


from datetime import datetime, timedelta, timezone

@patch("zotify_api.services.auth.SpotiClient.get_current_user", new_callable=AsyncMock)
@patch("zotify_api.services.auth.crud.get_spotify_token")
def test_get_status_authenticated_and_token_not_expired(mock_get_token, mock_get_user, monkeypatch):
    """
    Tests that /api/auth/status returns authenticated if a valid, non-expired token exists.
    """
    monkeypatch.setattr(settings, "admin_api_key", "test_key")
    mock_get_user.return_value = {"id": "test_user"}

    class MockToken:
        def __init__(self, expires_at):
            self.expires_at = expires_at
            self.user_id = "test_user"
            self.access_token = "mock_access_token"

    mock_get_token.return_value = MockToken(expires_at=datetime.now(timezone.utc) + timedelta(hours=1))

    response = client.get("/api/auth/status", headers={"X-API-Key": "test_key"})

    assert response.status_code == 200
    data = response.json()
    assert data["authenticated"] is True
    assert data["user_id"] == "test_user"

@patch("zotify_api.services.auth.crud.get_spotify_token")
def test_get_status_token_expired(mock_get_token, monkeypatch):
    """
    Tests that /api/auth/status returns not authenticated if the token is expired.
    """
    monkeypatch.setattr(settings, "admin_api_key", "test_key")

    class MockToken:
        def __init__(self, expires_at):
            self.expires_at = expires_at
            self.user_id = "test_user"
            self.access_token = "mock_access_token"

    mock_get_token.return_value = MockToken(expires_at=datetime.now(timezone.utc) - timedelta(hours=1))

    response = client.get("/api/auth/status", headers={"X-API-Key": "test_key"})

    assert response.status_code == 200
    data = response.json()
    assert data["authenticated"] is False


@pytest.mark.asyncio
@patch("zotify_api.services.auth.crud")
@patch("zotify_api.services.auth.SpotiClient.refresh_access_token", new_callable=AsyncMock)
async def test_refresh_spotify_token_success(mock_refresh, mock_crud):
    """ Tests that refresh_spotify_token successfully gets and saves a new token. """
    # Arrange
    mock_db = MagicMock()
    mock_crud.get_spotify_token.return_value = models.SpotifyToken(refresh_token="old_refresh")

    new_token_info = {"access_token": "new_access", "refresh_token": "new_refresh", "expires_in": 3600}
    mock_refresh.return_value = new_token_info

    mock_crud.create_or_update_spotify_token.return_value = models.SpotifyToken(
        expires_at=datetime.now(timezone.utc) + timedelta(seconds=3600)
    )

    # Act
    from zotify_api.services.auth import refresh_spotify_token
    new_timestamp = await refresh_spotify_token(db=mock_db)

    # Assert
    mock_refresh.assert_awaited_once_with("old_refresh")
    mock_crud.create_or_update_spotify_token.assert_called_once()
    assert isinstance(new_timestamp, int)


@pytest.mark.asyncio
@patch("zotify_api.services.auth.crud")
async def test_refresh_spotify_token_no_token(mock_crud):
    """ Tests that refresh_spotify_token fails if no token is in the DB. """
    mock_db = MagicMock()
    mock_crud.get_spotify_token.return_value = None

    from zotify_api.services.auth import refresh_spotify_token
    with pytest.raises(HTTPException) as exc:
        await refresh_spotify_token(db=mock_db)

    assert exc.value.status_code == 401


@pytest.mark.asyncio
@patch("zotify_api.services.auth.crud.get_spotify_token")
async def test_get_status_no_token(mock_get_token):
    """ Tests that /api/auth/status returns not authenticated if no token exists. """
    mock_get_token.return_value = None

    from zotify_api.services.auth import get_auth_status
    status = await get_auth_status(db=MagicMock())

    assert status.authenticated is False
    assert status.token_valid is False


@pytest.mark.asyncio
@patch("zotify_api.services.auth.SpotiClient.get_current_user", new_callable=AsyncMock)
@patch("zotify_api.services.auth.crud.get_spotify_token")
async def test_get_status_http_exception(mock_get_token, mock_get_user):
    """ Tests that get_auth_status handles non-401 HTTPExceptions from the client. """
    mock_get_user.side_effect = HTTPException(status_code=500, detail="Internal Error")

    class MockToken:
        expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
        access_token = "mock_access_token"

    mock_get_token.return_value = MockToken()

    from zotify_api.services.auth import get_auth_status
    with pytest.raises(HTTPException) as exc:
        await get_auth_status(db=MagicMock())

    assert exc.value.status_code == 500


@pytest.mark.asyncio
@patch("zotify_api.services.auth.crud")
@patch("zotify_api.services.auth.SpotiClient.exchange_code_for_token", new_callable=AsyncMock)
async def test_handle_spotify_callback(mock_exchange, mock_crud, monkeypatch):
    """ Tests the main success path of the spotify callback handler. """
    mock_db = MagicMock()
    monkeypatch.setitem(__import__("zotify_api.auth_state").auth_state.pending_states, "test_state", "test_verifier")
    mock_exchange.return_value = {
        "access_token": "new_access",
        "refresh_token": "new_refresh",
        "expires_in": 3600,
    }

    from zotify_api.services.auth import handle_spotify_callback
    await handle_spotify_callback(code="test_code", state="test_state", db=mock_db)

    mock_exchange.assert_awaited_once_with("test_code", "test_verifier")
    mock_crud.create_or_update_spotify_token.assert_called_once()


@pytest.mark.asyncio
async def test_handle_spotify_callback_invalid_state(monkeypatch):
    """ Tests that the callback fails with an invalid state. """
    mock_db = MagicMock()
    monkeypatch.setitem(__import__("zotify_api.auth_state").auth_state.pending_states, "good_state", "good_verifier")

    from zotify_api.services.auth import handle_spotify_callback
    with pytest.raises(HTTPException) as exc:
        await handle_spotify_callback(code="test_code", state="bad_state", db=mock_db)

    assert exc.value.status_code == 400
