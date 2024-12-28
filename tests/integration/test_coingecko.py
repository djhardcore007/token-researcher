import pytest
from src.coingecko import CoinGecko

@pytest.mark.integration
def test_coingecko_wbtc():
    """Test CoinGecko API with WBTC token."""
    coingecko = CoinGecko()

    # WBTC token address
    wbtc_address = "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599"

    # Get token ID
    token_id = coingecko.get_token_id(wbtc_address)
    assert token_id == "wrapped-bitcoin"

    # Get social info
    social_info = coingecko.get_social_info(token_id)

    assert social_info['twitter_handle'] is not None
    assert social_info['website'] is not None

@pytest.mark.integration
def test_coingecko_invalid_token():
    """Test CoinGecko API with invalid token."""
    coingecko = CoinGecko()

    # Test invalid address
    token_id = coingecko.get_token_id("0xinvalid")
    assert token_id is None