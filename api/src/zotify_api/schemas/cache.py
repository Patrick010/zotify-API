# ID: API-073
from typing import Dict, Optional

from pydantic import BaseModel, Field


class CacheClearRequest(BaseModel):
    type: Optional[str] = Field(
        None,
        description=(
            "The type of cache to clear (e.g., 'search', 'metadata'). "
            "If omitted, the entire cache is cleared."
        ),
    )


class CacheStatusResponse(BaseModel):
    total_items: int = Field(..., description="The total number of items in the cache.")
    by_type: Dict[str, int] = Field(
        ..., description="A dictionary with the number of items for each cache type."
    )
