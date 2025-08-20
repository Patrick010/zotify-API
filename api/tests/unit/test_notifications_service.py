from unittest.mock import MagicMock

import pytest

from zotify_api.services.notifications_service import NotificationsService


@pytest.fixture
def mock_user_service():
    return MagicMock()

def test_create_notification(mock_user_service):
    service = NotificationsService(user_service=mock_user_service)
    notification = service.create_notification("user1", "Test message")
    assert notification["user_id"] == "user1"
    assert notification["message"] == "Test message"
    mock_user_service.add_notification.assert_called_once()

def test_get_notifications(mock_user_service):
    service = NotificationsService(user_service=mock_user_service)
    service.get_notifications("user1")
    mock_user_service.get_notifications.assert_called_once_with("user1")

def test_mark_notification_as_read(mock_user_service):
    service = NotificationsService(user_service=mock_user_service)
    service.mark_notification_as_read("notif1", True)
    mock_user_service.mark_notification_as_read.assert_called_once_with("notif1", True)
