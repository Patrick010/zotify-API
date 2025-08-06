import pytest
from pathlib import Path
from zotify_api.config import Settings

@pytest.fixture
def temp_config_dir(tmp_path: Path):
    return tmp_path

def test_key_generation_on_first_startup(temp_config_dir):
    settings = Settings(key_file_path=temp_config_dir / ".admin_api_key")
    key_file = temp_config_dir / ".admin_api_key"
    assert key_file.exists()
    assert settings.admin_api_key is not None

def test_key_read_from_file(temp_config_dir):
    key_file = temp_config_dir / ".admin_api_key"
    key_file.write_text("test_key_from_file")
    settings = Settings(key_file_path=key_file)
    assert settings.admin_api_key == "test_key_from_file"

def test_env_var_overrides_file(temp_config_dir, monkeypatch):
    key_file = temp_config_dir / ".admin_api_key"
    key_file.write_text("test_key_from_file")
    monkeypatch.setenv("ADMIN_API_KEY", "test_key_from_env")
    settings = Settings(key_file_path=key_file)
    assert settings.admin_api_key == "test_key_from_env"

def test_production_guard(temp_config_dir, monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("ADMIN_API_KEY", "")
    with pytest.raises(RuntimeError):
        Settings(key_file_path=temp_config_dir / ".admin_api_key", generate_key=False)
