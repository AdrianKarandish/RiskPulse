from __future__ import annotations

from datetime import datetime, timedelta

import pandas as pd
import yfinance as yf


REQUIRED_PRICE_COLUMNS = {"Date", "price"}


def _normalize_price_frame(df: pd.DataFrame, *, ticker: str) -> pd.DataFrame:
    missing = REQUIRED_PRICE_COLUMNS.difference(df.columns)
    if missing:
        missing_cols = ", ".join(sorted(missing))
        raise ValueError(f"{ticker} price data missing required columns: {missing_cols}")

    out = df.loc[:, ["Date", "price"]].copy()
    out["Date"] = pd.to_datetime(out["Date"], errors="coerce").dt.tz_localize(None)
    out["price"] = pd.to_numeric(out["price"], errors="coerce")
    out = out.dropna(subset=["Date", "price"]).drop_duplicates(subset=["Date"], keep="last")
    out = out.sort_values("Date").reset_index(drop=True)
    if out.empty:
        raise ValueError(f"No usable price rows for {ticker}")
    return out


def fetch_prices(ticker: str, start: datetime, end: datetime) -> pd.DataFrame:
    if start >= end:
        raise ValueError("Price fetch start must be earlier than end.")

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
    return _normalize_price_frame(out, ticker=ticker)


def build_selected_frame(stock_df: pd.DataFrame, bench_df: pd.DataFrame) -> pd.DataFrame:
    s = _normalize_price_frame(stock_df, ticker="stock").rename(columns={"price": "stock_price"})
    b = _normalize_price_frame(bench_df, ticker="benchmark").rename(columns={"price": "benchmark_price"})
    d = s.merge(b, on="Date", how="inner").sort_values("Date").reset_index(drop=True)
    if len(d) < 2:
        raise ValueError("Need at least 2 overlapping trading days between stock and benchmark data.")
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
