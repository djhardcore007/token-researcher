import logging
import requests
from typing import Optional

class CoinGecko:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.logger = logging.getLogger(__name__)

    def get_token_id(self, contract_address: str, chain: str = 'ethereum') -> Optional[str]:
        """Get CoinGecko token ID from contract address."""
        try:
            endpoint = f"{self.base_url}/coins/{chain}/contract/{contract_address}"
            response = requests.get(endpoint)
            if response.status_code == 200:
                return response.json().get('id')
            return None
        except Exception as e:
            self.logger.error(f"Error getting CoinGecko ID: {str(e)}")
            return None

    def get_social_info(self, coingecko_id: str) -> dict:
        """Get basic token social media information."""
        try:
            endpoint = f"{self.base_url}/coins/{coingecko_id}?localization=false&tickers=false&market_data=false&community_data=true&developer_data=false&sparkline=false"
            response = requests.get(endpoint)
            if response.status_code == 200:
                data = response.json()
                return {
                    'twitter_handle': data.get('links', {}).get('twitter_screen_name'),
                    'telegram_handle': data.get('links', {}).get('telegram_channel_identifier'),
                    'github_repo': data.get('links', {}).get('repos_url', {}).get('github', [None])[0],
                    'website': data.get('links', {}).get('homepage', [None])[0]
                }
            return {}
        except Exception as e:
            self.logger.error(f"Error getting social info: {str(e)}")
            return {}