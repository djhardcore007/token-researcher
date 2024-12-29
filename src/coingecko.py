import logging
from typing import Optional
import requests
from src.schema import (
    CoingeckoReport,
    CommunityData,
    DeveloperData,
    Links,
    Image,
)

class CoinGecko:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"


    def parse_coin_data(self, data: dict) -> Optional[CoingeckoReport]:
        """Parse CoinGecko API response into CoingeckoReport"""
        try:
            # Create the CoingeckoReport instance
            parsed_data = CoingeckoReport(
                id=data['id'],
                symbol=data['symbol'],
                name=data['name'],
                web_slug=data['web_slug'],
                asset_platform_id=data['asset_platform_id'],
                block_time_in_minutes=data['block_time_in_minutes'],
                hashing_algorithm=data['hashing_algorithm'],
                categories=data['categories'],
                preview_listing=data['preview_listing'],
                public_notice=data['public_notice'],
                additional_notices=data['additional_notices'],
                description=data['description']["en"],
                links=Links(**data['links']) if data['links'] else None,
                image=Image(**data['image']) if data['image'] else None,
                country_origin=data['country_origin'],
                genesis_date=data['genesis_date'],
                contract_address=data['contract_address'],
                sentiment_votes_up_percentage=data['sentiment_votes_up_percentage'] if data['sentiment_votes_up_percentage'] else 0,
                sentiment_votes_down_percentage=data['sentiment_votes_down_percentage'] if data['sentiment_votes_down_percentage'] else 0,
                watchlist_portfolio_users=data['watchlist_portfolio_users'] if data['watchlist_portfolio_users'] else 0,
                market_cap_rank=data['market_cap_rank'] if data['market_cap_rank'] else None,
                community_data=CommunityData(**data['community_data']) if data['community_data'] else None,
                developer_data=DeveloperData(**data['developer_data']) if data['developer_data'] else None,
                status_updates=data['status_updates'] if data['status_updates'] else None,
                last_updated=data['last_updated'] if data['last_updated'] else None
            )
            return parsed_data

        except Exception as e:
            logging.info(f"Error parsing coin data: {e}")
            return None

    def get_coin_info(self, contract_address: str, chain: str = 'solana') -> Optional[CoingeckoReport]:
        """Get and parse coin information from CoinGecko"""
        try:
            url = f"{self.base_url}/coins/{chain}/contract/{contract_address}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            return self.parse_coin_data(data)

        except Exception as e:
            logging.info(f"Error fetching coin info: {e}")
            return None


# Example usage
if __name__ == "__main__":
    coingecko = CoinGecko()

    # Example with JAIL token
    contract = "8cNmp9T2CMQRNZhNRoeSvr57LDf1kbZ42SvgsSWfpump"
    parsed_data = coingecko.get_coin_info(contract)