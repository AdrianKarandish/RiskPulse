from __future__ import annotations

import math
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import pandas as pd


REQUIRED_SELECTED_COLUMNS = {
    "Date",
    "stock_price",
    "stock_daily_return",
    "stock_cumulative_return",
    "benchmark_price",
    "benchmark_daily_return",
    "benchmark_cumulative_return",
}

REQUIRED_METRICS = {
    "max_drawdown_1y",
    "worst_5day",
    "var_95_parametric",
    "beta",
    "annualized_volatility",
    "piotroski_f_score",
    "worst_day",
    "var_95_historical",
    "cvar_95_1d",
    "downside_beta",
    "sortino",
}

REQUIRED_ARTIFACTS = {"main_csv", "price_csv", "cum_chart", "vol_chart"}


def validate_selected_frame(selected: pd.DataFrame) -> None:
    missing = REQUIRED_SELECTED_COLUMNS.difference(selected.columns)
    if missing:
        missing_cols = ", ".join(sorted(missing))
        raise ValueError(f"Selected analysis frame missing required columns: {missing_cols}")
    if len(selected) < 2:
        raise ValueError("Selected analysis frame must contain at least 2 rows.")


def validate_metrics(metrics: Mapping[str, Any]) -> None:
    missing = REQUIRED_METRICS.difference(metrics.keys())
    if missing:
        missing_names = ", ".join(sorted(missing))
        raise ValueError(f"Metrics payload missing required fields: {missing_names}")

    for name, value in metrics.items():
        if value is None:
            continue
        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            raise ValueError(f"Metric {name} must be finite when present.")


def validate_artifacts(artifacts: Mapping[str, str]) -> None:
    missing = REQUIRED_ARTIFACTS.difference(artifacts.keys())
    if missing:
        missing_names = ", ".join(sorted(missing))
        raise ValueError(f"Artifacts payload missing required fields: {missing_names}")

    for name, value in artifacts.items():
        artifact_path = Path(value)
        if not artifact_path.exists():
            raise ValueError(f"Artifact {name} was not created: {artifact_path}")
