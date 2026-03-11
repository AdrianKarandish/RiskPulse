from __future__ import annotations

from riskpulse.domain.models import AnalysisRequest


def validate_analysis_request(request: AnalysisRequest) -> None:
    if not request.ticker.strip():
        raise ValueError("Ticker cannot be empty.")
    if request.start >= request.end:
        raise ValueError("Analysis start must be earlier than end.")
    if request.output_dir.exists() and not request.output_dir.is_dir():
        raise ValueError("Output path must be a directory.")
