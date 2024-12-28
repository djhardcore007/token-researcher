import pytest
import logging
from click.testing import CliRunner


TEST_TOKEN_ADDRESS = "0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82"
TEST_CHAIN = "bsc"
TEST_TOKEN_SYMBOL = "Cake"
TEST_TOKEN_COINGECKO_ID = "pancakeswap-token"


@pytest.fixture(autouse=True)
def setup_logging():
    """Setup basic logging for tests."""
    logging.basicConfig(level=logging.INFO)


@pytest.fixture
def temp_output_dir(tmp_path):
    output_dir = tmp_path / "reports"
    output_dir.mkdir()
    return output_dir


@pytest.fixture
def runner():
    return CliRunner()