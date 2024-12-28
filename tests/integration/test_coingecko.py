import pytest
from src.coingecko import CoinGecko
from src.schema import CoinGeckoSocial, CoinGeckoResponse
from tests.conftest import TEST_TOKEN_ADDRESS, TEST_CHAIN, TEST_TOKEN_COINGECKO_ID


@pytest.mark.integration
def test_integration_coingecko_token():
    """Test CoinGecko API with a sample token."""
    coingecko = CoinGecko()

    # WBTC token address
    response = coingecko.get_coin_info(TEST_TOKEN_ADDRESS, TEST_CHAIN)

    assert isinstance(response, CoinGeckoResponse)
    assert response.token_id == TEST_TOKEN_COINGECKO_ID
    assert isinstance(response.social_info, CoinGeckoSocial)
    assert response.social_info.twitter_handle is not None
    assert response.social_info.website is not None


@pytest.mark.integration
def test_integration_coingecko_invalid_token():
    """Test CoinGecko API with invalid token."""
    coingecko = CoinGecko()

    response = coingecko.get_coin_info("0xinvalid", TEST_CHAIN)
    assert isinstance(response, CoinGeckoResponse)
    assert response.token_id is None
    assert isinstance(response.social_info, CoinGeckoSocial)
    assert response.social_info.twitter_handle is None