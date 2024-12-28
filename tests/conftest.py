import pytest
import logging

@pytest.fixture(autouse=True)
def setup_logging():
    """Setup basic logging for tests."""
    logging.basicConfig(level=logging.INFO)