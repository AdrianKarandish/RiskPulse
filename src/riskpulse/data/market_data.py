from __future__ import annotations

from datetime import datetime, timedelta

import pandas as pd
import yfinance as yf


def fetch_prices(ticker: str, start: datetime, end: datetime) -> pd.DataFrame:
    df = yf.download(ticker, start=start.date().isoformat(), end=(end + timedelta(days=1)).date().isoformat(), progress=False, auto_adjust=False)
    if df.empty:
        raise ValueError(f"No data for {ticker}")

    # yfinance can return MultiIndex columns even for one ticker.
    if isinstance(df.columns, pd.MultiIndex):
        flat = []
        for c in df.columns:
            c0 = c[0] if isinstance(c, tuple) else c
            flat.append(str(c0))
        df.columns = flat

    if "Adj Close" not in df.columns and "Close" in df.columns:
        df["Adj Close"] = df["Close"]

    out = df.reset_index()[["Date", "Adj Close"]].copy()
    out = out.rename(columns={"Adj Close": "price"})
    out["Date"] = pd.to_datetime(out["Date"]).dt.tz_localize(None)
    out["price"] = pd.to_numeric(out["price"], errors="coerce")
    out = out.dropna(subset=["price"])
    return out


def build_selected_frame(stock_df: pd.DataFrame, bench_df: pd.DataFrame) -> pd.DataFrame:
    s = stock_df.rename(columns={"price": "stock_price"})
    b = bench_df.rename(columns={"price": "benchmark_price"})
    d = s.merge(b, on="Date", how="inner").sort_values("Date").reset_index(drop=True)
    d["stock_daily_return"] = d["stock_price"].pct_change()
    d["benchmark_daily_return"] = d["benchmark_price"].pct_change()
    d["stock_cumulative_return"] = (1 + d["stock_daily_return"].fillna(0)).cumprod() - 1
    d["benchmark_cumulative_return"] = (1 + d["benchmark_daily_return"].fillna(0)).cumprod() - 1
    return d


def fetch_fundamentals(ticker: str) -> dict:
    t = yf.Ticker(ticker)
    return {
        "financials": getattr(t, "financials", None),
        "balance_sheet": getattr(t, "balance_sheet", None),
        "cashflow": getattr(t, "cashflow", None),
        "info": getattr(t, "info", {}) or {},
    }
