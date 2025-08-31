from typing import List, Optional

from pydantic import BaseModel


class UserProfileUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None


class UserPreferences(BaseModel):
    theme: str
    language: str


class UserPreferencesUpdate(BaseModel):
    theme: Optional[str] = None
    language: Optional[str] = None


class UserProfileResponse(BaseModel):
    name: str
    email: str
    preferences: UserPreferences


class UserLikedResponse(BaseModel):
    items: List[str]


class UserHistoryResponse(BaseModel):
    items: List[str]


class SyncLikedResponse(BaseModel):
    status: str
    synced: int
