import pytest
from unittest.mock import patch, AsyncMock
from sqlalchemy.orm import Session
from zotify_api.providers.spotify_connector import SpotifyConnector

@pytest.mark.asyncio
@patch("zotify_api.providers.spotify_connector.crud.create_or_update_spotify_token")
@patch("httpx.AsyncClient")
async def test_handle_oauth_callback_success(mock_AsyncClient, mock_crud_call, monkeypatch):
    """ Tests the happy path for the OAuth callback handler """
    mock_db = Session()
    connector = SpotifyConnector(db=mock_db)

    # Configure the mock for the async context manager
    mock_client_instance = AsyncMock()

    # Configure the response from the 'post' call
    mock_post_response = AsyncMock()
    mock_post_response.json.return_value = {
        "access_token": "test_access_token",
        "refresh_token": "test_refresh_token",
        "expires_in": 3600
    }
    mock_post_response.raise_for_status.return_value = None
    mock_client_instance.post.return_value = mock_post_response

    # Make the AsyncClient return our configured instance when used as a context manager
    mock_AsyncClient.return_value.__aenter__.return_value = mock_client_instance

    monkeypatch.setitem(__import__("zotify_api.auth_state").auth_state.pending_states, "test_state", "test_code_verifier")

    html_response = await connector.handle_oauth_callback(code="test_code", error=None, state="test_state")

    mock_crud_call.assert_called_once()
    assert "Successfully authenticated" in html_response

@pytest.mark.asyncio
async def test_handle_oauth_callback_error():
    """ Tests the failure path for the OAuth callback handler """
    mock_db = Session()
    connector = SpotifyConnector(db=mock_db)

    html_response = await connector.handle_oauth_callback(code=None, error="access_denied", state="test_state")

    assert "Authentication Failed" in html_response
    assert "access_denied" in html_response
