from fastapi import APIRouter, Depends
from typing import List
from zotify_api.schemas.notifications import Notification, NotificationCreate, NotificationUpdate
from zotify_api.services.notifications_service import NotificationsService, get_notifications_service

router = APIRouter(prefix="/notifications")

@router.post("", response_model=Notification)
def create_notification(
    payload: NotificationCreate,
    notifications_service: NotificationsService = Depends(get_notifications_service),
):
    return notifications_service.create_notification(payload.user_id, payload.message)

@router.get("/{user_id}", response_model=List[Notification])
def get_notifications(
    user_id: str,
    notifications_service: NotificationsService = Depends(get_notifications_service),
):
    return notifications_service.get_notifications(user_id)

@router.patch("/{notification_id}", status_code=204)
def mark_notification_as_read(
    notification_id: str,
    payload: NotificationUpdate,
    notifications_service: NotificationsService = Depends(get_notifications_service),
):
    notifications_service.mark_notification_as_read(notification_id)
    return {}
