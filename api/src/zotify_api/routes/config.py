from fastapi import APIRouter, Depends
from zotify_api.models.config import ConfigUpdate
from zotify_api.services.config_service import ConfigService, get_config_service
from zotify_api.services.auth import require_admin_api_key

router = APIRouter(prefix="/config")

@router.get("")
def get_config(config_service: ConfigService = Depends(get_config_service)):
    return config_service.get_config()

@router.patch("", dependencies=[Depends(require_admin_api_key)])
def update_config(
    update: ConfigUpdate,
    config_service: ConfigService = Depends(get_config_service)
):
    return config_service.update_config(update.model_dump(exclude_unset=True))

@router.post("/reset", dependencies=[Depends(require_admin_api_key)])
def reset_config(config_service: ConfigService = Depends(get_config_service)):
    return config_service.reset_config()
