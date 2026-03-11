from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def cumulative_return_chart(selected: pd.DataFrame, output_path: Path, ticker: str, benchmark: str = "S&P 500") -> Path:
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(selected["Date"], selected["stock_cumulative_return"], label=ticker)
    ax.plot(selected["Date"], selected["benchmark_cumulative_return"], label=benchmark)
    ax.set_title("Cumulative Return Comparison")
    ax.set_ylabel("Cumulative Return")
    ax.legend()
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    return output_path


def volatility_chart(selected: pd.DataFrame, output_path: Path, window: int = 20) -> Path:
    d = selected.copy()
    d["stock_vol"] = d["stock_daily_return"].rolling(window).std() * (252 ** 0.5)
    d["benchmark_vol"] = d["benchmark_daily_return"].rolling(window).std() * (252 ** 0.5)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(d["Date"], d["stock_vol"], label="Stock Vol")
    ax.plot(d["Date"], d["benchmark_vol"], label="Benchmark Vol")
    ax.set_title(f"Rolling {window}-Day Annualized Volatility")
    ax.legend()
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    return output_path
