from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CacheClearRequest(BaseModel):
    type: Optional[str] = None  # "search", "metadata", etc.

class CacheResponse(BaseModel):
    total_items: int
    memory_usage_mb: float
    hit_rate: float = Field(..., ge=0.0, le=100.0)
    last_cleared: datetime
