import pytest
from unittest.mock import patch, Mock
from src.solscan import Solscan

@pytest.fixture
def solscan():
    return Solscan()

def test_get_token_metadata_success(solscan):
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": True,
            "data": {
                "address": "test123",
                "name": "Test Token",
                "symbol": "TEST",
                "icon": "https://example.com/icon.png",
                "decimals": 9,
                "holder": 1000,
                "creator": "creator123",
                "create_tx": "tx123",
                "created_time": 1234567890,
                "first_mint_tx": "mint123",
                "first_mint_time": 1234567890,
                "mint_authority": "auth123",
                "freeze_authority": "freeze123",
                "supply": "1000000",
                "price": 1.23,
                "volume_24h": 10000.0,
                "market_cap": 1230000.0,
                "market_cap_rank": 100,
                "price_change_24h": 5.5
            }
        }
        mock_get.return_value = mock_response

        result = solscan.get_token_metadata("test123")

        assert result is not None
        assert result.name == "Test Token"
        assert "test123" in solscan.REPORT

def test_get_token_metadata_error(solscan):
    with patch('requests.get') as mock_get:
        mock_get.side_effect = Exception("API Error")

        result = solscan.get_token_metadata("test123")

        assert result is None
        assert "test123" not in solscan.REPORT