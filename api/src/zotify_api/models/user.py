from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import List, Optional

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    pass

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    liked_tracks: List[str] = []
    history: List[str] = []
    settings: Optional[dict] = Field(default_factory=dict)
