import pytest
from unittest.mock import patch, Mock
from src.coingecko import CoinGecko
from src.schema import CoingeckoReport

@pytest.fixture
def coingecko():
    return CoinGecko()

@pytest.fixture
def mock_coin_data():
    """Minimal mock data for testing"""
    return {'id': 'jailbreakme', 'symbol': 'jail', 'name': 'JailbreakMe', 'web_slug': 'jailbreakme', 'asset_platform_id': 'solana', 'platforms': {'solana': '8cNmp9T2CMQRNZhNRoeSvr57LDf1kbZ42SvgsSWfpump'}, 'detail_platforms': {'solana': {'decimal_place': 6, 'contract_address': '8cNmp9T2CMQRNZhNRoeSvr57LDf1kbZ42SvgsSWfpump'}}, 'block_time_in_minutes': 0, 'hashing_algorithm': None, 'categories': ['Artificial Intelligence (AI)', 'Solana Ecosystem', 'Pump.fun Ecosystem'], 'preview_listing': False, 'public_notice': None, 'additional_notices': [], 'description': {'en': "The first open source, fairly launched dApp where organizations test their AI models while users earn rewards for finding weaknesses and jailbreaking them 🏆\r\n$JAIL tokens are designed to be the native currency of the JailbreakMe dApp, serving as the backbone of the platform's economy. While the full utility of $JAIL tokens will roll out in future updates, the groundwork is being laid to ensure their value and relevance within the ecosystem."}, 'links': {'homepage': ['https://jailbreakme.xyz/'], 'whitepaper': '', 'blockchain_site': ['https://solscan.io/token/8cNmp9T2CMQRNZhNRoeSvr57LDf1kbZ42SvgsSWfpump'], 'official_forum_url': [], 'chat_url': [], 'announcement_url': [], 'snapshot_url': None, 'twitter_screen_name': 'jailbreakme_xyz', 'facebook_username': '', 'bitcointalk_thread_identifier': None, 'telegram_channel_identifier': 'jailbreakme_xyz', 'subreddit_url': 'https://www.reddit.com', 'repos_url': {'github': [], 'bitbucket': []}}, 'image': {'thumb': 'https://coin-images.coingecko.com/coins/images/52620/thumb/stoneLogo.webp?1733784557', 'small': 'https://coin-images.coingecko.com/coins/images/52620/small/stoneLogo.webp?1733784557', 'large': 'https://coin-images.coingecko.com/coins/images/52620/large/stoneLogo.webp?1733784557'}, 'country_origin': '', 'genesis_date': None, 'contract_address': '8cNmp9T2CMQRNZhNRoeSvr57LDf1kbZ42SvgsSWfpump', 'sentiment_votes_up_percentage': 100.0, 'sentiment_votes_down_percentage': 0.0, 'watchlist_portfolio_users': 569, 'market_cap_rank': 2469, 'community_data': {'facebook_likes': None, 'twitter_followers': 11324, 'reddit_average_posts_48h': 0.0, 'reddit_average_comments_48h': 0.0, 'reddit_subscribers': 0, 'reddit_accounts_active_48h': 0, 'telegram_channel_user_count': 4649}, 'developer_data': {'forks': 0, 'stars': 0, 'subscribers': 0, 'total_issues': 0, 'closed_issues': 0, 'pull_requests_merged': 0, 'pull_request_contributors': 0, 'code_additions_deletions_4_weeks': {'additions': None, 'deletions': None}, 'commit_count_4_weeks': 0, 'last_4_weeks_commit_activity_series': []}, 'status_updates': [], 'last_updated': '2024-12-29T00:00:03.586Z'}

def test_parse_coin_data(coingecko, mock_coin_data):
    """Test basic data parsing"""
    result = coingecko.parse_coin_data(mock_coin_data)

    assert isinstance(result, CoingeckoReport)
    assert result.name == "JailbreakMe"
    assert result.symbol == "jail"
    assert result.contract_address == "8cNmp9T2CMQRNZhNRoeSvr57LDf1kbZ42SvgsSWfpump"

def test_get_coin_info(coingecko, mock_coin_data):
    """Test API call and parsing"""
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = mock_coin_data
        mock_get.return_value.status_code = 200

        result = coingecko.get_coin_info("test_contract")

        assert result is not None
        assert result.name == "JailbreakMe"
        assert result.symbol == "jail"

def test_get_coin_info_error(coingecko):
    """Test error handling"""
    with patch('requests.get') as mock_get:
        mock_get.side_effect = Exception("API Error")
        result = coingecko.get_coin_info("test_contract")
        assert result is None