from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path


TICKER_PATTERN = re.compile(r"^[A-Za-z0-9.-]{1,5}$")


def validate_ticker(value: str) -> str:
    ticker = value.strip().upper()
    if not TICKER_PATTERN.fullmatch(ticker):
        raise ValueError("Ticker must be 1-5 characters using letters, numbers, dots, or dashes.")
    return ticker


def validate_date(value: str) -> datetime:
    try:
        parsed = datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError("Date must use YYYY-MM-DD format.") from exc
    if parsed.date() > datetime.now().date():
        raise ValueError("Date cannot be in the future.")
    return parsed


def validate_rolling_days(value: int) -> int:
    if value < 5 or value > 252:
        raise ValueError("Rolling window must be between 5 and 252 business days.")
    return value


def validate_date_range(start: datetime, end: datetime) -> None:
    if start >= end:
        raise ValueError("Start date must be earlier than end date.")


def validate_output_dir(path: Path) -> Path:
    if path.exists() and not path.is_dir():
        raise ValueError("Output path must be a directory.")
    return path
