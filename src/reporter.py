import logging
from datetime import datetime
from typing import Optional
from src.schema import Report
from src.dexscreener import DexScreener
from src.coingecko import CoinGecko
from src.twitter import TwitterResearcher
from src.telegram import TelegramResearcher
from src.holder_researcher import HolderResearcher

class Reporter:
    def __init__(self):
        self.dex = DexScreener()
        self.coingecko = CoinGecko()
        self.twitter = TwitterResearcher()
        self.telegram = TelegramResearcher()
        self.holder_researcher = HolderResearcher()
        self.logger = logging.getLogger(__name__)

    def generate_report(self, token_address: str, chain: str) -> Optional[Report]:
        """Generate a complete report for a token."""
        try:
            token_info = self.dex.research_tokens(token_address)
            if not token_info:
                return None

            assert token_info.chain == chain
            coingecko_data = self.coingecko.get_coin_info(token_address, chain)

            twitter_data = None
            twitter_handle = coingecko_data.links.twitter_screen_name
            if twitter_handle:
                twitter_data = self.twitter.get_twitter_info(twitter_handle)

            telegram_data = None
            telegram_handle = coingecko_data.links.telegram_channel_identifier
            if telegram_handle:
                telegram_data = self.telegram.get_channel_info(telegram_handle)

            num_holders = self.holder_researcher.get_holders(token_address, chain)
            # Combine all data
            report = Report(
                token_address=token_address,
                chain=chain,
                timestamp=datetime.now(),
                num_holders=num_holders,
                dex=token_info,
                coingecko=coingecko_data,
                twitter=twitter_data,
                telegram=telegram_data
            )
            return report

        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            return None