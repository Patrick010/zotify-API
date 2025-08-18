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
