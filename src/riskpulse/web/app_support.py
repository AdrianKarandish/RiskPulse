from __future__ import annotations

from datetime import date, datetime, time, timedelta
from pathlib import Path
from typing import Any

import pandas as pd

from riskpulse.cli.validators import (
    validate_date,
    validate_date_range,
    validate_output_dir,
    validate_rolling_days,
    validate_ticker,
)
from riskpulse.domain.models import AnalysisRequest, AnalysisResult
from riskpulse.services.analysis_service import run_analysis


METRIC_SPECS = [
    ("Annualized Volatility", "annualized_volatility", "percent"),
    ("Beta", "beta", "number"),
    ("CVaR 95% (1D)", "cvar_95_1d", "percent"),
    ("Downside Beta", "downside_beta", "number"),
    ("Historical VaR 95%", "var_95_historical", "percent"),
    ("Max Drawdown (1Y)", "max_drawdown_1y", "percent"),
    ("Parametric VaR 95%", "var_95_parametric", "percent"),
    ("Piotroski F-Score", "piotroski_f_score", "number"),
    ("Sortino Ratio", "sortino", "number"),
    ("Worst 5-Day Return", "worst_5day", "percent"),
    ("Worst Day Return", "worst_day", "percent"),
]


def _coerce_datetime(value: date | datetime) -> datetime:
    if isinstance(value, datetime):
        return value
    return datetime.combine(value, time.min)


def _format_metric_value(value: Any, kind: str) -> str:
    if value is None or pd.isna(value):
        return "N/A"
    if kind == "percent":
        return f"{float(value):.2%}"
    return f"{float(value):.3f}"


def run_web_analysis(
    *,
    ticker: str,
    use_rolling_window: bool,
    rolling_days: int | None,
    start_date: date | datetime | None,
    end_date: date | datetime | None,
    output_dir: Path = Path("outputs"),
    now: datetime | None = None,
) -> AnalysisResult:
    normalized_ticker = validate_ticker(ticker)
    normalized_output_dir = validate_output_dir(output_dir)
    reference_now = now or datetime.now()

    if use_rolling_window:
        if rolling_days is None:
            raise ValueError("Rolling days are required for rolling-window analysis.")
        validated_days = validate_rolling_days(rolling_days)
        end = reference_now
        start = end - timedelta(days=int(validated_days * 1.6))
    else:
        if start_date is None or end_date is None:
            raise ValueError("Start and end dates are required for custom-range analysis.")
        start = validate_date(_coerce_datetime(start_date).date().isoformat())
        end = validate_date(_coerce_datetime(end_date).date().isoformat())
        validate_date_range(start, end)

    request = AnalysisRequest(
        ticker=normalized_ticker,
        start=start,
        end=end,
        output_dir=normalized_output_dir,
    )
    return run_analysis(request)


def build_main_csv_bytes(selected: pd.DataFrame) -> bytes:
    cols = [
        "Date",
        "stock_price",
        "stock_daily_return",
        "stock_cumulative_return",
        "benchmark_price",
        "benchmark_daily_return",
        "benchmark_cumulative_return",
    ]
    return selected.loc[:, cols].to_csv(index=False).encode("utf-8")


def build_price_csv_bytes(selected: pd.DataFrame) -> bytes:
    return selected.loc[:, ["Date", "stock_price", "benchmark_price"]].to_csv(index=False).encode("utf-8")


def build_summary_csv_bytes(result: AnalysisResult) -> bytes:
    rows: list[dict[str, str]] = [
        {"section": "request", "name": "ticker", "value": result.request.ticker},
        {"section": "request", "name": "start", "value": result.request.start.date().isoformat()},
        {"section": "request", "name": "end", "value": result.request.end.date().isoformat()},
        {"section": "request", "name": "benchmark", "value": result.request.benchmark},
    ]

    for key, value in result.period_returns.items():
        rows.append({"section": "period_returns", "name": key, "value": "" if value is None else str(value)})
    for key, value in result.metrics.items():
        rows.append({"section": "metrics", "name": key, "value": "" if value is None else str(value)})
    for warning in result.warnings:
        rows.append({"section": "warnings", "name": "warning", "value": warning})
    for key, value in result.artifacts.items():
        rows.append({"section": "artifacts", "name": key, "value": value})

    return pd.DataFrame(rows).to_csv(index=False).encode("utf-8")


def build_metrics_table(result: AnalysisResult) -> pd.DataFrame:
    rows = []
    for label, key, kind in METRIC_SPECS:
        rows.append({"Metric": label, "Key": key, "Value": _format_metric_value(result.metrics.get(key), kind)})
    rows.append(
        {
            "Metric": "Stock Period Return",
            "Key": "stock_period_return",
            "Value": _format_metric_value(result.period_returns.get("stock_period_return"), "percent"),
        }
    )
    rows.append(
        {
            "Metric": "Benchmark Period Return",
            "Key": "benchmark_period_return",
            "Value": _format_metric_value(result.period_returns.get("benchmark_period_return"), "percent"),
        }
    )
    return pd.DataFrame(rows)


def build_cumulative_figure(
    selected: pd.DataFrame,
    *,
    ticker: str,
    benchmark_label: str = "S&P 500",
) -> Any:
    import plotly.graph_objects as go

    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=selected["Date"],
            y=selected["stock_cumulative_return"],
            mode="lines",
            name=ticker,
        )
    )
    figure.add_trace(
        go.Scatter(
            x=selected["Date"],
            y=selected["benchmark_cumulative_return"],
            mode="lines",
            name=benchmark_label,
        )
    )
    figure.update_layout(
        title="Cumulative Return Comparison",
        xaxis_title="Date",
        yaxis_title="Cumulative Return",
        legend_title="Series",
        margin=dict(l=20, r=20, t=60, b=20),
    )
    return figure


def build_volatility_figure(selected: pd.DataFrame, *, window: int = 20) -> Any:
    import plotly.graph_objects as go

    volatility = selected.copy()
    volatility["stock_volatility"] = volatility["stock_daily_return"].rolling(window).std() * (252 ** 0.5)
    volatility["benchmark_volatility"] = volatility["benchmark_daily_return"].rolling(window).std() * (252 ** 0.5)

    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=volatility["Date"],
            y=volatility["stock_volatility"],
            mode="lines",
            name="Stock Volatility",
        )
    )
    figure.add_trace(
        go.Scatter(
            x=volatility["Date"],
            y=volatility["benchmark_volatility"],
            mode="lines",
            name="Benchmark Volatility",
        )
    )
    figure.update_layout(
        title=f"Rolling {window}-Day Annualized Volatility",
        xaxis_title="Date",
        yaxis_title="Annualized Volatility",
        legend_title="Series",
        margin=dict(l=20, r=20, t=60, b=20),
    )
    return figure
