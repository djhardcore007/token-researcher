import logging
from typing import Optional
import requests
from src.schema import (
    CoingeckoReport,
    CommunityData,
    DeveloperData,
    Links,
    Image,
    Platforms,
    DetailPlatforms,
    Description
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
                platforms=Platforms(**data['platforms']),
                detail_platforms=DetailPlatforms(**data['detail_platforms']),
                block_time_in_minutes=data['block_time_in_minutes'],
                hashing_algorithm=data['hashing_algorithm'],
                categories=data['categories'],
                preview_listing=data['preview_listing'],
                public_notice=data['public_notice'],
                additional_notices=data['additional_notices'],
                description=Description(**data['description']) if data['description'] else None,
                links=Links(**data['links']) if data['links'] else None,
                image=Image(**data['image']) if data['image'] else None,
                country_origin=data['country_origin'],
                genesis_date=data['genesis_date'],
                contract_address=data['contract_address'],
                sentiment_votes_up_percentage=data['sentiment_votes_up_percentage'],
                sentiment_votes_down_percentage=data['sentiment_votes_down_percentage'],
                watchlist_portfolio_users=data['watchlist_portfolio_users'],
                market_cap_rank=data['market_cap_rank'],
                community_data=CommunityData(**data['community_data']),
                developer_data=DeveloperData(**data['developer_data']),
                status_updates=data['status_updates'],
                last_updated=data['last_updated']
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