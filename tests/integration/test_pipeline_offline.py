from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd
import pytest

from riskpulse.analytics import metrics
from riskpulse.domain.models import AnalysisRequest
from riskpulse.services import analysis_service


def test_pipeline_with_monkeypatched_data(monkeypatch, tmp_path: Path):
    dates = pd.date_range("2024-01-01", periods=40, freq="B")
    stock = pd.DataFrame({"Date": dates, "price": [100 + i for i in range(40)]})
    bench = pd.DataFrame({"Date": dates, "price": [200 + i * 0.5 for i in range(40)]})

    def fake_fetch_prices(ticker, start, end):
        return stock if ticker != "^GSPC" else bench

    monkeypatch.setattr(analysis_service, "fetch_prices", fake_fetch_prices)
    monkeypatch.setattr(analysis_service, "fetch_fundamentals", lambda t: {})
    monkeypatch.setattr(metrics, "piotroski_f_score", lambda f: None)

    req = AnalysisRequest(ticker="AAPL", start=datetime(2024, 1, 1), end=datetime(2024, 2, 29), output_dir=tmp_path)
    result = analysis_service.run_analysis(req)

    assert result.artifacts["main_csv"].endswith(".csv")
    assert Path(result.artifacts["main_csv"]).exists()
    assert Path(result.artifacts["price_csv"]).exists()
    assert Path(result.artifacts["cum_chart"]).exists()
    assert Path(result.artifacts["vol_chart"]).exists()


def test_pipeline_fails_when_selected_window_has_no_overlap(monkeypatch, tmp_path: Path):
    stock = pd.DataFrame({"Date": pd.date_range("2024-01-01", periods=5, freq="B"), "price": [100 + i for i in range(5)]})
    bench = pd.DataFrame({"Date": pd.date_range("2024-03-01", periods=5, freq="B"), "price": [200 + i for i in range(5)]})

    def fake_fetch_prices(ticker, start, end):
        return stock if ticker != "^GSPC" else bench

    monkeypatch.setattr(analysis_service, "fetch_prices", fake_fetch_prices)

    req = AnalysisRequest(ticker="AAPL", start=datetime(2024, 1, 1), end=datetime(2024, 1, 31), output_dir=tmp_path)

    with pytest.raises(ValueError, match="No usable price rows for benchmark"):
        analysis_service.run_analysis(req)
