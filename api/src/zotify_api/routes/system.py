# ID: API-068
import os
import platform
import sys
import time
from typing import Any, Dict

import yaml
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError

from zotify_api.config import settings
from zotify_api.core.logging_framework.schemas import LoggingFrameworkConfig
from zotify_api.core.logging_framework.service import get_logging_service
from zotify_api.globals import app_start_time
from zotify_api.schemas.generic import StandardResponse
from zotify_api.schemas.system import SystemEnv, SystemUptime
from zotify_api.services.auth import require_admin_api_key

router = APIRouter(
    prefix="/system",
    tags=["system"],
    dependencies=[Depends(require_admin_api_key)],
)


@router.post("/logging/reload", status_code=status.HTTP_202_ACCEPTED)
def reload_logging_config() -> Dict[str, str]:
    """
    Reloads the logging framework's configuration from the
    `logging_framework.yml` file at runtime.
    """
    try:
        # Construct path to 'api/logging_framework.yml' relative to this file's location
        current_dir = os.path.dirname(__file__)
        config_path = os.path.abspath(
            os.path.join(current_dir, "..", "..", "..", "logging_framework.yml")
        )
        with open(config_path, "r") as f:
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
def get_system_status() -> None:
    raise HTTPException(status_code=501, detail="Not Implemented")


@router.get("/storage")
def get_system_storage() -> None:
    raise HTTPException(status_code=501, detail="Not Implemented")


@router.get("/logs")
def get_system_logs() -> None:
    raise HTTPException(status_code=501, detail="Not Implemented")


@router.post("/reload")
def reload_system_config() -> None:
    raise HTTPException(status_code=501, detail="Not Implemented")


@router.post("/reset")
def reset_system_state() -> None:
    raise HTTPException(status_code=501, detail="Not Implemented")


def get_human_readable_uptime(seconds: float) -> str:
    days, rem = divmod(seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, seconds = divmod(rem, 60)
    return f"{int(days)}d {int(hours)}h {int(minutes)}m {int(seconds)}s"


@router.get("/uptime", response_model=StandardResponse[SystemUptime])
def get_uptime() -> Dict[str, Any]:
    """Returns uptime in seconds and human-readable format."""
    uptime_seconds = time.time() - app_start_time.timestamp()
    uptime_data = SystemUptime(
        uptime_seconds=uptime_seconds,
        uptime_human=get_human_readable_uptime(uptime_seconds),
    )
    return {"data": uptime_data}


@router.get("/env", response_model=StandardResponse[SystemEnv])
def get_env() -> Dict[str, Any]:
    """Returns a safe subset of environment info"""
    env_data = SystemEnv(
        version=settings.version,
        python_version=sys.version,
        platform=platform.system(),
    )
    return {"data": env_data}
