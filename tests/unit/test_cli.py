from __future__ import annotations

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
