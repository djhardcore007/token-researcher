import logging
import requests
from typing import Optional
from src.config import Config
from src.schema import TelegramChannel

class TelegramResearcher:
    def __init__(self, bot_token: str = None):
        self.bot_token = bot_token or Config.TELEGRAM_BOT_TOKEN
        if not self.bot_token:
            raise ValueError("Telegram bot token is required")

        self.logger = logging.getLogger(__name__)
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"

    def get_channel_info(self, telegram_handle: str) -> Optional[TelegramChannel]:
        """Get Telegram channel information."""
        if not telegram_handle:
            return None

        try:
            # Clean handle and prepare URL
            telegram_handle = telegram_handle.replace('@', '')
            url = f"{self.base_url}/getChatMemberCount"
            params = {"chat_id": f"@{telegram_handle}"}

            # Make API request
            response = requests.get(url, params=params)
            data = response.json()

            if not data.get('ok'):
                return None

            return TelegramChannel(
                telegram_handle=telegram_handle,
                member_count=data['result']
            )

        except Exception as e:
            self.logger.error(f"Error getting Telegram info: {str(e)}")
            return None