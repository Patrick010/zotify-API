from pydantic import BaseModel, Field, ConfigDict
from typing import List

class PlaylistBase(BaseModel):
    name: str

class PlaylistCreate(PlaylistBase):
    pass

class Playlist(PlaylistBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tracks: List[str] = []

class TrackRequest(BaseModel):
    track_ids: List[str] = Field(..., min_length=1)
