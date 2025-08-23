from typing import Any, Dict

from fastapi import APIRouter, Depends

from zotify_api.models.config_models import ConfigModel, ConfigUpdate
from zotify_api.schemas.generic import StandardResponse
from zotify_api.services.auth import require_admin_api_key
from zotify_api.services.config_service import ConfigService, get_config_service

router = APIRouter(prefix="/config", tags=["config"])


@router.get("", response_model=StandardResponse[ConfigModel])
def get_config(
    config_service: ConfigService = Depends(get_config_service),
) -> Dict[str, Any]:
    config = config_service.get_config()
    return {"data": config}


@router.patch(
    "",
    dependencies=[Depends(require_admin_api_key)],
    response_model=StandardResponse[ConfigModel],
)
def update_config(
    update: ConfigUpdate, config_service: ConfigService = Depends(get_config_service)
) -> Dict[str, Any]:
    config = config_service.update_config(update.model_dump(exclude_unset=True))
    return {"data": config}


@router.post(
    "/reset",
    dependencies=[Depends(require_admin_api_key)],
    response_model=StandardResponse[ConfigModel],
)
def reset_config(
    config_service: ConfigService = Depends(get_config_service),
) -> Dict[str, Any]:
    config = config_service.reset_config()
    return {"data": config}
