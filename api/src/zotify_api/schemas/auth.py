from pydantic import BaseModel, Field
from typing import Optional

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
