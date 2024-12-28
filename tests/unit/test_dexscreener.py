import pytest
from src.dexscreener import DexScreener, get_token_addresses, research_tokens, save_results, setup_logger
import pandas as pd
from datetime import datetime
import os
import logging
from click.testing import CliRunner
from src.dexscreener import main

@pytest.fixture
def logger():
    return setup_logger(logging.DEBUG)

@pytest.fixture
def test_addresses():
    return [
        "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599",  # WBTC
        "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",  # WETH
        "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"   # USDC
    ]

@pytest.fixture
def temp_token_file(test_addresses, tmp_path):
    token_file = tmp_path / "test_tokens.txt"
    with open(token_file, "w") as f:
        f.write("\n".join(test_addresses))
    return token_file

def test_get_token_addresses(test_addresses, temp_token_file, logger):
    # Test comma-separated input
    tokens_str = ",".join(test_addresses)
    addresses = get_token_addresses(tokens=tokens_str, logger=logger)
    assert len(addresses) == len(test_addresses)
    assert all(addr in addresses for addr in test_addresses)

    # Test file input
    addresses = get_token_addresses(file=temp_token_file, logger=logger)
    assert len(addresses) == len(test_addresses)
    assert all(addr in addresses for addr in test_addresses)

def test_research_tokens(test_addresses, logger):
    addresses = set([test_addresses[0]])  # Just test with WBTC for speed
    results = research_tokens(addresses, logger)

    assert len(results) == 1
    result = results[0]

    # Check essential fields
    assert result['token_symbol'] == 'WBTC'
    assert float(result['price_usd']) > 0
    assert result['liquidity_usd'] is not None
    assert all(key in result for key in [
        'timestamp', 'token_name', 'chain', 'dex_id',
        'buys_24h', 'sells_24h', 'volume_24h'
    ])

def test_save_results(tmp_path, logger):
    # Prepare test data
    test_data = [{
        'token_symbol': 'TEST',
        'price_usd': '100',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }]

    output_dir = tmp_path / "test_output"
    save_results(test_data, output_dir, logger)

    # Check if file was created
    files = list(output_dir.glob("*.csv"))
    assert len(files) == 1

    # Verify content
    df = pd.read_csv(files[0])
    assert len(df) == 1
    assert df['token_symbol'].iloc[0] == 'TEST'

def test_cli_integration(temp_token_file, tmp_path):
    runner = CliRunner()
    output_dir = tmp_path / "cli_test_output"

    # Test with file input
    result = runner.invoke(main, [
        '-f', str(temp_token_file),
        '-o', str(output_dir),
        '--debug'
    ])

    assert result.exit_code == 0
    assert os.path.exists(output_dir)
    assert len(list(output_dir.glob("*.csv"))) == 1

def test_dexscreener_class():
    screener = DexScreener()
    token_address = "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599"  # WBTC

    # Test API connection
    token_data = screener.get_token_info(token_address)
    assert token_data is not None
    assert 'pairs' in token_data

    # Test data processing
    processed_data = screener.process_token_data(token_data)
    assert processed_data is not None
    assert processed_data['token_symbol'] == 'WBTC'

    # Test timeframe metrics
    timeframe_data = screener.get_timeframe_metrics(
        {'buys': 10, 'sells': 5},
        1000.0,
        '24h'
    )
    assert timeframe_data['buys_24h'] == 10
    assert timeframe_data['sells_24h'] == 5
    assert timeframe_data['total_txns_24h'] == 15
    assert timeframe_data['volume_24h'] == 1000.0

if __name__ == "__main__":
    pytest.main([__file__])