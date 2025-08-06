from fastapi import APIRouter, HTTPException
from zotify_api.models.logging import LogUpdate

router = APIRouter()

# In-memory state
log_config = {
    "level": "INFO",
    "log_to_file": False,
    "log_file": None
}

@router.get("/logging", summary="Get current logging settings")
def get_logging():
    return log_config

@router.patch("/logging", summary="Update logging level or target")
def update_logging(update: LogUpdate):
    if update.level and update.level not in ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]:
        raise HTTPException(status_code=400, detail="Invalid log level")
    for k, v in update.model_dump(exclude_unset=True).items():
        log_config[k] = v
    return log_config
