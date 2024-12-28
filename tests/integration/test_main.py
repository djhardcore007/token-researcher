import pytest
import json
from pathlib import Path
from click.testing import CliRunner
from src.main import main

@pytest.fixture
def runner():
    return CliRunner()

@pytest.fixture
def temp_output_dir(tmp_path):
    output_dir = tmp_path / "reports"
    output_dir.mkdir()
    return output_dir

def test_main_cake(runner, temp_output_dir):
    """Test main with cake token."""
    result = runner.invoke(main, [
        '--token-address', '0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82',
        '--chain', 'bsc',
        '--output-dir', str(temp_output_dir)
    ])

    # Check command executed successfully
    assert result.exit_code == 0

    # Check report file was created
    report_files = list(temp_output_dir.glob("report_bsc_Cake_*.json"))
    assert len(report_files) == 1

    # Load and verify report content
    report = json.loads(report_files[0].read_text())
    assert report['chain'] == 'bsc'
    assert report['dex']['token_symbol'] == 'Cake'
    assert float(report['dex']['price_usd']) > 0


def test_main_invalid_token(runner, temp_output_dir):
    """Test main with invalid token."""
    result = runner.invoke(main, [
        '--token-address', '0xinvalid',
        '--output-dir', str(temp_output_dir)
    ])

    assert result.exit_code == 0  # Command should complete

    # No report file should be created
    report_files = list(temp_output_dir.glob("report_*.json"))
    assert len(report_files) == 0