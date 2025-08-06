from fastapi import APIRouter, Depends
from zotify_api.models.config import ConfigUpdate
from zotify_api.services.config_service import ConfigService, get_config_service

router = APIRouter(prefix="/config")

@router.get("")
def get_config(config_service: ConfigService = Depends(get_config_service)):
    return config_service.get_config()

@router.patch("")
def update_config(
    update: ConfigUpdate,
    config_service: ConfigService = Depends(get_config_service)
):
    return config_service.update_config(update.model_dump(exclude_unset=True))

@router.post("/reset")
def reset_config(config_service: ConfigService = Depends(get_config_service)):
    return config_service.reset_config()
