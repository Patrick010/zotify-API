from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from zotify_api.database import models, crud
from zotify_api.database.session import get_db
from zotify_api.schemas import notifications as notification_schemas
from zotify_api.services import notifications_service
from zotify_api.services.jwt_service import get_current_user


router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.post("", response_model=notification_schemas.Notification)
def create_notification(
    payload: notification_schemas.NotificationCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> Any:
    return notifications_service.create_notification(
        db, user=current_user, message=payload.message
    )


@router.get("", response_model=List[notification_schemas.Notification])
def get_notifications(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    return notifications_service.get_notifications(db, user=current_user)


@router.patch("/{notification_id}", status_code=204)
def mark_notification_as_read(
    notification_id: int,
    payload: notification_schemas.NotificationUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    # In a real app, we should check if the user is authorized to mark this notification as read.
    # For now, any authenticated user can mark any notification as read.
    notifications_service.mark_notification_as_read(
        db, notification_id=notification_id, read=payload.read
    )
    return
