import pytest
from unittest.mock import patch
from src.telegram import TelegramResearcher

def test_get_channel_info():
    """Test getting Telegram channel info."""
    telegram = TelegramResearcher("test_token")

    mock_response = {
        'ok': True,
        'result': 1000
    }

    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        info = telegram.get_channel_info("test_channel")
        assert info.telegram_handle == "test_channel"
        assert info.member_count == 1000