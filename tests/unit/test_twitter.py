import pytest
from unittest.mock import patch, Mock
from datetime import datetime
from src.twitter import TwitterResearcher
from src.schema import TwitterUser, Tweet, TwitterResponse

def test_get_user_info():
    """Test getting basic Twitter user info."""
    twitter = TwitterResearcher("test_token")

    # Create mock user data
    mock_user = Mock()
    mock_user.data = Mock()
    mock_user.data.id = 12345
    mock_user.data.public_metrics = {'followers_count': 1000}
    mock_user.data.description = "Test account"
    mock_user.data.created_at = datetime(2020, 1, 1)

    with patch('tweepy.Client.get_user', return_value=mock_user):
        info = twitter.get_user_info("example")

        assert info.twitter_id == 12345
        assert info.twitter_handle == "example"
        assert info.twitter_followers == 1000
        assert info.twitter_description == "Test account"
        assert info.twitter_created_at == datetime(2020, 1, 1)

def test_get_popular_tweets():
    """Test getting popular tweets."""
    twitter = TwitterResearcher("test_token")

    # Create mock tweet
    mock_tweet = Mock()
    mock_tweet.text = "Test tweet"
    mock_tweet.created_at = datetime(2024, 1, 1)
    mock_tweet.public_metrics = {'like_count': 1000}

    mock_response = Mock()
    mock_response.data = [mock_tweet]

    with patch('tweepy.Client.get_users_tweets', return_value=mock_response):
        tweets = twitter.get_popular_tweets(123)

        assert len(tweets) == 1
        assert tweets[0].tweet_text == "Test tweet"
        assert tweets[0].tweet_likes == 1000
        assert tweets[0].tweet_created_at == datetime(2024, 1, 1)

def test_get_twitter_info():
    """Test getting complete Twitter info."""
    twitter = TwitterResearcher("test_token")

    # Mock user info
    mock_user = Mock()
    mock_user.data = Mock()
    mock_user.data.id = 12345
    mock_user.data.public_metrics = {'followers_count': 1000}
    mock_user.data.description = "Test account"
    mock_user.data.created_at = datetime(2020, 1, 1)

    # Mock tweet
    mock_tweet = Mock()
    mock_tweet.text = "Test tweet"
    mock_tweet.created_at = datetime(2024, 1, 1)
    mock_tweet.public_metrics = {'like_count': 1000}

    mock_tweets = Mock()
    mock_tweets.data = [mock_tweet]

    with patch('tweepy.Client.get_user', return_value=mock_user), \
         patch('tweepy.Client.get_users_tweets', return_value=mock_tweets):
        response = twitter.get_twitter_info("example")

        assert isinstance(response, TwitterResponse)
        assert response.user.twitter_id == 12345
        assert response.user.twitter_handle == "example"
        assert len(response.popular_tweets) == 1