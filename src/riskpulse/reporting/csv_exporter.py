from __future__ import annotations

from pathlib import Path

import pandas as pd


def export_main_csv(selected: pd.DataFrame, output_path: Path) -> Path:
    cols = [
        "Date",
        "stock_price",
        "stock_daily_return",
        "stock_cumulative_return",
        "benchmark_price",
        "benchmark_daily_return",
        "benchmark_cumulative_return",
    ]
    out = selected[cols].copy()
    out.to_csv(output_path, index=False)
    return output_path


def export_price_only_csv(selected: pd.DataFrame, output_path: Path) -> Path:
    out = selected[["Date", "stock_price", "benchmark_price"]].copy()
    out.to_csv(output_path, index=False)
    return output_path
