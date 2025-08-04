from pydantic import BaseModel, Field
from typing import List

class PlaylistBase(BaseModel):
    name: str

class PlaylistCreate(PlaylistBase):
    pass

class Playlist(PlaylistBase):
    id: str
    tracks: List[str] = []

    class Config:
        orm_mode = True

class TrackRequest(BaseModel):
    track_ids: List[str] = Field(..., min_items=1)
