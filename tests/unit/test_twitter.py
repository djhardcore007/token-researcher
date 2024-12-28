import pytest
from datetime import datetime
from src.twitter import TwitterResearcher
from src.schema import TwitterUser, TwitterResponse, RecentTwitterMetrics


@pytest.fixture
def twitter():
    """Create TwitterResearcher instance."""
    return TwitterResearcher("test_bearer_token")


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


@pytest.fixture
def metrics_data():
    """Sample metrics data."""
    return {
        "num_recent_posts": 100,
        "avg_engagement": 150.5,
        "avg_impressions": 1000.0,
        "engagement_rate": 0.15
    }


def test_twitter_user_from_data(user_data):
    """Test TwitterUser creation from data."""
    user = TwitterUser.from_api_response("example", user_data)

    assert user.twitter_handle == "example"
    assert user.twitter_id == 12345
    assert user.twitter_followers == 1000
    assert user.twitter_description == "Test account"
    assert user.twitter_created_at == datetime(2020, 1, 1)


def test_twitter_metrics(twitter, metrics_data):
    """Test metrics calculation."""
    metrics = RecentTwitterMetrics(**metrics_data)

    assert metrics.num_recent_posts == 100
    assert metrics.avg_engagement == 150.5
    assert metrics.avg_impressions == 1000.0
    assert metrics.engagement_rate == 0.15


def test_twitter_response_with_metrics(user_data, tweet_data, metrics_data):
    """Test TwitterResponse creation with metrics."""
    user = TwitterUser.from_api_response("example", user_data)
    metrics = RecentTwitterMetrics(**metrics_data)

    response = TwitterResponse(
        user=user,
        recent_tweets=[],
        metrics=metrics
    )

    assert response.metrics.num_recent_posts == 100
    assert response.metrics.avg_engagement == 150.5
    assert response.metrics.avg_impressions == 1000.0
    assert response.metrics.engagement_rate == 0.15