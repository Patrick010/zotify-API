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

def test_correct_key(monkeypatch):
    monkeypatch.setattr(settings, "admin_api_key", "test_key")
    assert require_admin_api_key(x_api_key="test_key", settings=settings) is True
