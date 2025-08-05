from pydantic import BaseModel
from datetime import datetime

class CacheStats(BaseModel):
    total_items: int
    memory_usage_mb: float
    hit_rate: float  # 0.0 - 100.0
    last_cleared: datetime
