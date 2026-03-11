from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

from riskpulse.analytics.metrics import (
    annualized_volatility,
    beta,
    cvar_95_1d,
    downside_beta,
    max_drawdown_1y,
    period_return,
    piotroski_f_score,
    sortino,
    var_95_historical,
    var_95_parametric,
    worst_5day,
    worst_day,
)
from riskpulse.data.market_data import build_selected_frame, fetch_fundamentals, fetch_prices
from riskpulse.domain.models import AnalysisRequest, AnalysisResult
from riskpulse.reporting.charts import cumulative_return_chart, volatility_chart
from riskpulse.reporting.csv_exporter import export_main_csv, export_price_only_csv
from riskpulse.reporting.filenames import cumulative_chart_path, price_csv_path, summary_csv_path, volatility_chart_path
from riskpulse.reporting.validation import validate_artifacts, validate_metrics, validate_selected_frame
from riskpulse.services.validation import validate_analysis_request


def run_analysis(request: AnalysisRequest) -> AnalysisResult:
    validate_analysis_request(request)
    warnings: list[str] = []

    extended_start = min(request.start, request.end - timedelta(days=420))
    stock_ext = fetch_prices(request.ticker, extended_start, request.end)
    bench_ext = fetch_prices(request.benchmark, extended_start, request.end)

    selected_stock = stock_ext[(stock_ext["Date"] >= request.start) & (stock_ext["Date"] <= request.end)].copy()
    selected_bench = bench_ext[(bench_ext["Date"] >= request.start) & (bench_ext["Date"] <= request.end)].copy()
    selected = build_selected_frame(selected_stock, selected_bench)
    validate_selected_frame(selected)

    sr = selected["stock_daily_return"]
    br = selected["benchmark_daily_return"]

    metrics = {
        "max_drawdown_1y": max_drawdown_1y(stock_ext["price"]),
        "worst_5day": worst_5day(selected["stock_price"]),
        "var_95_parametric": var_95_parametric(sr),
        "beta": beta(sr, br),
        "annualized_volatility": annualized_volatility(sr),
        "piotroski_f_score": None,
        "worst_day": worst_day(sr),
        "var_95_historical": var_95_historical(sr),
        "cvar_95_1d": cvar_95_1d(sr),
        "downside_beta": downside_beta(sr, br),
        "sortino": sortino(sr),
    }

    try:
        fundamentals = fetch_fundamentals(request.ticker)
        metrics["piotroski_f_score"] = piotroski_f_score(fundamentals)
        if metrics["piotroski_f_score"] is None:
            warnings.append("Piotroski F-score unavailable due to insufficient fundamentals.")
    except Exception as e:
        warnings.append(f"Fundamentals fetch failed: {e}")
    validate_metrics(metrics)

    period_returns = {
        "stock_period_return": period_return(selected["stock_price"]),
        "benchmark_period_return": period_return(selected["benchmark_price"]),
    }

    out = request.output_dir
    out.mkdir(parents=True, exist_ok=True)
    artifacts = {
        "main_csv": str(export_main_csv(selected, summary_csv_path(out, request))),
        "price_csv": str(export_price_only_csv(selected, price_csv_path(out, request))),
        "cum_chart": str(cumulative_return_chart(selected, cumulative_chart_path(out, request), request.ticker)),
        "vol_chart": str(volatility_chart(selected, volatility_chart_path(out, request))),
    }
    validate_artifacts(artifacts)

    return AnalysisResult(
        request=request,
        selected=selected,
        metrics=metrics,
        period_returns=period_returns,
        warnings=warnings,
        artifacts=artifacts,
    )
