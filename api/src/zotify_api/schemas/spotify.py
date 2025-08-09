from pydantic import BaseModel
from typing import List

class SpotifyDevices(BaseModel):
    devices: List[dict]

class OAuthLoginResponse(BaseModel):
    auth_url: str

class TokenStatus(BaseModel):
    access_token_valid: bool
    expires_in_seconds: int
