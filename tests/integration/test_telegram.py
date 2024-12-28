import pytest
from src.telegram import TelegramResearcher

@pytest.mark.integration
def test_telegram_channel():
    """Test with a real Telegram channel."""
    telegram = TelegramResearcher()

    info = telegram.get_channel_info("durov")
    assert info is not None
    assert info.telegram_handle == "durov"
    assert info.member_count > 0

@pytest.mark.integration
def test_telegram_invalid_channel():
    """Test with an invalid channel."""
    telegram = TelegramResearcher()
    info = telegram.get_channel_info("thischannelshouldnotexist12345abc")
    assert info is None