from typing import Optional

from pydantic import BaseModel


class ProxyConfig(BaseModel):
    proxy_enabled: Optional[bool] = None
    http_proxy: Optional[str] = None
    https_proxy: Optional[str] = None

class NetworkConfigResponse(BaseModel):
    proxy_enabled: bool
    http_proxy: Optional[str] = None
    https_proxy: Optional[str] = None
