from unittest.mock import Mock, patch

from zotify_api.logging_config import setup_logging


@patch("zotify_api.logging_config.logging.basicConfig")
def test_setup_logging(mock_basic_config: Mock) -> None:
    """
    Tests that setup_logging calls logging.basicConfig.
    """
    setup_logging()
    mock_basic_config.assert_called_once()
