import logging
import uuid
from typing import Any, Dict, List

from zotify_api.services import user_service

log = logging.getLogger(__name__)


class NotificationsService:
    def create_notification(self, user_id: str, message: str) -> Dict[str, Any]:
        log.info(f"Creating notification for user {user_id}: {message}")
        notification = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "message": message,
            "read": False,
        }
        user_data = user_service.get_user(user_id)
        if user_data:
            user_data["notifications"].append(notification)
            user_service.update_user(user_id, user_data)
        log.info(f"Notification {notification['id']} created for user {user_id}")
        return notification

    def get_notifications(self, user_id: str) -> List[Dict[str, Any]]:
        user_data = user_service.get_user(user_id)
        if not user_data:
            return []
        return user_data["notifications"]

    def mark_notification_as_read(
        self, notification_id: str, read: bool = True
    ) -> None:
        log.info(f"Setting notification {notification_id} read status to {read}")
        # This is inefficient, but we have to work with the current data structure.
        # To fix this properly, we would need to store notifications in their own table.
        data = user_service._read_data()
        for user_id, user_data in data["users"].items():
            for n in user_data["notifications"]:
                if n["id"] == notification_id:
                    n["read"] = read
                    user_service.update_user(user_id, user_data)
                    log.info(f"Notification {notification_id} read status set to {read}")
                    return


def get_notifications_service() -> NotificationsService:
    return NotificationsService()
