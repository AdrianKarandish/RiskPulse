from __future__ import annotations

from pathlib import Path

from riskpulse.domain.models import AnalysisRequest


def _period_slug(request: AnalysisRequest) -> str:
    return request.selected_period.label.replace(":", "-")


def summary_csv_path(output_dir: Path, request: AnalysisRequest) -> Path:
    return output_dir / f"analysis_summary_{request.ticker}_{_period_slug(request)}.csv"


def price_csv_path(output_dir: Path, request: AnalysisRequest) -> Path:
    return output_dir / f"price_history_{request.ticker}_{_period_slug(request)}.csv"


def cumulative_chart_path(output_dir: Path, request: AnalysisRequest) -> Path:
    return output_dir / f"cumulative_returns_{request.ticker}_{_period_slug(request)}.png"


def volatility_chart_path(output_dir: Path, request: AnalysisRequest) -> Path:
    return output_dir / f"rolling_volatility_{request.ticker}_{_period_slug(request)}.png"
