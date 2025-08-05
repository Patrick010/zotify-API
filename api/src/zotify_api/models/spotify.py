from pydantic import BaseModel, EmailStr
from typing import List, Literal
from datetime import datetime

class OAuthLoginResponse(BaseModel):
    auth_url: str

class TokenStatus(BaseModel):
    access_token_valid: bool
    expires_in_seconds: int

class SpotifyStatus(BaseModel):
    connected: bool
    account_name: EmailStr
    subscription_type: Literal["free", "premium"]
    last_synced: datetime

class SpotifySearchItem(BaseModel):
    id: str
    name: str
    type: Literal["track", "album", "artist", "playlist"]
    artist: str
    album: str

class SpotifySearchResponse(BaseModel):
    data: List[SpotifySearchItem]
    meta: dict
