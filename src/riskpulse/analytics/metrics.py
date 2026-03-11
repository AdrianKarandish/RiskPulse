from __future__ import annotations

import math
from typing import Any

import numpy as np
import pandas as pd


Z_95 = 1.6448536269514722


def _clean(r: pd.Series) -> pd.Series:
    return r.dropna().astype(float)


def max_drawdown_1y(stock_prices: pd.Series) -> float | None:
    p = stock_prices.dropna()
    if len(p) < 2:
        return None
    p = p.tail(252)
    peak = p.cummax()
    dd = p / peak - 1
    return float(dd.min())


def worst_5day(stock_prices: pd.Series) -> float | None:
    p = stock_prices.dropna()
    if len(p) < 6:
        return None
    r5 = p.pct_change(5).dropna()
    return float(r5.min()) if not r5.empty else None


def var_95_parametric(returns: pd.Series) -> float | None:
    r = _clean(returns)
    if len(r) < 2:
        return None
    mu, sigma = float(r.mean()), float(r.std(ddof=1))
    return float(-(mu - Z_95 * sigma))


def var_95_historical(returns: pd.Series) -> float | None:
    r = _clean(returns)
    if len(r) < 2:
        return None
    return float(-np.quantile(r, 0.05))


def cvar_95_1d(returns: pd.Series) -> float | None:
    r = _clean(returns)
    if len(r) < 2:
        return None
    q = np.quantile(r, 0.05)
    tail = r[r <= q]
    if tail.empty:
        return None
    return float(-tail.mean())


def beta(stock_ret: pd.Series, bench_ret: pd.Series) -> float | None:
    d = pd.concat([stock_ret, bench_ret], axis=1).dropna()
    if len(d) < 2:
        return None
    cov = np.cov(d.iloc[:, 0], d.iloc[:, 1], ddof=1)[0, 1]
    varb = np.var(d.iloc[:, 1], ddof=1)
    if varb == 0:
        return None
    return float(cov / varb)


def downside_beta(stock_ret: pd.Series, bench_ret: pd.Series) -> float | None:
    d = pd.concat([stock_ret, bench_ret], axis=1).dropna()
    d = d[d.iloc[:, 1] < 0]
    if len(d) < 2:
        return None
    cov = np.cov(d.iloc[:, 0], d.iloc[:, 1], ddof=1)[0, 1]
    varb = np.var(d.iloc[:, 1], ddof=1)
    if varb == 0:
        return None
    return float(cov / varb)


def annualized_volatility(returns: pd.Series) -> float | None:
    r = _clean(returns)
    if len(r) < 2:
        return None
    return float(r.std(ddof=1) * math.sqrt(252))


def sortino(returns: pd.Series, annual_rf: float = 0.0) -> float | None:
    r = _clean(returns)
    if len(r) < 2:
        return None
    rf_daily = annual_rf / 252
    downside = r[r < rf_daily] - rf_daily
    if len(downside) < 2:
        return None
    denom = downside.std(ddof=1)
    if denom == 0:
        return None
    return float(((r.mean() - rf_daily) / denom) * math.sqrt(252))


def worst_day(returns: pd.Series) -> float | None:
    r = _clean(returns)
    return float(r.min()) if not r.empty else None


def period_return(prices: pd.Series) -> float | None:
    p = prices.dropna()
    if len(p) < 2:
        return None
    return float(p.iloc[-1] / p.iloc[0] - 1)


def piotroski_f_score(fundamentals: dict[str, Any]) -> float | None:
    try:
        fin = fundamentals.get("financials")
        bal = fundamentals.get("balance_sheet")
        cf = fundamentals.get("cashflow")
        info = fundamentals.get("info", {})
        if fin is None or bal is None or cf is None or fin.empty or bal.empty or cf.empty:
            return None
        cols = list(fin.columns)
        if len(cols) < 2:
            return None
        c, p = cols[0], cols[1]

        def g(df, row, col):
            return float(df.loc[row, col]) if row in df.index and col in df.columns and pd.notna(df.loc[row, col]) else None

        ni_c, ni_p = g(fin, "Net Income", c), g(fin, "Net Income", p)
        ocf_c = g(cf, "Operating Cash Flow", c)
        ta_c, ta_p = g(bal, "Total Assets", c), g(bal, "Total Assets", p)
        ltd_c, ltd_p = g(bal, "Long Term Debt", c), g(bal, "Long Term Debt", p)
        ca_c, ca_p = g(bal, "Current Assets", c), g(bal, "Current Assets", p)
        cl_c, cl_p = g(bal, "Current Liabilities", c), g(bal, "Current Liabilities", p)
        gp_c, gp_p = g(fin, "Gross Profit", c), g(fin, "Gross Profit", p)
        rev_c, rev_p = g(fin, "Total Revenue", c), g(fin, "Total Revenue", p)
        shares = info.get("sharesOutstanding")

        score = 0
        if ni_c is not None and ni_c > 0: score += 1
        if ocf_c is not None and ocf_c > 0: score += 1
        if ni_c is not None and ocf_c is not None and ocf_c > ni_c: score += 1
        if all(v is not None for v in [ni_c, ni_p, ta_c, ta_p]) and ta_c > 0 and ta_p > 0 and (ni_c/ta_c) > (ni_p/ta_p): score += 1
        if all(v is not None for v in [ltd_c, ltd_p, ta_c, ta_p]) and ta_c > 0 and ta_p > 0 and (ltd_c/ta_c) < (ltd_p/ta_p): score += 1
        if all(v is not None for v in [ca_c, ca_p, cl_c, cl_p]) and cl_c > 0 and cl_p > 0 and (ca_c/cl_c) > (ca_p/cl_p): score += 1
        if shares is None: score += 1
        if all(v is not None for v in [gp_c, gp_p, rev_c, rev_p]) and rev_c > 0 and rev_p > 0 and (gp_c/rev_c) > (gp_p/rev_p): score += 1
        if all(v is not None for v in [rev_c, rev_p, ta_c, ta_p]) and ta_c > 0 and ta_p > 0 and (rev_c/ta_c) > (rev_p/ta_p): score += 1
        return float(score)
    except Exception:
        return None
