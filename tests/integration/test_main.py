import json

from src.main import main
from tests.conftest import TEST_TOKEN_ADDRESS, TEST_CHAIN, TEST_TOKEN_SYMBOL


# def test_integration_main(runner, temp_output_dir):
#     """Test main with a sample token."""
#     result = runner.invoke(main, [
#         '--token-address', TEST_TOKEN_ADDRESS,
#         '--chain', TEST_CHAIN,
#         '--output-dir', str(temp_output_dir)
#     ])

#     # Check command executed successfully
#     assert result.exit_code == 0

#     # Check report file was created
#     report_files = list(temp_output_dir.glob(f"report_*.json"))
#     assert len(report_files) == 1

#     # Load and verify report content
#     report = json.loads(report_files[0].read_text())
#     assert report['chain'] == TEST_CHAIN
#     assert report['dex']['token_symbol'] == TEST_TOKEN_SYMBOL
#     assert float(report['dex']['price_usd']) > 0
#     # assert report['num_holders'] > 0


def test_integration_main_invalid(runner, temp_output_dir):
    """Test main with invalid token."""
    result = runner.invoke(main, [
        '--token-address', '0xinvalid',
        '--output-dir', str(temp_output_dir)
    ])

    assert result.exit_code == 0  # Command should complete

    # No report file should be created
    report_files = list(temp_output_dir.glob("report_*.json"))
    assert len(report_files) == 0