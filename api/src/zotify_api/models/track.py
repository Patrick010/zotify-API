from pydantic import BaseModel, ConfigDict
from typing import Optional

class TrackBase(BaseModel):
    title: str
    artist: str
    album: str

class TrackCreate(TrackBase):
    pass

class Track(TrackBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    genre: Optional[str] = None
    year: Optional[int] = None

class TrackMetadata(BaseModel):
    title: Optional[str] = None
    artist: Optional[str] = None
    album: Optional[str] = None
    genre: Optional[str] = None
    year: Optional[int] = None
