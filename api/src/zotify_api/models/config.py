from pydantic import BaseModel
from typing import Optional

class ConfigModel(BaseModel):
    library_path: str
    scan_on_startup: bool
    cover_art_embed_enabled: bool

class ConfigUpdate(BaseModel):
    library_path: Optional[str] = None
    scan_on_startup: Optional[bool] = None
    cover_art_embed_enabled: Optional[bool] = None

    class Config:
        extra = "forbid"
