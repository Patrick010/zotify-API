from fastapi import APIRouter, Depends
from zotify_api.schemas.network import ProxyConfig, NetworkConfigResponse
from zotify_api.services.network_service import NetworkService, get_network_service

router = APIRouter(prefix="/network")

@router.get("", response_model=NetworkConfigResponse)
def get_network(network_service: NetworkService = Depends(get_network_service)):
    return network_service.get_network_config()

@router.patch("", response_model=NetworkConfigResponse)
def update_network(
    cfg: ProxyConfig,
    network_service: NetworkService = Depends(get_network_service)
):
    return network_service.update_network_config(cfg.model_dump(exclude_unset=True))
