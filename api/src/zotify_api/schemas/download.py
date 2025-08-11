from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from datetime import datetime
import uuid

class DownloadJobStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

# --- Base Schemas ---

class DownloadJobBase(BaseModel):
    track_id: str

# --- Schemas for Creating and Updating ---

class DownloadJobCreate(DownloadJobBase):
    pass

class DownloadJobUpdate(BaseModel):
    status: Optional[DownloadJobStatus] = None
    progress: Optional[float] = None
    error_message: Optional[str] = None

# --- Schema for Reading Data (includes all fields) ---

class DownloadJob(DownloadJobBase):
    job_id: str
    status: DownloadJobStatus
    progress: Optional[float]
    created_at: datetime
    error_message: Optional[str]

    class Config:
        orm_mode = True

# --- Schema for the Queue Status Endpoint ---

class DownloadQueueStatus(BaseModel):
    total_jobs: int
    pending: int
    completed: int
    failed: int
    jobs: List[DownloadJob]
