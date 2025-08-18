import pytest
from fastapi import HTTPException
from zotify_api.services.auth import require_admin_api_key
from zotify_api.config import settings

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
from unittest.mock import patch, AsyncMock, ANY

client = TestClient(app)

def test_correct_key(monkeypatch):
    monkeypatch.setattr(settings, "admin_api_key", "test_key")
    assert require_admin_api_key(x_api_key="test_key", settings=settings) is True

@patch("httpx.AsyncClient.post", new_callable=AsyncMock)
@patch("zotify_api.routes.auth.crud.create_or_update_spotify_token")
def test_spotify_callback_success(mock_crud_call, mock_httpx_post, client, monkeypatch):
    """
    Tests the new GET /auth/spotify/callback endpoint.
    """
    # Mock the response from Spotify's token endpoint
    mock_httpx_post.return_value.json = AsyncMock(return_value={
        "access_token": "test_access_token",
        "refresh_token": "test_refresh_token",
        "expires_in": 3600
    })
    mock_httpx_post.return_value.raise_for_status.return_value = None

    # Set up the pending state
    monkeypatch.setitem(__import__("zotify_api.auth_state").auth_state.pending_states, "test_state", "test_code_verifier")

    response = client.get("/api/auth/spotify/callback?code=test_code&state=test_state")

    assert response.status_code == 200
    assert response.json()["status"] == "success"

    # Check that the token was saved to the DB
    mock_crud_call.assert_called_once()


from datetime import datetime, timedelta, timezone

@patch("zotify_api.services.auth.SpotiClient.get_current_user", new_callable=AsyncMock)
@patch("zotify_api.services.auth.crud.get_spotify_token")
def test_get_status_authenticated_and_token_not_expired(mock_get_token, mock_get_user, monkeypatch):
    """
    Tests that /api/auth/status returns authenticated if a valid, non-expired token exists.
    This also implicitly tests the timezone comparison fix.
    """
    monkeypatch.setattr(settings, "admin_api_key", "test_key")
    mock_get_user.return_value = {"id": "test_user"}

    # Mock a token that expires in the future
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

    # Mock a token that has already expired
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
