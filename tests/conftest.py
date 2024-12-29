import pytest
import logging
from click.testing import CliRunner


TEST_TOKEN_ADDRESS = "8cNmp9T2CMQRNZhNRoeSvr57LDf1kbZ42SvgsSWfpump"
TEST_CHAIN = "solana"
TEST_TOKEN_SYMBOL = "JAIL"
TEST_TOKEN_COINGECKO_ID = "jailbreakme"


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