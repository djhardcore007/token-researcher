import logging
import tweepy
from typing import Optional, List
from src.config import Config
from src.schema import TwitterUser, Tweet, TwitterResponse

class TwitterResearcher:
    def __init__(self, bearer_token: str = None):
        self.bearer_token = bearer_token or Config.TWITTER_BEARER_TOKEN
        if not self.bearer_token:
            raise ValueError("Twitter bearer token is required")

        self.client = tweepy.Client(bearer_token=self.bearer_token)
        self.logger = logging.getLogger(__name__)
        self.max_results = Config.TWITTER_MAX_RESULTS

    def get_user_info(self, twitter_handle: str) -> Optional[TwitterUser]:
        """Get basic Twitter user information."""
        if not twitter_handle:
            return None

        try:
            user = self.client.get_user(
                username=twitter_handle,
                user_fields=['public_metrics', 'description', 'created_at']
            )

            if not user.data:
                return None

            return TwitterUser.from_api_response(twitter_handle, user.data)

        except Exception as e:
            self.logger.error(f"Error getting Twitter user info: {str(e)}")
            return None

    def get_popular_tweets(self, user_id: int) -> List[Tweet]:
        """Get the 5 most popular tweets of a user."""
        try:
            tweets = self.client.get_users_tweets(
                user_id,
                max_results=self.max_results,
                tweet_fields=['public_metrics', 'created_at', 'text'],
                exclude=['retweets', 'replies']
            )

            if not tweets.data:
                return []

            # Sort by likes and get top 5
            sorted_tweets = sorted(
                tweets.data,
                key=lambda x: x.public_metrics['like_count'],
                reverse=True
            )[:5]

            return [
                Tweet(
                    tweet_text=tweet.text,
                    tweet_likes=tweet.public_metrics['like_count'],
                    tweet_created_at=tweet.created_at
                )
                for tweet in sorted_tweets
            ]

        except Exception as e:
            self.logger.error(f"Error getting popular tweets: {str(e)}")
            return []

    def get_twitter_info(self, twitter_handle: str) -> Optional[TwitterResponse]:
        """Get Twitter information including user info and popular tweets."""
        user_info = self.get_user_info(twitter_handle)
        if not user_info:
            return None

        popular_tweets = self.get_popular_tweets(user_info.twitter_id)
        return TwitterResponse(
            user=user_info,
            popular_tweets=popular_tweets
        )