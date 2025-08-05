from pydantic import BaseModel, Field, ConfigDict
from typing import List

class PlaylistBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)

class PlaylistCreate(PlaylistBase):
    pass

class Playlist(PlaylistBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tracks: List[str] = []

class TrackRequest(BaseModel):
    track_ids: List[str] = Field(..., min_length=1)

class PlaylistResponse(BaseModel):
    data: List[Playlist]
    meta: dict
