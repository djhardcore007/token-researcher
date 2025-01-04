from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class VolumeMetrics:
    continuous_price_increase: float
    turnover_rate: float
    net_flow_ratio: float

@dataclass
class LiquidityMetrics:
    liquidity_depth: float
    market_depth_ratio: float
    alpha_signal: bool

@dataclass
class WalletMetrics:
    gini_coefficient: float
    top_10_concentration: float
    top_20_concentration: float

@dataclass
class SocialMetrics:
    social_dominance: float
    engagement_rate: float
    sentiment_score: float

@dataclass
class FinancialMetrics:
    pe_ratio: Optional[float]
    revenue_growth_rate: Optional[float]
    revenue_per_token: Optional[float]

@dataclass
class KOLMetrics:
    holding_impact: float
    movement_impact: float
    concentration_index: float

@dataclass
class TokenAnalysis:
    timestamp: datetime
    volume_metrics: VolumeMetrics
    liquidity_metrics: LiquidityMetrics
    financial_metrics: FinancialMetrics
    social_metrics: SocialMetrics
    kol_metrics: KOLMetrics
    wallet_metrics: Optional[WalletMetrics]
