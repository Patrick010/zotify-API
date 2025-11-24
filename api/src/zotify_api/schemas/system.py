from pydantic import BaseModel


class SystemUptime(BaseModel):
    uptime_seconds: float
    uptime_human: str


class SystemEnv(BaseModel):
    version: str
    python_version: str
    platform: str
