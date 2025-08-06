"""
Config service module.

This module contains the business logic for the config subsystem.
The functions in this module are designed to be called from the API layer.
The dependencies are injected into the functions, which makes them easy to test.
"""
import json
from pathlib import Path
from typing import Dict, Any

CONFIG_PATH = Path(__file__).parent.parent / "storage" / "config.json"

def get_default_config() -> Dict[str, Any]:
    """Returns the default configuration."""
    return {
        "library_path": "/music",
        "scan_on_startup": True,
        "cover_art_embed_enabled": True
    }

class ConfigService:
    def __init__(self, storage_path: Path = CONFIG_PATH):
        self._storage_path = storage_path
        self._config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        if self._storage_path.exists():
            content = self._storage_path.read_text()
            if content:
                return json.loads(content)
        return get_default_config()

    def _save_config(self):
        self._storage_path.write_text(json.dumps(self._config, indent=2))

    def get_config(self) -> Dict[str, Any]:
        return self._config

    def update_config(self, update_data: Dict[str, Any]) -> Dict[str, Any]:
        from zotify_api.models.config import ConfigUpdate
        validated_update = ConfigUpdate(**update_data)
        for k, v in validated_update.model_dump(exclude_unset=True).items():
            self._config[k] = v
        self._save_config()
        return self._config

    def reset_config(self) -> Dict[str, Any]:
        self._config = get_default_config()
        self._save_config()
        return self._config

def get_config_service():
    return ConfigService()
