from __future__ import annotations

import math

import numpy as np
import pandas as pd


def safe_std(series: pd.Series) -> float | None:
    clean = series.dropna()
    if len(clean) < 2:
        return None
    value = float(clean.std(ddof=1))
    return None if math.isnan(value) else value


def safe_covariance(left: pd.Series, right: pd.Series) -> float | None:
    aligned = pd.concat([left, right], axis=1).dropna()
    if len(aligned) < 2:
        return None
    value = float(np.cov(aligned.iloc[:, 0], aligned.iloc[:, 1], ddof=1)[0, 1])
    return None if math.isnan(value) else value


def normal_z_score(confidence: float) -> float:
    if abs(confidence - 0.95) < 1e-9:
        return 1.6448536269514722
    raise ValueError("Only 95% confidence is currently supported.")
