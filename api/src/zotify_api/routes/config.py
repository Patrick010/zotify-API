from fastapi import APIRouter
from zotify_api.models.config import ConfigUpdate

router = APIRouter()

# In-memory dummy config
config = {
    "library_path": "/music",
    "scan_on_startup": True,
    "cover_art_embed_enabled": True
}
default_config = config.copy()

@router.get("/config", summary="Get current application configuration")
def get_config():
    return config

@router.patch("/config", summary="Update specific configuration fields")
def update_config(update: ConfigUpdate):
    for key, value in update.model_dump(exclude_unset=True).items():
        config[key] = value
    return config

@router.post("/config/reset", summary="Reset configuration to default values")
def reset_config():
    global config
    config = default_config.copy()
    return config
