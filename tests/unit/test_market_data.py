from __future__ import annotations

import pandas as pd
import pytest

from riskpulse.data.market_data import build_selected_frame


def test_build_selected_frame_requires_overlap():
    stock = pd.DataFrame(
        {
            "Date": pd.to_datetime(["2024-01-01", "2024-01-02"]),
            "price": [100.0, 101.0],
        }
    )
    bench = pd.DataFrame(
        {
            "Date": pd.to_datetime(["2024-02-01", "2024-02-02"]),
            "price": [200.0, 201.0],
        }
    )

    with pytest.raises(ValueError, match="overlapping trading days"):
        build_selected_frame(stock, bench)


def test_build_selected_frame_requires_expected_columns():
    stock = pd.DataFrame({"Date": pd.to_datetime(["2024-01-01", "2024-01-02"]), "close": [100.0, 101.0]})
    bench = pd.DataFrame(
        {
            "Date": pd.to_datetime(["2024-01-01", "2024-01-02"]),
            "price": [200.0, 201.0],
        }
    )

    with pytest.raises(ValueError, match="missing required columns"):
        build_selected_frame(stock, bench)


def test_build_selected_frame_normalizes_and_deduplicates_rows():
    stock = pd.DataFrame(
        {
            "Date": ["2024-01-01", "2024-01-02", "2024-01-02"],
            "price": ["100", "101", "102"],
        }
    )
    bench = pd.DataFrame(
        {
            "Date": pd.to_datetime(["2024-01-01", "2024-01-02"]),
            "price": [200.0, 202.0],
        }
    )

    selected = build_selected_frame(stock, bench)

    assert list(selected["stock_price"]) == [100.0, 102.0]
    assert len(selected) == 2
