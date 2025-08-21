import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session

from zotify_api.config import settings
from zotify_api.services.auth import require_admin_api_key


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

from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from zotify_api.main import app
from zotify_api.providers.base import BaseProvider
from zotify_api.services import deps

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
    from zotify_api.database.models import SpotifyToken
    from zotify_api.services.auth import refresh_spotify_token

    mock_crud.get_spotify_token.return_value = SpotifyToken(refresh_token="some_token")
    mock_refresh.return_value = {"access_token": "new_token", "expires_in": 3600, "refresh_token": "new_refresh"}

    db_session = Session()
    expires_at = await refresh_spotify_token(db=db_session)

    assert isinstance(expires_at, int)
    mock_crud.create_or_update_spotify_token.assert_called_once()

@pytest.mark.asyncio
@patch("zotify_api.services.auth.crud")
async def test_refresh_spotify_token_no_token(mock_crud):
    from zotify_api.services.auth import refresh_spotify_token
    mock_crud.get_spotify_token.return_value = None

    with pytest.raises(HTTPException) as exc:
        await refresh_spotify_token(db=Session())
    assert exc.value.status_code == 401

@patch("zotify_api.services.auth.crud.get_spotify_token")
def test_get_status_no_token(mock_get_token, monkeypatch):
    mock_get_token.return_value = None
    response = client.get("/api/auth/status", headers={"X-API-Key": "test_key"})
    assert response.status_code == 200
    assert response.json()["authenticated"] is False

@patch("zotify_api.services.auth.SpotiClient.get_current_user", new_callable=AsyncMock)
@patch("zotify_api.services.auth.crud.get_spotify_token")
def test_get_status_http_exception(mock_get_token, mock_get_user, monkeypatch):
    from zotify_api.database.models import SpotifyToken
    mock_get_token.return_value = SpotifyToken(
        access_token="valid",
        expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
    )
    mock_get_user.side_effect = HTTPException(status_code=401)

    response = client.get("/api/auth/status", headers={"X-API-Key": "test_key"})
    assert response.status_code == 200
    assert response.json()["token_valid"] is False

@pytest.mark.asyncio
@patch("zotify_api.services.auth.crud")
@patch("zotify_api.services.auth.SpotiClient.exchange_code_for_token", new_callable=AsyncMock)
async def test_handle_spotify_callback(mock_exchange, mock_crud, monkeypatch):
    from zotify_api.services.auth import handle_spotify_callback

    monkeypatch.setitem(__import__("zotify_api.auth_state").auth_state.pending_states, "test_state", "test_verifier")
    mock_exchange.return_value = {"access_token": "acc", "refresh_token": "ref", "expires_in": 3600}

    await handle_spotify_callback("test_code", "test_state", db=Session())

    mock_crud.create_or_update_spotify_token.assert_called_once()


@pytest.mark.asyncio
@patch("zotify_api.services.auth.SpotiClient.exchange_code_for_token", new_callable=AsyncMock)
async def test_handle_spotify_callback_invalid_state(mock_exchange, monkeypatch):
    from zotify_api.services.auth import handle_spotify_callback

    # Ensure state is not in pending_states
    if "test_state" in __import__("zotify_api.auth_state").auth_state.pending_states:
        monkeypatch.delitem(__import__("zotify_api.auth_state").auth_state.pending_states, "test_state")

    with pytest.raises(HTTPException) as exc:
        await handle_spotify_callback("test_code", "test_state", db=Session())
    assert exc.value.status_code == 400
