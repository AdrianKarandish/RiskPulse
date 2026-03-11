from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd


@dataclass
class AnalysisRequest:
    ticker: str
    start: datetime
    end: datetime
    output_dir: Path
    benchmark: str = "^GSPC"


@dataclass
class AnalysisResult:
    request: AnalysisRequest
    selected: pd.DataFrame
    metrics: dict[str, Any]
    period_returns: dict[str, float | None]
    warnings: list[str]
    artifacts: dict[str, str]
