import pytest
from src.dexscreener import DexScreener
import pandas as pd
from datetime import datetime
import os

def test_real_token_integration():
    """
    Integration test using real WBTC token address on Ethereum
    """
    # Setup
    screener = DexScreener()
    wbtc_address = "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599"  # WBTC token

    # Test API connection and data fetching
    token_data = screener.get_token_info(wbtc_address)
    assert token_data is not None
    assert 'pairs' in token_data
    assert len(token_data['pairs']) > 0

    # Test data processing
    processed_data = screener.process_token_data(token_data)
    assert processed_data is not None

    # Verify essential fields
    assert processed_data['token_symbol'] == 'WBTC'
    assert float(processed_data['price_usd']) > 0
    assert processed_data['liquidity_usd'] is not None

    # Test CSV export
    results = [processed_data]
    df = pd.DataFrame(results)
    test_output_file = f"test_integration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    try:
        df.to_csv(test_output_file, index=False)
        assert os.path.exists(test_output_file)

        # Verify CSV content
        df_read = pd.read_csv(test_output_file)
        assert len(df_read) == 1
        assert df_read['token_symbol'].iloc[0] == 'WBTC'
    finally:
        # Cleanup
        if os.path.exists(test_output_file):
            os.remove(test_output_file)

def test_multiple_tokens_integration():
    """
    Integration test using multiple tokens
    """
    screener = DexScreener()
    token_addresses = [
        "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599",  # WBTC
        "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",  # WETH
        "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"   # USDC
    ]

    results = []
    for address in token_addresses:
        token_data = screener.get_token_info(address)
        processed_data = screener.process_token_data(token_data)
        assert processed_data is not None
        results.append(processed_data)

    # Verify we got data for all tokens
    assert len(results) == len(token_addresses)

    # Verify basic data for each token
    symbols = [data['token_symbol'] for data in results]

    assert 'WBTC' in symbols
    assert 'WETH' in symbols
    assert 'USDC' in symbols

if __name__ == "__main__":
    pytest.main([__file__])