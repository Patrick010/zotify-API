from typing import Optional

from pydantic import BaseModel


class MetadataUpdate(BaseModel):
    mood: Optional[str] = None
    rating: Optional[int] = None
    source: Optional[str] = None


class MetadataResponse(BaseModel):
    title: str
    mood: Optional[str] = None
    rating: Optional[int] = None
    source: Optional[str] = None


class MetadataPatchResponse(BaseModel):
    status: str
    track_id: str
