import pytest
from src.telegram import TelegramResearcher


TEST_CHANNEL = "durov"
TEST_CHANNEL_INVALID = "thischannelshouldnotexist12345abc"


@pytest.mark.integration
def test_telegram_channel():
    """Test with a real Telegram channel."""
    telegram = TelegramResearcher()

    info = telegram.get_channel_info(TEST_CHANNEL)
    assert info is not None
    assert info.telegram_handle == TEST_CHANNEL
    assert info.member_count > 0


@pytest.mark.integration
def test_telegram_invalid_channel():
    """Test with an invalid channel."""
    telegram = TelegramResearcher()
    info = telegram.get_channel_info(TEST_CHANNEL_INVALID)
    assert info is None
