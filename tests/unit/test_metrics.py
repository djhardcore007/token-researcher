import pytest
from pathlib import Path
from src.metrics import (
    calculate_volume_metrics,
    calculate_liquidity_metrics,
    calculate_financial_metrics,
    calculate_social_metrics,
    calculate_wallet_metrics,
    calculate_kol_metrics,
    analyze_token
)
from src.metrics_schema import TokenAnalysis
from src.schema import Report


TEST_FILES_DIR = Path("tests/test_files")


@pytest.fixture
def sample_report() -> Report:
    """Load a sample report from test files"""
    report_path = TEST_FILES_DIR / "sample_report.json"
    report = Report.from_json(report_path)
    yield report

def test_volume_metrics_calculation(sample_report):
    """Test volume metrics calculation"""

    metrics = calculate_volume_metrics(sample_report)
    assert metrics.turnover_rate >= 0
    assert -1 <= metrics.net_flow_ratio <= 1
    assert metrics.continuous_price_increase >= 0

def test_liquidity_metrics_calculation(sample_report):
    """Test liquidity metrics calculation"""
    metrics = calculate_liquidity_metrics(sample_report)
    assert metrics.liquidity_depth >= 0
    assert metrics.market_depth_ratio >= 0
    assert isinstance(metrics.alpha_signal, bool)

def test_social_metrics_calculation(sample_report):
    """Test social metrics calculation"""
    metrics = calculate_social_metrics(sample_report)
    assert 0 <= metrics.social_dominance <= 100
    assert metrics.engagement_rate >= 0
    assert -1 <= metrics.sentiment_score <= 1

def test_wallet_metrics_calculation(sample_report):
    """Test wallet metrics calculation"""
    holders = [
        {"address": "0x1", "balance": 1000},
        {"address": "0x2", "balance": 500}
    ]
    metrics = calculate_wallet_metrics(sample_report, holders)
    assert 0 <= metrics.gini_coefficient <= 1
    assert 0 <= metrics.top_10_concentration <= 100
    assert 0 <= metrics.top_20_concentration <= 100

def test_missing_twitter_data(sample_report):
    """Test handling of missing Twitter data"""
    sample_report.twitter = None
    metrics = calculate_social_metrics(sample_report)
    assert metrics.engagement_rate == 0
    assert metrics.social_dominance == 0
    assert metrics.sentiment_score == 0

def test_zero_market_cap(sample_report):
    """Test handling of zero market cap"""
    sample_report.dex.market_cap = 0
    metrics = calculate_liquidity_metrics(sample_report)
    assert metrics.liquidity_depth == 0
    assert metrics.market_depth_ratio == 0

def test_kol_metrics_calculation(sample_report):
    """Test KOL metrics calculation"""
    metrics = calculate_kol_metrics(sample_report)
    assert 0 <= metrics.holding_impact <= 1
    assert 0 <= metrics.movement_impact <= 1
    assert metrics.concentration_index >= 0

def test_financial_metrics_calculation(sample_report):
    """Test financial metrics calculation"""
    metrics = calculate_financial_metrics(sample_report)
    assert metrics.pe_ratio is None or metrics.pe_ratio >= 0
    assert metrics.revenue_growth_rate is None or metrics.revenue_growth_rate >= 0

def test_analyze_token(sample_report):
    """Test analyze_token function"""
    analysis = analyze_token(sample_report)
    assert isinstance(analysis, TokenAnalysis)