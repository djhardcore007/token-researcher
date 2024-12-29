import pytest
from src.coingecko import CoinGecko
from src.schema import CoingeckoReport
from tests.conftest import TEST_TOKEN_ADDRESS, TEST_CHAIN, TEST_TOKEN_SYMBOL


@pytest.mark.integration
def test_real_api_call():
    """Simple integration test"""
    coingecko = CoinGecko()
    result = coingecko.get_coin_info(TEST_TOKEN_ADDRESS, TEST_CHAIN)

    assert isinstance(result, CoingeckoReport)
    assert result is not None
    assert result.symbol.lower() == TEST_TOKEN_SYMBOL.lower()
    assert result.asset_platform_id == TEST_CHAIN


@pytest.mark.integration
def test_integration_coingecko_invalid_token():
    """Test CoinGecko API with invalid token."""
    coingecko = CoinGecko()

    response = coingecko.get_coin_info("0xinvalid", TEST_CHAIN)
    assert response is None
