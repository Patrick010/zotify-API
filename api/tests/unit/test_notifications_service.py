from unittest.mock import MagicMock

import pytest
from sqlalchemy.orm import Session

from zotify_api.database import crud, models
from zotify_api.services import notifications_service


@pytest.fixture
def mock_crud(monkeypatch):
    mock_create = MagicMock()
    mock_get = MagicMock()
    mock_mark_as_read = MagicMock()
    monkeypatch.setattr(crud, "create_notification", mock_create)
    monkeypatch.setattr(crud, "get_notifications", mock_get)
    monkeypatch.setattr(crud, "mark_notification_as_read", mock_mark_as_read)
    return mock_create, mock_get, mock_mark_as_read


def test_create_notification(mock_crud, test_db_session: Session):
    mock_create, _, _ = mock_crud
    user = models.User(id="user1", username="test", hashed_password="pw")
    notifications_service.create_notification(db=test_db_session, user=user, message="Test message")
    mock_create.assert_called_once()
    call_args, call_kwargs = mock_create.call_args
    assert call_kwargs['user'] == user
    assert call_kwargs['message'] == "Test message"


def test_get_notifications(mock_crud, test_db_session: Session):
    _, mock_get, _ = mock_crud
    user = models.User(id="user1", username="test", hashed_password="pw")
    notifications_service.get_notifications(db=test_db_session, user=user)
    mock_get.assert_called_once_with(db=test_db_session, user_id="user1")


def test_mark_notification_as_read(mock_crud, test_db_session: Session):
    _, _, mock_mark_as_read = mock_crud
    notifications_service.mark_notification_as_read(
        db=test_db_session, notification_id=1, read=True
    )
    mock_mark_as_read.assert_called_once_with(
        db=test_db_session, notification_id=1, read=True
    )
