from pydantic import BaseModel
from typing import Optional

class MetadataUpdate(BaseModel):
    mood: Optional[str] = None
    rating: Optional[int] = None
    source: Optional[str] = None
