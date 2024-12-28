from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class TwitterUser(BaseModel):
    twitter_id: int
    twitter_handle: str
    twitter_followers: int
    twitter_description: str
    twitter_created_at: datetime

    @classmethod
    def from_api_response(cls, handle: str, user_data) -> 'TwitterUser':
        return cls(
            twitter_id=user_data.id,
            twitter_handle=handle,
            twitter_followers=user_data.public_metrics['followers_count'],
            twitter_description=user_data.description,
            twitter_created_at=user_data.created_at
        )

class Tweet(BaseModel):
    tweet_text: str
    tweet_likes: int
    tweet_created_at: datetime

class TwitterResponse(BaseModel):
    user: TwitterUser
    popular_tweets: List[Tweet] = []

class TelegramChannel(BaseModel):
    telegram_handle: str
    member_count: int
    description: Optional[str] = None
    created_at: Optional[datetime] = None

class TelegramResponse(BaseModel):
    channel: TelegramChannel