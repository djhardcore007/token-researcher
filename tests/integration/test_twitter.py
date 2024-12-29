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


@pytest.mark.integration
def test_integration_twitter_invalid_user():
    """Test Twitter API with invalid username."""
    twitter = TwitterResearcher()
    response = twitter.get_twitter_info(TEST_ACCOUNT_INVALID)
    assert response is None