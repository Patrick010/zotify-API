from pydantic import BaseModel
from typing import List, Dict, Any

class UserProfileResponse(BaseModel):
    name: str
    email: str

class UserLikedResponse(BaseModel):
    items: List[str]

class UserHistoryResponse(BaseModel):
    items: List[str]

class SyncLikedResponse(BaseModel):
    status: str
    synced: int
