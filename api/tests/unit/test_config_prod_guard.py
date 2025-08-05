import os
import importlib
import pytest

def test_production_requires_database(monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")
    # Ensure DATABASE_URL is not set
    monkeypatch.delenv("DATABASE_URL", raising=False)
    # Reload config module to pick up env changes
    with pytest.raises(RuntimeError):
        import zotify_api.config as cfg
        importlib.reload(cfg)
