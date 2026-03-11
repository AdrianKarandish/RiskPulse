from __future__ import annotations

from pathlib import Path

from riskpulse.domain.models import AnalysisRequest


def _period_slug(request: AnalysisRequest) -> str:
    return f"{request.start.date()}_{request.end.date()}".replace(":", "-")


def summary_csv_path(output_dir: Path, request: AnalysisRequest) -> Path:
    return output_dir / f"riskpulse_main_{request.ticker}_{_period_slug(request)}.csv"


def price_csv_path(output_dir: Path, request: AnalysisRequest) -> Path:
    return output_dir / f"riskpulse_prices_{request.ticker}_{_period_slug(request)}.csv"


def cumulative_chart_path(output_dir: Path, request: AnalysisRequest) -> Path:
    return output_dir / f"riskpulse_cumulative_{request.ticker}_{_period_slug(request)}.png"


def volatility_chart_path(output_dir: Path, request: AnalysisRequest) -> Path:
    return output_dir / f"riskpulse_volatility_{request.ticker}_{_period_slug(request)}.png"
