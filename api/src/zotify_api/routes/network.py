from fastapi import APIRouter
from zotify_api.models.network import ProxyConfig

router = APIRouter()

# In-memory state
network_config = {
    "proxy_enabled": False,
    "http_proxy": None,
    "https_proxy": None
}

@router.get("/network", summary="Get network proxy configuration")
def get_network():
    return network_config

@router.patch("/network", summary="Update network proxy settings")
def update_network(cfg: ProxyConfig):
    for k, v in cfg.model_dump(exclude_unset=True).items():
        network_config[k] = v
    return network_config
