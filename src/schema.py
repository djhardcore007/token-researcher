from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, List


# Twitter models
class TwitterUser(BaseModel):
    twitter_handle: str
    twitter_id: int
    twitter_followers: int = 0
    twitter_description: str = ""
    twitter_created_at: datetime

    @classmethod
    def from_api_response(cls, handle: str, data: Dict) -> 'TwitterUser':
        """Create TwitterUser from API response."""
        # Handle both string and datetime objects for created_at
        created_at = data.get('created_at')
        if isinstance(created_at, str):
            created_at = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%S.%fZ')
        elif not isinstance(created_at, datetime):
            created_at = datetime.now()  # fallback

        return cls(
            twitter_handle=handle,
            twitter_id=data.get('id'),
            twitter_followers=data.get('public_metrics', {}).get('followers_count', 0),
            twitter_description=data.get('description', ''),
            twitter_created_at=created_at
        )

class Tweet(BaseModel):
    tweet_text: str
    tweet_likes: int
    tweet_created_at: datetime

class RecentTwitterMetrics(BaseModel):
    num_recent_posts: int = 0
    avg_engagement: float = 0.0
    avg_impressions: float = 0.0
    engagement_rate: float = 0.0

class TwitterResponse(BaseModel):
    user: TwitterUser
    recent_tweets: List[Tweet] = []
    metrics: RecentTwitterMetrics = RecentTwitterMetrics()

# Telegram models
class TelegramChannel(BaseModel):
    telegram_handle: str
    member_count: int

# CoinGecko models
class CoinGeckoSocial(BaseModel):
    twitter_handle: Optional[str] = None
    telegram_handle: Optional[str] = None
    github_repo: Optional[str] = None
    website: Optional[str] = None

class CoinGeckoResponse(BaseModel):
    token_id: Optional[str] = None
    social_info: CoinGeckoSocial = CoinGeckoSocial()

# DexScreener models
class TokenInfo(BaseModel):
    # Basic token info
    token_address: str
    token_name: str
    token_symbol: str
    chain: str
    dex_id: str
    pair_address: str
    timestamp: datetime

    # Price metrics
    price_usd: float = 0.0
    price_native: float = 0.0
    price_change_5m: float = 0.0
    price_change_1h: float = 0.0
    price_change_6h: float = 0.0
    price_change_24h: float = 0.0

    # Financial metrics
    liquidity_usd: float = 0.0
    fdv: float = 0.0
    market_cap: float = 0.0

    # 5m metrics
    buys_5m: int = 0
    sells_5m: int = 0
    total_txns_5m: int = 0
    volume_5m: float = 0.0

    # 1h metrics
    buys_1h: int = 0
    sells_1h: int = 0
    total_txns_1h: int = 0
    volume_1h: float = 0.0

    # 6h metrics
    buys_6h: int = 0
    sells_6h: int = 0
    total_txns_6h: int = 0
    volume_6h: float = 0.0

    # 24h metrics
    buys_24h: int = 0
    sells_24h: int = 0
    total_txns_24h: int = 0
    volume_24h: float = 0.0


class Report(BaseModel):
    token_address: str
    chain: str
    timestamp: datetime

    # DexScreener data
    dex: TokenInfo

    # CoinGecko data
    coingecko: CoinGeckoResponse

    # Social data
    twitter: Optional[TwitterResponse] = None
    telegram: Optional[TelegramChannel] = None
