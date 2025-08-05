from pydantic import BaseModel
from typing import Literal
import socket
import sys

class SystemInfo(BaseModel):
    uptime_seconds: float
    version: str
    env: str
    hostname: str
    python_version: str
