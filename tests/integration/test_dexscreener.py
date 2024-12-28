import pytest
from src.dexscreener import DexScreener

@pytest.mark.integration
def test_research_wbtc():
    """Test with real WBTC token."""
    dex = DexScreener()

    # WBTC address
    wbtc = "0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82"

    token = dex.research_tokens(wbtc)

    assert token is not None
    assert token.token_symbol == "Cake"
    assert token.chain == "bsc"
    assert token.price_usd > 0
    assert token.volume_24h > 0

@pytest.mark.integration
def test_research_invalid_token():
    """Test with invalid token address."""
    dex = DexScreener()
    token = dex.research_tokens("0xinvalid")
    assert token is None