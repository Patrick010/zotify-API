from pydantic import BaseModel
from typing import Optional

class CacheClearRequest(BaseModel):
    type: Optional[str] = None  # "search", "metadata", etc.
