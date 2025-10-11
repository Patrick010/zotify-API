# ID: API-217
from unittest.mock import MagicMock, patch

from zotify_api.core.error_handler.actions import log_critical, webhook


def test_log_critical_action() -> None:
    """
    Tests that the log_critical action logs a critical error.
    """
    with patch(
        "zotify_api.core.error_handler.actions.log_critical.log_event"
    ) as mock_log_event:
        log_critical.run(Exception("Test"), {"message": "Test message"})
        mock_log_event.assert_called_once()


def test_webhook_action_success() -> None:
    """
    Tests that the webhook action logs the intent to send a webhook.
    """
    mock_logger = MagicMock()
    with patch("zotify_api.core.error_handler.actions.webhook.log", mock_logger):
        webhook.run(
            Exception("Test"), {"url": "http://test.com", "payload": {"key": "value"}}
        )
        mock_logger.info.assert_called_once_with(
            "Sending webhook to http://test.com..."
        )


def test_webhook_action_missing_details() -> None:
    """
    Tests that the webhook action logs an error if details are missing.
    """
    mock_logger = MagicMock()
    with patch("zotify_api.core.error_handler.actions.webhook.log", mock_logger):
        webhook.run(Exception("Test"), {})
        mock_logger.error.assert_called_once_with(
            "Webhook action is missing 'url' or 'payload' in details."
        )
