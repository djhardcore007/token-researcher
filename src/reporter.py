import logging
from datetime import datetime
from typing import Optional
from src.schema import Report
from src.dexscreener import DexScreener
from src.coingecko import CoinGecko
from src.twitter import TwitterResearcher
from src.telegram import TelegramResearcher

class Reporter:
    def __init__(self):
        self.dex = DexScreener()
        self.coingecko = CoinGecko()
        self.twitter = TwitterResearcher()
        self.telegram = TelegramResearcher()
        self.logger = logging.getLogger(__name__)

    def generate_report(self, token_address: str, chain: str) -> Optional[Report]:
        """Generate a complete report for a token."""
        try:
            # Get DexScreener data
            token_info = self.dex.research_tokens(token_address)
            if not token_info:
                return None

            # Get CoinGecko data
            assert token_info.chain == chain
            coingecko_data = self.coingecko.get_coin_info(token_address, chain)

            # Get Twitter data if handle exists
            twitter_data = None
            if coingecko_data.social_info.twitter_handle:
                twitter_data = self.twitter.get_twitter_info(
                    coingecko_data.social_info.twitter_handle
                )

            # Get Telegram data if handle exists
            telegram_data = None
            if coingecko_data.social_info.telegram_handle:
                telegram_data = self.telegram.get_channel_info(
                    coingecko_data.social_info.telegram_handle
                )

            # Combine all data
            return Report(
                token_address=token_address,
                chain=chain,
                timestamp=datetime.now(),
                dex=token_info,
                coingecko=coingecko_data,
                twitter=twitter_data,
                telegram=telegram_data
            )

        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            return None