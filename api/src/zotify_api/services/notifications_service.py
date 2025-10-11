# ID: API-097
import logging
import uuid
from typing import Any, Dict, List

from sqlalchemy.orm import Session

from zotify_api.database import crud, models

log = logging.getLogger(__name__)


def create_notification(db: Session, user: models.User, message: str) -> models.Notification:
    log.info(f"Creating notification for user {user.id}: {message}")
    notification = crud.create_notification(db, user=user, message=message)
    log.info(f"Notification {notification.id} created for user {user.id}")
    return notification


def get_notifications(db: Session, user: models.User) -> List[models.Notification]:
    return crud.get_notifications(db=db, user_id=user.id)


def mark_notification_as_read(db: Session, notification_id: int, read: bool = True) -> None:
    log.info(f"Setting notification {notification_id} read status to {read}")
    crud.mark_notification_as_read(
        db=db, notification_id=notification_id, read=read
    )
    log.info(f"Notification {notification_id} read status set to {read}")
