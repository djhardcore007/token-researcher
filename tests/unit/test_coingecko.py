from unittest.mock import patch
from src.coingecko import CoinGecko
from src.schema import CoinGeckoSocial

def test_get_token_id():
    """Test getting token ID from contract address."""
    coingecko = CoinGecko()
    mock_data = {"id": "bitcoin"}

    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_data

        token_id = coingecko.get_token_id("0x123", "bitcoin")
        assert token_id == "bitcoin"

def test_get_social_info():
    """Test getting social info for a token."""
    coingecko = CoinGecko()
    mock_data = {
        "links": {
            "twitter_screen_name": "bitcoin",
            "telegram_channel_identifier": "bitcoin_telegram",
            "repos_url": {"github": ["https://github.com/bitcoin"]},
            "homepage": ["https://bitcoin.org"]
        }
    }

    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_data

        info = coingecko.get_social_info("bitcoin")
        assert isinstance(info, CoinGeckoSocial)
        assert info.twitter_handle == "bitcoin"
        assert info.telegram_handle == "bitcoin_telegram"
        assert info.github_repo == "https://github.com/bitcoin"
        assert info.website == "https://bitcoin.org"

def test_get_social_info_error():
    """Test error handling in social info."""
    coingecko = CoinGecko()

    with patch('requests.get', side_effect=Exception("API Error")):
        info = coingecko.get_social_info("bitcoin")
        assert isinstance(info, CoinGeckoSocial)
        assert info.twitter_handle is None
        assert info.telegram_handle is None