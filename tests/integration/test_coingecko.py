import pytest
from src.coingecko import CoinGecko
from src.schema import CoinGeckoSocial, CoinGeckoResponse

@pytest.mark.integration
def test_coingecko_wbtc():
    """Test CoinGecko API with WBTC token."""
    coingecko = CoinGecko()

    # WBTC token address
    wbtc_address = "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599"

    # Get complete info
    response = coingecko.get_coin_info(wbtc_address, "ethereum")

    assert isinstance(response, CoinGeckoResponse)
    assert response.token_id == "wrapped-bitcoin"
    assert isinstance(response.social_info, CoinGeckoSocial)
    assert response.social_info.twitter_handle is not None
    assert response.social_info.website is not None

@pytest.mark.integration
def test_coingecko_invalid_token():
    """Test CoinGecko API with invalid token."""
    coingecko = CoinGecko()

    response = coingecko.get_coin_info("0xinvalid", "ethereum")
    assert isinstance(response, CoinGeckoResponse)
    assert response.token_id is None
    assert isinstance(response.social_info, CoinGeckoSocial)
    assert response.social_info.twitter_handle is None