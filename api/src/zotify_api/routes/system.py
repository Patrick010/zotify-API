import yaml
from pydantic import ValidationError
from fastapi import APIRouter, HTTPException, Depends, status

from zotify_api.services.auth import require_admin_api_key
from zotify_api.core.logging_framework.schemas import LoggingFrameworkConfig
from zotify_api.core.logging_framework.service import get_logging_service

router = APIRouter(prefix="/system", tags=["system"], dependencies=[Depends(require_admin_api_key)])

@router.post("/logging/reload", status_code=status.HTTP_202_ACCEPTED)
def reload_logging_config():
    """
    Reloads the logging framework's configuration from the
    `logging_framework.yml` file at runtime.
    """
    try:
        with open("logging_framework.yml", "r") as f:
            config_data = yaml.safe_load(f)
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="logging_framework.yml not found.",
        )
    except yaml.YAMLError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error parsing logging_framework.yml.",
        )

    try:
        validated_config = LoggingFrameworkConfig(**config_data)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid configuration schema: {e}",
        )

    # Get the service and load the new config
    logging_service = get_logging_service()
    logging_service.load_config(validated_config)

    return {"status": "success", "message": "Logging framework configuration reloaded."}


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
from zotify_api.schemas.generic import StandardResponse
from zotify_api.config import settings


@router.post("/reset")
def reset_system_state():
    raise HTTPException(status_code=501, detail="Not Implemented")

def get_human_readable_uptime(seconds):
    days, rem = divmod(seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, seconds = divmod(rem, 60)
    return f"{int(days)}d {int(hours)}h {int(minutes)}m {int(seconds)}s"

@router.get("/uptime", response_model=StandardResponse[SystemUptime])
def get_uptime():
    """ Returns uptime in seconds and human-readable format. """
    uptime_seconds = time.time() - app_start_time.timestamp()
    uptime_data = SystemUptime(
        uptime_seconds=uptime_seconds,
        uptime_human=get_human_readable_uptime(uptime_seconds)
    )
    return {"data": uptime_data}

@router.get("/env", response_model=StandardResponse[SystemEnv])
def get_env():
    """ Returns a safe subset of environment info """
    env_data = SystemEnv(
        version=settings.version,
        python_version=sys.version,
        platform=platform.system(),
    )
    return {"data": env_data}
