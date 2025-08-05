from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List

class TrackBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    artist: str = Field(..., min_length=1, max_length=100)
    album: str = Field(..., min_length=1, max_length=100)

class TrackCreate(TrackBase):
    pass

class Track(TrackBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    genre: Optional[str] = None
    year: Optional[int] = Field(None, gt=1900, lt=2100)

class TrackMetadata(BaseModel):
    title: Optional[str] = None
    artist: Optional[str] = None
    album: Optional[str] = None
    genre: Optional[str] = None
    year: Optional[int] = None

class TrackResponse(BaseModel):
    data: List[Track]
    meta: dict
