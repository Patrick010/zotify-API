from fastapi import APIRouter, Depends, HTTPException
from zotify_api.schemas.logging import LogUpdate, LoggingConfigResponse
from zotify_api.services.logging_service import LoggingService, get_logging_service
from zotify_api.services.auth import require_admin_api_key

router = APIRouter(prefix="/logging")

@router.get("", response_model=LoggingConfigResponse)
def get_logging(logging_service: LoggingService = Depends(get_logging_service)):
    return logging_service.get_logging_config()

@router.patch("", response_model=LoggingConfigResponse, dependencies=[Depends(require_admin_api_key)])
def update_logging(
    update: LogUpdate,
    logging_service: LoggingService = Depends(get_logging_service)
):
    try:
        return logging_service.update_logging_config(update.model_dump(exclude_unset=True))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
