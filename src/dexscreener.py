import logging
import requests
from typing import Optional, Dict
from datetime import datetime
from src.schema import TokenInfo

class DexScreener:
    def __init__(self):
        self.base_url = "https://api.dexscreener.com/latest/dex"
        self.logger = logging.getLogger(__name__)

    def get_token_info(self, address: str) -> Optional[Dict]:
        """Get token information from DexScreener API."""
        try:
            response = requests.get(f"{self.base_url}/tokens/{address}")
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            self.logger.error(f"Error getting token info: {str(e)}")
            return None

    def process_token_data(self, data: Dict) -> Optional[TokenInfo]:
        """Process raw token data into TokenInfo model."""
        try:
            if not data or 'pairs' not in data or not data['pairs']:
                return None

            pair = data['pairs'][0]  # Use first pair

            return TokenInfo(
                token_address=pair['baseToken']['address'],
                token_name=pair['baseToken']['name'],
                token_symbol=pair['baseToken']['symbol'],
                price_usd=float(pair.get('priceUsd', 0)),
                price_native=float(pair.get('priceNative', 0)),
                price_change_5m=float(pair.get('priceChange', {}).get('m5', 0)),
                price_change_1h=float(pair.get('priceChange', {}).get('h1', 0)),
                price_change_6h=float(pair.get('priceChange', {}).get('h6', 0)),
                price_change_24h=float(pair.get('priceChange', {}).get('h24', 0)),
                liquidity_usd=float(pair.get('liquidity', {}).get('usd', 0)),
                fdv=float(pair.get('fdv', 0)),
                market_cap=float(pair.get('marketCap', 0)),
                chain=pair['chainId'],
                dex_id=pair['dexId'],
                pair_address=pair['pairAddress'],
                timestamp=datetime.now(),

                # Transaction metrics
                buys_5m=pair.get('txns', {}).get('m5', {}).get('buys', 0),
                sells_5m=pair.get('txns', {}).get('m5', {}).get('sells', 0),
                total_txns_5m=pair.get('txns', {}).get('m5', {}).get('buys', 0) + pair.get('txns', {}).get('m5', {}).get('sells', 0),
                volume_5m=float(pair.get('volume', {}).get('m5', 0)),

                buys_1h=pair.get('txns', {}).get('h1', {}).get('buys', 0),
                sells_1h=pair.get('txns', {}).get('h1', {}).get('sells', 0),
                total_txns_1h=pair.get('txns', {}).get('h1', {}).get('buys', 0) + pair.get('txns', {}).get('h1', {}).get('sells', 0),
                volume_1h=float(pair.get('volume', {}).get('h1', 0)),

                buys_6h=pair.get('txns', {}).get('h6', {}).get('buys', 0),
                sells_6h=pair.get('txns', {}).get('h6', {}).get('sells', 0),
                total_txns_6h=pair.get('txns', {}).get('h6', {}).get('buys', 0) + pair.get('txns', {}).get('h6', {}).get('sells', 0),
                volume_6h=float(pair.get('volume', {}).get('h6', 0)),

                buys_24h=pair.get('txns', {}).get('h24', {}).get('buys', 0),
                sells_24h=pair.get('txns', {}).get('h24', {}).get('sells', 0),
                total_txns_24h=pair.get('txns', {}).get('h24', {}).get('buys', 0) + pair.get('txns', {}).get('h24', {}).get('sells', 0),
                volume_24h=float(pair.get('volume', {}).get('h24', 0))
            )

        except Exception as e:
            self.logger.error(f"Error processing token data: {str(e)}")
            return None

    def research_tokens(self, address: str) -> Optional[TokenInfo]:
        """Research single token and return result."""
        data = self.get_token_info(address)
        if data:
            return self.process_token_data(data)
        return None