import pytest
from src.twitter import TwitterResearcher
from src.schema import TwitterResponse


TEST_ACCOUNT = "elonmusk"
TEST_ACCOUNT_INVALID = "thisusershouldnotexist12345abc"


@pytest.mark.integration
def test_integration_twitter():
    """Test Twitter API with test account."""
    twitter = TwitterResearcher()

    response = twitter.get_twitter_info(TEST_ACCOUNT)
    assert isinstance(response, TwitterResponse)

    assert response.user.twitter_handle == TEST_ACCOUNT
    assert response.user.twitter_followers > 0
    assert response.user.twitter_description

    assert len(response.recent_tweets) > 0
    assert response.recent_tweets[0].tweet_likes > 0

    assert response.metrics.num_recent_posts >= 0
    assert response.metrics.avg_engagement >= 0
    assert response.metrics.avg_impressions >= 0
    assert response.metrics.engagement_rate >= 0


@pytest.mark.integration
def test_integration_twitter_invalid_user():
    """Test Twitter API with invalid username."""
    twitter = TwitterResearcher()
    response = twitter.get_twitter_info(TEST_ACCOUNT_INVALID)
    assert response is None