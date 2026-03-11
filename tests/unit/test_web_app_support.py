from __future__ import annotations

from datetime import date, datetime
from pathlib import Path

import pandas as pd
import pytest

from riskpulse.domain.models import AnalysisRequest, AnalysisResult
from riskpulse.web import app_support


def _sample_result(tmp_path: Path) -> AnalysisResult:
    selected = pd.DataFrame(
        {
            "Date": pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03"]),
            "stock_price": [100.0, 103.0, 101.0],
            "stock_daily_return": [None, 0.03, -0.0194174757],
            "stock_cumulative_return": [0.0, 0.03, 0.01],
            "benchmark_price": [200.0, 201.0, 205.0],
            "benchmark_daily_return": [None, 0.005, 0.0199004975],
            "benchmark_cumulative_return": [0.0, 0.005, 0.025],
        }
    )
    return AnalysisResult(
        request=AnalysisRequest(
            ticker="AAPL",
            start=datetime(2024, 1, 1),
            end=datetime(2024, 1, 3),
            output_dir=tmp_path,
        ),
        selected=selected,
        metrics={
            "annualized_volatility": 0.22,
            "beta": 1.1,
            "cvar_95_1d": 0.04,
            "downside_beta": 0.8,
            "max_drawdown_1y": -0.12,
            "piotroski_f_score": None,
            "sortino": 1.6,
            "var_95_historical": 0.03,
            "var_95_parametric": 0.035,
            "worst_5day": None,
            "worst_day": -0.02,
        },
        period_returns={
            "stock_period_return": 0.01,
            "benchmark_period_return": 0.025,
        },
        warnings=["Piotroski F-score unavailable due to insufficient fundamentals."],
        artifacts={"main_csv": "outputs/main.csv", "price_csv": "outputs/prices.csv", "cum_chart": "outputs/cum.png", "vol_chart": "outputs/vol.png"},
    )


def test_run_web_analysis_builds_rolling_request(monkeypatch, tmp_path: Path):
    captured: dict[str, object] = {}
    expected_result = _sample_result(tmp_path)

    def fake_run_analysis(request: AnalysisRequest) -> AnalysisResult:
        captured["request"] = request
        return expected_result

    monkeypatch.setattr(app_support, "run_analysis", fake_run_analysis)
    result = app_support.run_web_analysis(
        ticker=" aapl ",
        use_rolling_window=True,
        rolling_days=20,
        start_date=None,
        end_date=None,
        output_dir=tmp_path,
        now=datetime(2024, 6, 1, 12, 0, 0),
    )

    request = captured["request"]
    assert isinstance(request, AnalysisRequest)
    assert request.ticker == "AAPL"
    assert request.end == datetime(2024, 6, 1, 12, 0, 0)
    assert request.start == datetime(2024, 4, 30, 12, 0, 0)
    assert result is expected_result


def test_run_web_analysis_builds_custom_request(monkeypatch, tmp_path: Path):
    captured: dict[str, object] = {}

    def fake_run_analysis(request: AnalysisRequest) -> AnalysisResult:
        captured["request"] = request
        return _sample_result(tmp_path)

    monkeypatch.setattr(app_support, "run_analysis", fake_run_analysis)
    app_support.run_web_analysis(
        ticker="MSFT",
        use_rolling_window=False,
        rolling_days=None,
        start_date=date(2024, 1, 2),
        end_date=date(2024, 2, 2),
        output_dir=tmp_path,
    )

    request = captured["request"]
    assert isinstance(request, AnalysisRequest)
    assert request.start == datetime(2024, 1, 2)
    assert request.end == datetime(2024, 2, 2)


def test_run_web_analysis_rejects_missing_custom_dates(tmp_path: Path):
    with pytest.raises(ValueError, match="required for custom-range"):
        app_support.run_web_analysis(
            ticker="AAPL",
            use_rolling_window=False,
            rolling_days=None,
            start_date=None,
            end_date=None,
            output_dir=tmp_path,
        )


def test_build_csv_download_bytes_include_expected_headers(tmp_path: Path):
    result = _sample_result(tmp_path)

    main_csv = app_support.build_main_csv_bytes(result.selected).decode("utf-8")
    price_csv = app_support.build_price_csv_bytes(result.selected).decode("utf-8")
    summary_csv = app_support.build_summary_csv_bytes(result).decode("utf-8")

    assert "stock_daily_return" in main_csv
    assert "benchmark_price" in price_csv
    assert "section,name,value" in summary_csv
    assert "stock_period_return" in summary_csv


def test_build_metrics_table_formats_missing_and_percent_values(tmp_path: Path):
    result = _sample_result(tmp_path)

    table = app_support.build_metrics_table(result)

    assert table.loc[table["Key"] == "annualized_volatility", "Value"].item() == "22.00%"
    assert table.loc[table["Key"] == "piotroski_f_score", "Value"].item() == "N/A"
    assert table.loc[table["Key"] == "benchmark_period_return", "Value"].item() == "2.50%"


def test_chart_builders_return_plotly_figures(tmp_path: Path):
    go = pytest.importorskip("plotly.graph_objects")
    result = _sample_result(tmp_path)

    cumulative = app_support.build_cumulative_figure(result.selected, ticker="AAPL")
    volatility = app_support.build_volatility_figure(result.selected)

    assert isinstance(cumulative, go.Figure)
    assert isinstance(volatility, go.Figure)
    assert len(cumulative.data) == 2
    assert len(volatility.data) == 2
