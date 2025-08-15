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

@patch("zotify_api.routes.auth.handle_spotify_callback", new_callable=AsyncMock)
def test_spotify_callback_success(mock_handle_callback, client):
    """
    Tests the /auth/spotify/callback endpoint, mocking the service call.
    """
    payload = {"code": "test_code", "state": "test_state"}
    response = client.post("/api/auth/spotify/callback", json=payload)

    assert response.status_code == 200
    assert response.json() == {"status": "success"}
    mock_handle_callback.assert_called_once_with(code="test_code", state="test_state", db=ANY)
