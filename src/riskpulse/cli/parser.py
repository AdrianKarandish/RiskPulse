from __future__ import annotations

import argparse
from pathlib import Path

from riskpulse.cli.validators import (
    validate_date,
    validate_date_range,
    validate_rolling_days,
    validate_ticker,
)


class ValidatingArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise ValueError(message)


def build_parser() -> argparse.ArgumentParser:
    parser = ValidatingArgumentParser(
        prog="riskpulse",
        description="Calculate stock risk metrics and benchmark comparisons.",
    )
    parser.add_argument("--ticker", required=True, help="Ticker symbol to analyze.")

    period_group = parser.add_mutually_exclusive_group(required=True)
    period_group.add_argument(
        "--rolling-days",
        type=int,
        help="Rolling lookback in business days (5-252).",
    )
    period_group.add_argument(
        "--start-date",
        help="Start date for custom analysis period in YYYY-MM-DD format.",
    )

    parser.add_argument(
        "--end-date",
        help="End date for custom analysis period in YYYY-MM-DD format. Required with --start-date.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs"),
        help="Directory for CSVs and charts.",
    )
    parser.add_argument(
        "--verbose",
        action="count",
        default=0,
        help="Increase logging verbosity.",
    )
    return parser


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = build_parser()
    args = parser.parse_args(argv)

    args.ticker = validate_ticker(args.ticker)
    if args.rolling_days is not None:
        args.rolling_days = validate_rolling_days(args.rolling_days)
        if args.end_date is not None:
            raise ValueError("--end-date cannot be used with --rolling-days.")
    else:
        if args.end_date is None:
            raise ValueError("--end-date is required when using --start-date.")
        args.start_date = validate_date(args.start_date)
        args.end_date = validate_date(args.end_date)
        validate_date_range(args.start_date, args.end_date)

    return args
