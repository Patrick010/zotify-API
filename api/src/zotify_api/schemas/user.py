import datetime
from typing import List, Optional

from pydantic import BaseModel, field_serializer


class UserProfileUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None


class UserPreferences(BaseModel):
    theme: str
    language: str
    notifications_enabled: bool

    class Config:
        from_attributes = True


class UserPreferencesUpdate(BaseModel):
    theme: Optional[str] = None
    language: Optional[str] = None
    notifications_enabled: Optional[bool] = None

    class Config:
        from_attributes = True


class UserProfileResponse(BaseModel):
    name: str
    email: Optional[str]
    preferences: UserPreferences

    class Config:
        from_attributes = True


class UserLikedResponse(BaseModel):
    items: List[str]


class UserHistoryResponse(BaseModel):
    items: List[str]


class UserCreate(BaseModel):
    username: str
    password: str


class User(BaseModel):
    id: str
    username: str
    role: str

    class Config:
        from_attributes = True


class LikedSong(BaseModel):
    id: int
    track_id: str

    class Config:
        from_attributes = True


class History(BaseModel):
    id: int
    track_id: str
    played_at: datetime.datetime

    @field_serializer("played_at")
    def serialize_dt(self, dt: datetime.datetime, _info):
        return dt.isoformat()

    class Config:
        from_attributes = True


class SyncLikedResponse(BaseModel):
    status: str
    synced: int
