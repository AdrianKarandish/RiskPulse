from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd
import pytest

from riskpulse.domain.models import AnalysisRequest
from riskpulse.reporting.validation import validate_artifacts, validate_metrics, validate_selected_frame
from riskpulse.services.validation import validate_analysis_request


def test_validate_analysis_request_rejects_reversed_dates(tmp_path: Path):
    request = AnalysisRequest(
        ticker="AAPL",
        start=datetime(2024, 2, 1),
        end=datetime(2024, 1, 1),
        output_dir=tmp_path,
    )

    with pytest.raises(ValueError, match="earlier than end"):
        validate_analysis_request(request)


def test_validate_analysis_request_rejects_output_file(tmp_path: Path):
    output_file = tmp_path / "results.csv"
    output_file.write_text("x", encoding="utf-8")
    request = AnalysisRequest(
        ticker="AAPL",
        start=datetime(2024, 1, 1),
        end=datetime(2024, 2, 1),
        output_dir=output_file,
    )

    with pytest.raises(ValueError, match="directory"):
        validate_analysis_request(request)


def test_validate_selected_frame_requires_rows():
    selected = pd.DataFrame(
        {
            "Date": pd.to_datetime(["2024-01-01"]),
            "stock_price": [100.0],
            "stock_daily_return": [None],
            "stock_cumulative_return": [0.0],
            "benchmark_price": [200.0],
            "benchmark_daily_return": [None],
            "benchmark_cumulative_return": [0.0],
        }
    )

    with pytest.raises(ValueError, match="at least 2 rows"):
        validate_selected_frame(selected)


def test_validate_metrics_rejects_non_finite_values():
    metrics = {
        "max_drawdown_1y": -0.2,
        "worst_5day": -0.1,
        "var_95_parametric": 0.03,
        "beta": 1.1,
        "annualized_volatility": float("nan"),
        "piotroski_f_score": None,
        "worst_day": -0.08,
        "var_95_historical": 0.02,
        "cvar_95_1d": 0.04,
        "downside_beta": 0.9,
        "sortino": 1.4,
    }

    with pytest.raises(ValueError, match="finite"):
        validate_metrics(metrics)


def test_validate_artifacts_requires_existing_files(tmp_path: Path):
    artifact = tmp_path / "missing.csv"

    with pytest.raises(ValueError, match="was not created"):
        validate_artifacts(
            {
                "main_csv": str(artifact),
                "price_csv": str(artifact),
                "cum_chart": str(artifact),
                "vol_chart": str(artifact),
            }
        )
