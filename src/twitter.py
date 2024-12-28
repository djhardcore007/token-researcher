import logging
import tweepy
from typing import Optional, Dict, List
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
            self.logger.error("Twitter handle is required")
            return None

        try:
            user = self.client.get_user(
                username=twitter_handle,
                user_fields=['id', 'public_metrics', 'description', 'created_at']
            )

            if not user or not user.data:
                self.logger.error(f"No user data found for {twitter_handle}")
                return None

            return TwitterUser.from_api_response(twitter_handle, user.data)

        except Exception as e:
            self.logger.error(f"Error getting Twitter user info: {str(e)}")
            return None

    def get_recent_tweets(self, user_id: int, max_results: int = 5) -> List[Tweet]:
        """Get the {max_results} most recent tweets of a user."""
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
            )[:max_results]

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

    def get_user_metrics(self, user_id: int) -> Dict[str, float]:
        """Calculate comprehensive user metrics."""
        try:
            # Get user tweets with all necessary metrics
            tweets = self.client.get_users_tweets(
                user_id,
                max_results=self.max_results,
                tweet_fields=['public_metrics', 'created_at', 'text'],
                exclude=['retweets']
            )

            if not tweets.data:
                return {}

            # Extract metrics from tweets
            likes = [t.public_metrics.get('like_count', 0) for t in tweets.data]
            replies = [t.public_metrics.get('reply_count', 0) for t in tweets.data]
            retweets = [t.public_metrics.get('retweet_count', 0) for t in tweets.data]
            impressions = [t.public_metrics.get('impression_count', 0) for t in tweets.data]

            metrics = {
                'num_recent_posts': len(tweets.data),
                'avg_engagement': self._calculate_avg_engagement(likes, replies, retweets),
                'avg_impressions': sum(impressions) / len(impressions) if impressions else 0,
                'engagement_rate': self._calculate_impressions_per_metric(
                    sum(impressions),
                    sum(likes) + sum(replies) + sum(retweets)
                ) if impressions else 0
            }

            return metrics

        except Exception as e:
            self.logger.error(f"Error calculating user metrics: {str(e)}")
            return {}

    def _calculate_avg_engagement(self, likes: List[int], replies: List[int], shares: List[int]) -> float:
        """Calculate average engagement per post."""
        total_engagement = [l + r + s for l, r, s in zip(likes, replies, shares)]
        return sum(total_engagement) / len(total_engagement) if total_engagement else 0

    def _calculate_impressions_per_metric(self, impressions: int, metric_counts: int) -> float:
        """Calculate impressions per metric count."""
        return impressions / metric_counts if metric_counts > 0 else 0

    def get_twitter_info(self, twitter_handle: str) -> Optional[TwitterResponse]:
        """Get Twitter information including user info, popular tweets, and metrics."""
        user_info = self.get_user_info(twitter_handle)
        if not user_info:
            return None

        recent_tweets = self.get_recent_tweets(user_info.twitter_id)
        metrics = self.get_user_metrics(user_info.twitter_id)

        return TwitterResponse(
            user=user_info,
            recent_tweets=recent_tweets,
            metrics=metrics
        )