from typing import Any, Dict

from fastapi import APIRouter, Depends

from zotify_api.schemas.generic import StandardResponse
from zotify_api.schemas.notifications import Notification, NotificationCreate, NotificationUpdate
from zotify_api.services.auth import require_admin_api_key
from zotify_api.services.notifications_service import NotificationsService, get_notifications_service

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.post(
    "",
    response_model=StandardResponse[Notification],
    dependencies=[Depends(require_admin_api_key)],
)
def create_notification(
    payload: NotificationCreate,
    notifications_service: NotificationsService = Depends(get_notifications_service),
):
    notification = notifications_service.create_notification(
        payload.user_id, payload.message
    )
    return {"data": notification}


@router.get("/{user_id}", response_model=Dict[str, Any])
def get_notifications(
    user_id: str,
    notifications_service: NotificationsService = Depends(get_notifications_service),
):
    items = notifications_service.get_notifications(user_id)
    return {"data": items, "meta": {"total": len(items)}}


@router.patch(
    "/{notification_id}",
    status_code=204,
    dependencies=[Depends(require_admin_api_key)],
)
def mark_notification_as_read(
    notification_id: str,
    payload: NotificationUpdate,
    notifications_service: NotificationsService = Depends(get_notifications_service),
):
    notifications_service.mark_notification_as_read(notification_id, payload.read)
    return {}
