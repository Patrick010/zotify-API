from typing import Optional

from pydantic import BaseModel, Field


class AuthStatus(BaseModel):
    authenticated: bool
    user_id: Optional[str] = None
    token_valid: bool
    expires_in: int


class RefreshResponse(BaseModel):
    expires_at: int


class SpotifyCallbackPayload(BaseModel):
    code: str = Field(..., min_length=1)
    state: str = Field(..., min_length=1)


class CallbackResponse(BaseModel):
    status: str


class Token(BaseModel):
    access_token: str
    token_type: str


class OAuthLoginResponse(BaseModel):
    auth_url: str
