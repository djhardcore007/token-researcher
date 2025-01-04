"""Metrics for token analysis."""

from datetime import datetime
from typing import List, Dict
from src.schema import Report
from src.metrics_schema import (
    VolumeMetrics,
    LiquidityMetrics,
    SocialMetrics,
    FinancialMetrics,
    KOLMetrics,
    WalletMetrics,
    TokenAnalysis
)


def calculate_volume_metrics(report: Report) -> VolumeMetrics:
    """Calculate volume and price related metrics"""
    price_24h = report.dex.price_usd
    volume_24h = report.dex.volume_24h
    circulating_supply = report.coingecko.market_data.circulating_supply or 0

    # Turnover Rate
    tr = (volume_24h / circulating_supply * 100) if circulating_supply > 0 else 0

    # Continuous Price Increase
    cpi = ((price_24h / (price_24h * (1 - report.dex.price_change_24h/100)))
           if report.dex.price_change_24h != 0 else 1)

    # Net Flow Ratio
    buys = report.dex.buys_24h
    sells = report.dex.sells_24h
    nfr = (buys - sells) / (buys + sells) if (buys + sells) > 0 else 0

    return VolumeMetrics(
        continuous_price_increase=cpi,
        turnover_rate=tr,
        net_flow_ratio=nfr
    )

def calculate_liquidity_metrics(report: Report) -> LiquidityMetrics:
    """Calculate liquidity related metrics"""
    liquidity = report.dex.liquidity_usd
    market_cap = report.dex.market_cap

    # Liquidity Depth
    ld = (liquidity / market_cap * 100) if market_cap > 0 else 0

    # Market Depth Ratio (simplified)
    mdr = liquidity / market_cap if market_cap > 0 else 0

    # Alpha Signal
    alpha = ld > 10

    return LiquidityMetrics(
        liquidity_depth=ld,
        market_depth_ratio=mdr,
        alpha_signal=alpha
    )

def calculate_social_metrics(report: Report) -> SocialMetrics:
    """Calculate social media related metrics"""
    if not report.twitter:
        return SocialMetrics(0, 0, 0)

    followers = report.twitter.user.twitter_followers
    total_engagement = sum(tweet.tweet_likes for tweet in report.twitter.recent_tweets)

    # Engagement Rate
    er = (total_engagement / followers * 100) if followers > 0 else 0

    # Social Dominance (simplified)
    sd = min(followers / 1_000_000 * 100, 100)

    # Sentiment Score
    ss = (report.coingecko.sentiment_votes_up_percentage -
          report.coingecko.sentiment_votes_down_percentage) / 100

    return SocialMetrics(
        social_dominance=sd,
        engagement_rate=er,
        sentiment_score=ss
    )

def calculate_financial_metrics(report: Report) -> FinancialMetrics:
    """Calculate financial metrics"""
    return FinancialMetrics(
        pe_ratio=None,
        revenue_growth_rate=None,
        revenue_per_token=None
    )

def calculate_wallet_metrics(report: Report, holders: List[Dict[str, float]]) -> WalletMetrics:
    """Calculate wallet concentration metrics"""
    total_supply = report.coingecko.market_data.total_supply or 0

    if not holders or total_supply == 0:
        return WalletMetrics(0, 0, 0)

    # Sort holders by balance
    sorted_holders = sorted(holders, key=lambda x: x['balance'], reverse=True)

    # Top holder concentrations
    top_10_sum = sum(h['balance'] for h in sorted_holders[:10])
    top_20_sum = sum(h['balance'] for h in sorted_holders[:20])

    # Gini coefficient calculation
    n = len(holders)
    mean_holding = sum(h['balance'] for h in holders) / n
    gini = sum(sum(abs(x['balance'] - y['balance'])
               for y in holders) for x in holders) / (2 * n * n * mean_holding)

    return WalletMetrics(
        gini_coefficient=gini,
        top_10_concentration=(top_10_sum / total_supply * 100),
        top_20_concentration=(top_20_sum / total_supply * 100)
    )


def calculate_kol_metrics(report: Report) -> KOLMetrics:
    """
    Calculate KOL (Key Opinion Leader) metrics based on:
    - Holding impact: Impact of large transactions on price
    - Movement impact: Price change after large transactions
    - Concentration index: Distribution of large holders
    """
    try:
        # Get DexScreener data
        dex = report.dex

        # Calculate holding impact (0-100)
        # Based on ratio of large transactions to total volume
        large_tx_threshold = dex.volume_24h * 0.05  # 5% of 24h volume
        large_buys = sum(1 for tx in range(dex.buys_24h) if dex.volume_24h/dex.buys_24h > large_tx_threshold) if dex.buys_24h > 0 else 0
        large_sells = sum(1 for tx in range(dex.sells_24h) if dex.volume_24h/dex.sells_24h > large_tx_threshold) if dex.sells_24h > 0 else 0

        total_txs = dex.total_txns_24h or 1
        holding_impact = min(100, (large_buys + large_sells) / total_txs * 100)

        # Calculate movement impact (-100 to 100)
        # Based on price change correlation with large transactions
        price_changes = [
            dex.price_change_5m,
            dex.price_change_1h,
            dex.price_change_6h,
            dex.price_change_24h
        ]

        avg_price_change = sum(price_changes) / len(price_changes) if price_changes else 0
        movement_impact = max(-100, min(100, avg_price_change))

        # Calculate concentration index (0-100)
        # Based on liquidity vs market cap ratio and transaction distribution
        if dex.market_cap > 0:
            liquidity_ratio = min(1, dex.liquidity_usd / dex.market_cap)
            tx_distribution = abs(dex.buys_24h - dex.sells_24h) / (dex.total_txns_24h or 1)
            concentration_index = (liquidity_ratio * 50 + tx_distribution * 50)
        else:
            concentration_index = 0

        return KOLMetrics(
            holding_impact=holding_impact,
            movement_impact=movement_impact,
            concentration_index=concentration_index
        )

    except Exception as e:
        print(f"Error calculating KOL metrics: {str(e)}")
        return KOLMetrics(0, 0, 0)


def analyze_token(report: Report, holders: List[Dict[str, float]] = None) -> TokenAnalysis:
    """Main analysis function that combines all metrics"""
    if not holders:
        wallet_metrics = None
    else:
        wallet_metrics = calculate_wallet_metrics(report, holders)

    return TokenAnalysis(
        timestamp=datetime.now(),
        volume_metrics=calculate_volume_metrics(report),
        liquidity_metrics=calculate_liquidity_metrics(report),
        financial_metrics=calculate_financial_metrics(report),
        social_metrics=calculate_social_metrics(report),
        kol_metrics=calculate_kol_metrics(report),
        wallet_metrics=wallet_metrics,
    )
