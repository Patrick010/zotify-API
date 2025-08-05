from fastapi import APIRouter
from zotify_api.models.config import ConfigUpdate
import json
from pathlib import Path

router = APIRouter()

CONFIG_PATH = Path(__file__).parent.parent / "storage" / "config.json"

def load_config():
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text())
    else:
        return {
            "library_path": "/music",
            "scan_on_startup": True,
            "cover_art_embed_enabled": True
        }

def save_config(config_data):
    CONFIG_PATH.write_text(json.dumps(config_data, indent=2))

config = load_config()
default_config = config.copy()

@router.get("/config")
def get_config():
    return config

@router.patch("/config")
def update_config(update: ConfigUpdate):
    for k, v in update.model_dump(exclude_unset=True).items():
        config[k] = v
    save_config(config)
    return config

@router.post("/config/reset")
def reset_config():
    global config
    config = default_config.copy()
    save_config(config)
    return config
