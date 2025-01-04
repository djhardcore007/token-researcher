from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class VolumeMetrics(BaseModel):
    continuous_price_increase: float
    turnover_rate: float
    net_flow_ratio: float


class LiquidityMetrics(BaseModel):
    liquidity_depth: float
    market_depth_ratio: float
    alpha_signal: bool


class WalletMetrics(BaseModel):
    gini_coefficient: float
    top_10_concentration: float
    top_20_concentration: float


class SocialMetrics(BaseModel):
    social_dominance: float
    engagement_rate: float
    sentiment_score: float


class FinancialMetrics(BaseModel):
    pe_ratio: Optional[float]
    revenue_growth_rate: Optional[float]
    revenue_per_token: Optional[float]


class KOLMetrics(BaseModel):
    holding_impact: float
    movement_impact: float
    concentration_index: float


class TokenAnalysis(BaseModel):
    timestamp: datetime
    volume_metrics: VolumeMetrics
    liquidity_metrics: LiquidityMetrics
    financial_metrics: FinancialMetrics
    social_metrics: SocialMetrics
    kol_metrics: KOLMetrics
    wallet_metrics: Optional[WalletMetrics] = None

    @classmethod
    def from_json(cls, json_str: str) -> 'TokenAnalysis':
        return cls.model_validate_json(json_str)
