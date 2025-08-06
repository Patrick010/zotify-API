from pydantic import BaseModel
from typing import Optional, Dict

class CacheClearRequest(BaseModel):
    type: Optional[str] = None  # "search", "metadata", etc.

class CacheStatusResponse(BaseModel):
    total_items: int
    by_type: Dict[str, int]
