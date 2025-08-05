from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from enum import Enum

class SyncStatus(str, Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"

class SyncJob(BaseModel):
    id: UUID
    status: SyncStatus
    progress: float = Field(..., ge=0.0, le=100.0)
    started_at: datetime
    finished_at: Optional[datetime] = None

class SyncResponse(BaseModel):
    data: List[SyncJob]
    meta: dict

class SyncRequest(BaseModel):
    playlist_id: str
