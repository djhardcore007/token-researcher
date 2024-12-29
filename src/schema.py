from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, List
from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict, Union
import json
from pathlib import Path


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

###################### CoinGecko models ######################

class DetailPlatform(BaseModel):
    decimal_place: int
    contract_address: str

class Platforms(BaseModel):
    solana: str

class DetailPlatforms(BaseModel):
    solana: DetailPlatform

class Description(BaseModel):
    en: str

class Links(BaseModel):
    homepage: List[HttpUrl]
    whitepaper: Optional[str]
    blockchain_site: List[HttpUrl]
    official_forum_url: List[str]
    chat_url: List[str]
    announcement_url: List[str]
    snapshot_url: Optional[str]
    twitter_screen_name: Optional[str]
    facebook_username: Optional[str]
    bitcointalk_thread_identifier: Optional[str]
    telegram_channel_identifier: Optional[str]
    subreddit_url: Optional[HttpUrl]
    repos_url: Dict[str, List[str]]

class Image(BaseModel):
    thumb: HttpUrl
    small: HttpUrl
    large: HttpUrl

class CommunityData(BaseModel):
    facebook_likes: Optional[int]
    twitter_followers: Optional[int]
    reddit_average_posts_48h: float
    reddit_average_comments_48h: float
    reddit_subscribers: int
    reddit_accounts_active_48h: int
    telegram_channel_user_count: int

class CodeAdditionsDeletions(BaseModel):
    additions: Optional[int]
    deletions: Optional[int]

class DeveloperData(BaseModel):
    forks: int
    stars: int
    subscribers: int
    total_issues: int
    closed_issues: int
    pull_requests_merged: int
    pull_request_contributors: int
    code_additions_deletions_4_weeks: CodeAdditionsDeletions
    commit_count_4_weeks: int
    last_4_weeks_commit_activity_series: List[int]

class CoingeckoReport(BaseModel):
    id: str
    symbol: str
    name: str
    web_slug: str
    asset_platform_id: str
    platforms: Platforms
    detail_platforms: DetailPlatforms
    block_time_in_minutes: int
    hashing_algorithm: Optional[str]
    categories: List[str]
    preview_listing: bool
    public_notice: Optional[str]
    additional_notices: List[str]
    description: Optional[Description]
    links: Optional[Links]
    image: Optional[Image]
    country_origin: Optional[str]
    genesis_date: Optional[str]
    contract_address: Optional[str]
    sentiment_votes_up_percentage: Optional[float]
    sentiment_votes_down_percentage: Optional[float]
    watchlist_portfolio_users: Optional[int]
    market_cap_rank: Optional[int]
    community_data: Optional[CommunityData]
    developer_data: Optional[DeveloperData]
    status_updates: List[dict]
    last_updated: str


###################### DexScreener models ######################

class DexScreenerInfo(BaseModel):
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
    num_holders: int = 0

    # DexScreener data
    dex: DexScreenerInfo

    # CoinGecko data
    coingecko: CoingeckoReport

    # Social data
    twitter: Optional[TwitterResponse] = None
    telegram: Optional[TelegramChannel] = None

    @classmethod
    def from_json(cls, json_path: Union[str, Path]) -> 'Report':
        """Load a TokenReport from a JSON file"""
        with open(json_path, 'r') as f:
            data = json.load(f)
            # Convert string timestamp back to datetime if needed
            if isinstance(data.get('timestamp'), str):
                data['timestamp'] = datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00'))
            return cls(**data)