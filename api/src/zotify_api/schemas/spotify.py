from pydantic import BaseModel
from typing import List

class SpotifyDevices(BaseModel):
    devices: List[dict]

class OAuthLoginResponse(BaseModel):
    auth_url: str

class TokenStatus(BaseModel):
    access_token_valid: bool
    expires_in_seconds: int

class Playlist(BaseModel):
    id: str
    name: str
    public: bool
    collaborative: bool
    description: str | None = None
    tracks: dict

class PlaylistTracks(BaseModel):
    items: List[dict]
    total: int

class CreatePlaylistRequest(BaseModel):
    name: str
    public: bool = True
    collaborative: bool = False
    description: str = ""

class AddTracksRequest(BaseModel):
    uris: List[str]

class RemoveTracksRequest(BaseModel):
    uris: List[str]
