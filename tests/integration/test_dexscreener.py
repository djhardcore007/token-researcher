import pytest

from src.dexscreener import DexScreener
from tests.conftest import TEST_TOKEN_ADDRESS, TEST_CHAIN, TEST_TOKEN_SYMBOL


@pytest.mark.integration
def test_integration_dexscreener():
    """Test with a sample token."""
    dex = DexScreener()


    token = dex.research_tokens(TEST_TOKEN_ADDRESS)

    assert token is not None
    assert token.token_symbol == TEST_TOKEN_SYMBOL
    assert token.chain == TEST_CHAIN
    assert token.price_usd > 0
    assert token.volume_24h > 0


@pytest.mark.integration
def test_integration_dexscreener_invalid_token():
    """Test with invalid token address."""
    dex = DexScreener()
    token = dex.research_tokens("0xinvalid")
    assert token is None