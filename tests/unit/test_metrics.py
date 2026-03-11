from __future__ import annotations

import pandas as pd

from riskpulse.analytics.metrics import (
    annualized_volatility,
    cvar_95_1d,
    var_95_historical,
    var_95_parametric,
    worst_day,
)


def test_basic_metrics():
    r = pd.Series([0.01, -0.02, 0.03, -0.01, 0.005, -0.04, 0.02])
    assert annualized_volatility(r) is not None
    assert var_95_parametric(r) is not None
    assert var_95_historical(r) is not None
    assert cvar_95_1d(r) is not None
    assert worst_day(r) == -0.04
