from pydantic import BaseModel, Field, model_validator
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from typing import Optional, Dict, List
from typing import List, Optional, Dict, Union
import json
from pathlib import Path
from dataclasses import dataclass, field
from pydantic import validator


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

from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field, model_validator
from datetime import datetime



class Image(BaseModel):
    thumb: Optional[str] = None
    small: Optional[str] = None
    large: Optional[str] = None

class ReposUrl(BaseModel):
    github: List[str] = Field(default_factory=list)
    bitbucket: List[str] = Field(default_factory=list)

class Links(BaseModel):
    homepage: List[str] = Field(default_factory=list)
    whitepaper: Optional[str] = None
    blockchain_site: List[str] = Field(default_factory=list)
    official_forum_url: List[str] = Field(default_factory=list)
    chat_url: List[str] = Field(default_factory=list)
    announcement_url: List[str] = Field(default_factory=list)
    snapshot_url: Optional[str] = None
    twitter_screen_name: Optional[str] = None
    facebook_username: Optional[str] = None
    bitcointalk_thread_identifier: Optional[Any] = None
    telegram_channel_identifier: Optional[str] = None
    subreddit_url: Optional[str] = None
    repos_url: ReposUrl = Field(default_factory=ReposUrl)

class CommunityData(BaseModel):
    facebook_likes: Optional[int] = None
    twitter_followers: Optional[int] = None
    reddit_average_posts_48h: float = 0.0
    reddit_average_comments_48h: float = 0.0
    reddit_subscribers: int = 0
    reddit_accounts_active_48h: int = 0
    telegram_channel_user_count: Optional[int] = None

class CodeAdditionsDeletions4Weeks(BaseModel):
    additions: Optional[Any] = None
    deletions: Optional[Any] = None

class DeveloperData(BaseModel):
    forks: int = 0
    stars: int = 0
    subscribers: int = 0
    total_issues: int = 0
    closed_issues: int = 0
    pull_requests_merged: int = 0
    pull_request_contributors: int = 0
    code_additions_deletions_4_weeks: CodeAdditionsDeletions4Weeks = Field(default_factory=CodeAdditionsDeletions4Weeks)
    commit_count_4_weeks: int = 0
    last_4_weeks_commit_activity_series: List[Any] = Field(default_factory=list)

class Market(BaseModel):
    name: str
    identifier: str
    has_trading_incentive: bool

class Ticker(BaseModel):
    base: str
    target: str
    market: Market
    last: float
    volume: float
    converted_last: Dict[str, float]
    converted_volume: Dict[str, float]
    trust_score: Optional[str] = None
    bid_ask_spread_percentage: Optional[float] = None
    timestamp: str
    last_traded_at: str
    last_fetch_at: str
    is_anomaly: bool
    is_stale: bool
    trade_url: Optional[str] = None
    token_info_url: Optional[str] = None
    coin_id: str
    target_coin_id: str

class MarketData(BaseModel):
    current_price: Dict[str, float] = Field(default_factory=dict)
    total_value_locked: Optional[Any] = None
    mcap_to_tvl_ratio: Optional[Any] = None
    fdv_to_tvl_ratio: Optional[Any] = None
    roi: Optional[Any] = None
    ath: Dict[str, float] = Field(default_factory=dict)
    ath_change_percentage: Dict[str, float] = Field(default_factory=dict)
    ath_date: Dict[str, str] = Field(default_factory=dict)
    atl: Dict[str, float] = Field(default_factory=dict)
    atl_change_percentage: Dict[str, float] = Field(default_factory=dict)
    atl_date: Dict[str, str] = Field(default_factory=dict)
    market_cap: Dict[str, float] = Field(default_factory=dict)
    market_cap_rank: Optional[int] = None
    fully_diluted_valuation: Dict[str, float] = Field(default_factory=dict)
    market_cap_fdv_ratio: Optional[float] = None
    total_volume: Dict[str, float] = Field(default_factory=dict)
    high_24h: Dict[str, float] = Field(default_factory=dict)
    low_24h: Dict[str, float] = Field(default_factory=dict)
    price_change_24h: Optional[float] = None
    price_change_percentage_24h: Optional[float] = None
    price_change_percentage_7d: Optional[float] = None
    price_change_percentage_14d: Optional[float] = None
    price_change_percentage_30d: Dict[str, float] = Field(default_factory=dict)
    price_change_percentage_60d: Dict[str, float] = Field(default_factory=dict)
    price_change_percentage_200d: Dict[str, float] = Field(default_factory=dict)
    price_change_percentage_1y: Dict[str, float] = Field(default_factory=dict)
    market_cap_change_24h: Optional[float] = None
    market_cap_change_percentage_24h: Optional[float] = None
    total_supply: Optional[float] = None
    max_supply: Optional[float] = None
    max_supply_infinite: Optional[bool] = None
    circulating_supply: Optional[float] = None
    last_updated: Optional[str] = None

class CoingeckoReport(BaseModel):
    id: str = ""
    symbol: str = ""
    name: str = ""
    web_slug: Optional[str] = None
    asset_platform_id: Optional[str] = None
    block_time_in_minutes: int = 0
    hashing_algorithm: Optional[str] = None
    categories: List[str] = Field(default_factory=list)
    preview_listing: bool = False
    public_notice: Optional[str] = None
    additional_notices: Optional[List[str]] = None
    localization: Optional[Dict[str, str]] = None
    description: str = ""
    links: Optional[Links] = None
    image: Optional[Image] = None
    country_origin: Optional[str] = None
    genesis_date: Optional[str] = None
    contract_address: Optional[str] = None
    sentiment_votes_up_percentage: float = 0.0
    sentiment_votes_down_percentage: float = 0.0
    watchlist_portfolio_users: int = 0
    market_cap_rank: Optional[int] = None
    market_data: MarketData = Field(default_factory=MarketData)
    community_data: CommunityData = Field(default_factory=CommunityData)
    developer_data: DeveloperData = Field(default_factory=DeveloperData)
    status_updates: Optional[List[Any]] = None
    last_updated: Optional[str] = None
    tickers: Optional[List[Ticker]] = None

    class Config:
        extra = "ignore"

    @model_validator(mode='before')
    @classmethod
    def validate_data(cls, values):
        if not isinstance(values, dict):
            return values
        return values

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
