from pydantic import BaseModel

class OAuthLoginResponse(BaseModel):
    auth_url: str

class TokenStatus(BaseModel):
    access_token_valid: bool
    expires_in_seconds: int
