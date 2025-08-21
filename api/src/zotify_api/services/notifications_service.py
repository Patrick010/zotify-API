import logging
import uuid
from typing import Any, Dict, List

from fastapi import Depends

from zotify_api.services.user_service import UserService, get_user_service

log = logging.getLogger(__name__)

class NotificationsService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def create_notification(self, user_id: str, message: str) -> Dict[str, Any]:
        log.info(f"Creating notification for user {user_id}: {message}")
        notification = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "message": message,
            "read": False,
        }
        self.user_service.add_notification(notification)
        log.info(f"Notification {notification['id']} created for user {user_id}")
        return notification

    def get_notifications(self, user_id: str) -> List[Dict[str, Any]]:
        return self.user_service.get_notifications(user_id)

    def mark_notification_as_read(self, notification_id: str, read: bool = True) -> None:
        log.info(f"Setting notification {notification_id} read status to {read}")
        self.user_service.mark_notification_as_read(notification_id, read)
        log.info(f"Notification {notification_id} read status set to {read}")

def get_notifications_service(
    user_service: UserService = Depends(get_user_service),
) -> NotificationsService:
    return NotificationsService(user_service)
