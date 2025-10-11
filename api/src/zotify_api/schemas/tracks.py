# ID: API-083
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class CreateTrackModel(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    artist: Optional[str] = Field(None, max_length=200)
    album: Optional[str] = Field(None, max_length=200)
    duration_seconds: Optional[int] = Field(None, gt=0)
    path: Optional[str] = None


class UpdateTrackModel(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    artist: Optional[str] = Field(None, max_length=200)
    album: Optional[str] = Field(None, max_length=200)
    duration_seconds: Optional[int] = Field(None, gt=0)
    path: Optional[str] = None


class TrackResponseModel(BaseModel):
    id: str
    name: str
    artist: Optional[str] = None
    album: Optional[str] = None
    duration_seconds: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    cover_url: Optional[str] = None


class TrackMetadataRequest(BaseModel):
    track_ids: List[str]


class TrackMetadataResponse(BaseModel):
    metadata: List[Dict[str, Any]]

    class Config:
        from_attributes = True
