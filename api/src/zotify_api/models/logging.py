from pydantic import BaseModel
from typing import Literal, List
from datetime import datetime

class LogLevel(str):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

class LogEntry(BaseModel):
    timestamp: datetime
    level: str
    message: str

class LoggingResponse(BaseModel):
    data: list[LogEntry]
    meta: dict
