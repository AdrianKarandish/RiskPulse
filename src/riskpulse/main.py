from __future__ import annotations

import json
from datetime import timedelta

from riskpulse.cli.parser import parse_args
from riskpulse.domain.models import AnalysisRequest
from riskpulse.services.analysis_service import run_analysis
from riskpulse.utils.logging import configure_logging


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    configure_logging(args.verbose)

    if args.rolling_days is not None:
        end = args.end_date if args.end_date is not None else __import__("datetime").datetime.now()
        start = end - timedelta(days=int(args.rolling_days * 1.6))
    else:
        start, end = args.start_date, args.end_date

    request = AnalysisRequest(
        ticker=args.ticker,
        start=start,
        end=end,
        output_dir=args.output_dir,
    )
    result = run_analysis(request)
    payload = {
        "ticker": result.request.ticker,
        "period": {"start": str(result.request.start.date()), "end": str(result.request.end.date())},
        "period_returns": result.period_returns,
        "metrics": result.metrics,
        "warnings": result.warnings,
        "artifacts": result.artifacts,
    }
    print(json.dumps(payload, indent=2, default=str))
    return 0
