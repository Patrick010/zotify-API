from fastapi import APIRouter, HTTPException, Depends
from zotify_api.services.auth import require_admin_api_key

router = APIRouter(prefix="/system", tags=["system"], dependencies=[Depends(require_admin_api_key)])

@router.get("/status")
def get_system_status():
    raise HTTPException(status_code=501, detail="Not Implemented")

@router.get("/storage")
def get_system_storage():
    raise HTTPException(status_code=501, detail="Not Implemented")

@router.get("/logs")
def get_system_logs():
    raise HTTPException(status_code=501, detail="Not Implemented")

@router.post("/reload")
def reload_system_config():
    raise HTTPException(status_code=501, detail="Not Implemented")

import time
import platform
import sys
from fastapi import Request
from typing import Optional
from zotify_api.globals import app_start_time
from zotify_api.schemas.system import SystemUptime, SystemEnv
from zotify_api.config import settings


@router.post("/reset")
def reset_system_state():
    raise HTTPException(status_code=501, detail="Not Implemented")

def get_human_readable_uptime(seconds):
    days, rem = divmod(seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, seconds = divmod(rem, 60)
    return f"{int(days)}d {int(hours)}h {int(minutes)}m {int(seconds)}s"

@router.get("/uptime", response_model=SystemUptime)
def get_uptime():
    """ Returns uptime in seconds and human-readable format. """
    uptime_seconds = time.time() - app_start_time.timestamp()
    return SystemUptime(
        uptime_seconds=uptime_seconds,
        uptime_human=get_human_readable_uptime(uptime_seconds)
    )

@router.get("/env", response_model=SystemEnv)
def get_env():
    """ Returns a safe subset of environment info """
    return SystemEnv(
        version=settings.version,
        python_version=sys.version,
        platform=platform.system(),
    )
