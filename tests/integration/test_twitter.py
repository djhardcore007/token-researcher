import pytest
from src.twitter import TwitterResearcher
from src.schema import TwitterResponse

@pytest.mark.integration
def test_twitter():
    """Test Twitter API with Vitalik's account."""
    twitter = TwitterResearcher()

    response = twitter.get_twitter_info("djhardcore007")

    assert isinstance(response, TwitterResponse)
    # Check user info
    assert response.user.twitter_handle == "djhardcore007"
    assert response.user.twitter_followers > 0
    assert response.user.twitter_description

    # Check tweets
    assert len(response.popular_tweets) > 0
    assert response.popular_tweets[0].tweet_likes > 0

@pytest.mark.integration
def test_twitter_invalid_user():
    """Test Twitter API with invalid username."""
    twitter = TwitterResearcher()
    response = twitter.get_twitter_info("thisusershouldnotexist12345abc")
    assert response is None