from pydantic import BaseModel
from typing import Optional
import requests
from src.config import Config


class TokenMetadata(BaseModel):
    address: str
    name: str
    symbol: str
    icon: str
    decimals: int
    holder: int
    creator: str
    create_tx: str
    created_time: int
    first_mint_tx: str
    first_mint_time: int
    mint_authority: Optional[str]
    freeze_authority: Optional[str]
    supply: str
    price: float
    volume_24h: float
    market_cap: float
    market_cap_rank: int
    price_change_24h: float


class Solscan:
    def __init__(self):
        self.api_key = Config.SOLSCAN_API_KEY
        self.base_url = "https://pro-api.solscan.io/v2.0"
        self.headers = {"token": self.api_key}
        self.REPORT = {}

    def get_token_metadata(self, token_address: str) -> Optional[TokenMetadata]:
        try:
            url = f"{self.base_url}/token/meta?address={token_address}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            data = response.json()

            token_metadata = TokenMetadata.model_validate(data['data'])
            self.REPORT[token_address] = token_metadata
            return token_metadata

        except requests.RequestException as e:
            print(f"API request failed: {e}")
            return None
        except KeyError as e:
            print(f"Invalid response format: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None