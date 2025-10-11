# ID: API-080
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class PlaylistIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)


class PlaylistOut(BaseModel):
    id: Optional[str] = None
    name: str
    description: Optional[str] = None


class PlaylistsResponse(BaseModel):
    data: List[PlaylistOut]
    meta: Dict[str, Any]
