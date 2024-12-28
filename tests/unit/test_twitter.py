import pytest
from datetime import datetime
from src.twitter import TwitterResearcher
from src.schema import TwitterUser, TwitterResponse

@pytest.fixture
def twitter():
    """Create TwitterResearcher instance."""
    return TwitterResearcher("test_token")

@pytest.fixture
def user_data():
    """Sample Twitter user data."""
    return {
        "id": 12345,
        "public_metrics": {"followers_count": 1000},
        "description": "Test account",
        "created_at": datetime(2020, 1, 1)
    }

@pytest.fixture
def tweet_data():
    """Sample tweet data."""
    return {
        "text": "Test tweet",
        "public_metrics": {"like_count": 1000},
        "created_at": datetime(2024, 1, 1)
    }

def test_twitter_user_from_data(user_data):
    """Test TwitterUser creation from data."""
    user = TwitterUser.from_api_response("example", user_data)

    assert user.twitter_handle == "example"
    assert user.twitter_id == 12345
    assert user.twitter_followers == 1000
    assert user.twitter_description == "Test account"
    assert user.twitter_created_at == datetime(2020, 1, 1)