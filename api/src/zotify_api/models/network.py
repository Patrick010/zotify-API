from pydantic import BaseModel
from typing import Optional

class ProxyConfig(BaseModel):
    proxy_enabled: Optional[bool] = None
    http_proxy: Optional[str] = None
    https_proxy: Optional[str] = None
