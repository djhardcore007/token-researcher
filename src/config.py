import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Twitter settings
    TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
    TWITTER_MAX_RESULTS = int(os.getenv('TWITTER_MAX_RESULTS', 5))
    TWITTER_LOG_LEVEL = os.getenv('TWITTER_LOG_LEVEL', 'INFO')

    # Telegram settings
    TELEGRAM_API_ID = os.getenv('TELEGRAM_API_ID')
    TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH')
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

    # Blockchain Explorer API Keys
    ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')
    BASESCAN_API_KEY = os.getenv('BASESCAN_API_KEY')
    SOLSCAN_API_KEY = os.getenv('SOLSCAN_API_KEY')

    @classmethod
    def validate(cls):
        """Validate required environment variables."""
        missing = []

        if not cls.TWITTER_BEARER_TOKEN:
            missing.append("TWITTER_BEARER_TOKEN")

        if not cls.TELEGRAM_API_ID:
            missing.append("TELEGRAM_API_ID")
        if not cls.TELEGRAM_API_HASH:
            missing.append("TELEGRAM_API_HASH")
        if not cls.TELEGRAM_BOT_TOKEN:
            missing.append("TELEGRAM_BOT_TOKEN")

        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")