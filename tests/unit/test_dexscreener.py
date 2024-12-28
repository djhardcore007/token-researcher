import pytest
from unittest.mock import patch
from datetime import datetime
from src.dexscreener import DexScreener

@pytest.fixture
def mock_token_data():
    """Mock DexScreener API response."""
    return {
        "pairs": [{
            "baseToken": {
                "address": "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599",
                "name": "Wrapped Bitcoin",
                "symbol": "WBTC"
            },
            "chainId": "ethereum",
            "dexId": "uniswap",
            "pairAddress": "0x123",
            "priceUsd": "30000",
            "priceNative": "15.5",
            "liquidity": {"usd": "1000000"},
            "volume": {
                "m5": "10000",
                "h1": "100000",
                "h6": "500000",
                "h24": "1000000"
            },
            "priceChange": {
                "m5": "1.2",
                "h1": "2.3",
                "h6": "3.4",
                "h24": "4.5"
            },
            "txns": {
                "m5": {"buys": 10, "sells": 5},
                "h1": {"buys": 100, "sells": 50},
                "h6": {"buys": 500, "sells": 250},
                "h24": {"buys": 1000, "sells": 500}
            },
            "fdv": "1000000000",
            "marketCap": "500000000"
        }]
    }

def test_get_token_info():
    """Test getting token info from API."""
    dex = DexScreener()

    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"pairs": []}

        info = dex.get_token_info("0x123")
        assert info is not None
        assert "pairs" in info

def test_process_token_data(mock_token_data):
    """Test processing token data."""
    dex = DexScreener()
    token = dex.process_token_data(mock_token_data)

    assert token is not None
    assert token.token_symbol == "WBTC"
    assert token.price_usd == 30000
    assert token.chain == "ethereum"
    assert token.buys_24h == 1000
    assert token.sells_24h == 500
    assert token.volume_24h == 1000000

def test_research_tokens():
    """Test researching a token."""
    dex = DexScreener()

    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "pairs": [{
                "baseToken": {
                    "address": "0x123",
                    "name": "Test Token",
                    "symbol": "TEST"
                },
                "chainId": "ethereum",
                "dexId": "uniswap",
                "pairAddress": "0x456",
                "priceUsd": "1.0"
            }]
        }

        token = dex.research_tokens("0x123")
        assert token is not None
        assert token.token_symbol == "TEST"