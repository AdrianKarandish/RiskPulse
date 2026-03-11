from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

import pytest

from riskpulse.cli.parser import parse_args


def test_parse_rolling():
    args = parse_args(["--ticker", "AAPL", "--rolling-days", "10"])
    assert args.ticker == "AAPL"
    assert args.rolling_days == 10


def test_parse_custom():
    args = parse_args(["--ticker", "MSFT", "--start-date", "2024-01-01", "--end-date", "2024-02-01"])
    assert args.start_date.year == 2024


def test_invalid_ticker():
    with pytest.raises(ValueError):
        parse_args(["--ticker", "TOOLONG", "--rolling-days", "10"])


def test_missing_end_date_for_custom_range():
    with pytest.raises(ValueError, match="--end-date is required"):
        parse_args(["--ticker", "AAPL", "--start-date", "2024-01-01"])


def test_end_date_disallowed_with_rolling_days():
    with pytest.raises(ValueError, match="--end-date cannot be used"):
        parse_args(["--ticker", "AAPL", "--rolling-days", "10", "--end-date", "2024-01-31"])


def test_future_date_rejected():
    future = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
    with pytest.raises(ValueError, match="future"):
        parse_args(["--ticker", "AAPL", "--start-date", "2024-01-01", "--end-date", future])


def test_output_dir_must_be_directory(tmp_path: Path):
    output_file = tmp_path / "not_a_dir"
    output_file.write_text("x", encoding="utf-8")
    with pytest.raises(ValueError, match="directory"):
        parse_args(
            [
                "--ticker",
                "AAPL",
                "--rolling-days",
                "10",
                "--output-dir",
                str(output_file),
            ]
        )
