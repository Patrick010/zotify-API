# ID: API-063
from typing import Any, Dict

from fastapi import APIRouter, Depends

from zotify_api.schemas.generic import StandardResponse
from zotify_api.schemas.network import NetworkConfigResponse, ProxyConfig
from zotify_api.services.auth import require_admin_api_key
from zotify_api.services.network_service import NetworkService, get_network_service

router = APIRouter(prefix="/network", tags=["network"])


@router.get("", response_model=StandardResponse[NetworkConfigResponse])
def get_network(
    network_service: NetworkService = Depends(get_network_service),
) -> Dict[str, Any]:
    config = network_service.get_network_config()
    return {"data": config}


@router.patch(
    "",
    response_model=StandardResponse[NetworkConfigResponse],
    dependencies=[Depends(require_admin_api_key)],
)
def update_network(
    cfg: ProxyConfig, network_service: NetworkService = Depends(get_network_service)
) -> Dict[str, Any]:
    config = network_service.update_network_config(cfg.model_dump(exclude_unset=True))
    return {"data": config}
