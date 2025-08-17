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
    mock_httpx_post.return_value.json.return_value = {
        "access_token": "test_access_token",
        "refresh_token": "test_refresh_token",
        "expires_in": 3600
    }
    mock_httpx_post.return_value.raise_for_status.return_value = None

    # Set up the pending state
    monkeypatch.setitem(__import__("zotify_api.auth_state").auth_state.pending_states, "test_state", "test_code_verifier")

    response = client.get("/api/auth/spotify/callback?code=test_code&state=test_state")

    assert response.status_code == 200
    assert response.json()["status"] == "success"

    # Check that the token was saved to the DB
    mock_crud_call.assert_called_once()
