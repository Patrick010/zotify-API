from unittest.mock import MagicMock

import pytest

from zotify_api.services.notifications_service import NotificationsService
from zotify_api.services import user_service


@pytest.fixture
def mock_user_service(monkeypatch):
    mock_get_user = MagicMock()
    mock_update_user = MagicMock()
    mock_read_data = MagicMock()
    monkeypatch.setattr(user_service, "get_user", mock_get_user)
    monkeypatch.setattr(user_service, "update_user", mock_update_user)
    monkeypatch.setattr(user_service, "_read_data", mock_read_data)
    return mock_get_user, mock_update_user, mock_read_data


def test_create_notification(mock_user_service) -> None:
    mock_get_user, mock_update_user, _ = mock_user_service
    mock_get_user.return_value = {"notifications": []}
    service = NotificationsService()
    notification = service.create_notification("user1", "Test message")
    assert notification["user_id"] == "user1"
    assert notification["message"] == "Test message"
    mock_get_user.assert_called_once_with("user1")
    mock_update_user.assert_called_once()


def test_get_notifications(mock_user_service) -> None:
    mock_get_user, _, _ = mock_user_service
    mock_get_user.return_value = {"notifications": ["notification1"]}
    service = NotificationsService()
    notifications = service.get_notifications("user1")
    assert notifications == ["notification1"]
    mock_get_user.assert_called_once_with("user1")


def test_mark_notification_as_read(mock_user_service) -> None:
    mock_get_user, mock_update_user, mock_read_data = mock_user_service
    mock_read_data.return_value = {
        "users": {
            "user1": {
                "notifications": [
                    {"id": "notif1", "read": False},
                    {"id": "notif2", "read": False},
                ]
            }
        }
    }
    service = NotificationsService()
    service.mark_notification_as_read("notif1", True)
    mock_read_data.assert_called_once()
    mock_update_user.assert_called_once()
    args, _ = mock_update_user.call_args
    assert args[0] == "user1"
    assert args[1]["notifications"][0]["read"] is True
