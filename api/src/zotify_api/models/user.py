from pydantic import BaseModel, ConfigDict, EmailStr
from typing import List, Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    liked_tracks: List[str] = []
    history: List[str] = []
    settings: Optional[dict] = {}
