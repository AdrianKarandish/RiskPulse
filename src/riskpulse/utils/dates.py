from __future__ import annotations

from datetime import datetime, timedelta

from riskpulse.domain.models import PeriodSpec


def align_to_business_days(value: datetime) -> datetime:
    adjusted = value
    while adjusted.weekday() >= 5:
        adjusted -= timedelta(days=1)
    return adjusted.replace(hour=0, minute=0, second=0, microsecond=0)


def parse_period_input(
    rolling_days: int | None = None,
    start_date: str | datetime | None = None,
    end_date: str | datetime | None = None,
    now: datetime | None = None,
) -> PeriodSpec:
    reference_now = align_to_business_days(now or datetime.now())
    if rolling_days is not None:
        end = reference_now
        start = end - timedelta(days=int(rolling_days * 1.6))
        business_days = 0
        cursor = start
        while cursor <= end:
            if cursor.weekday() < 5:
                business_days += 1
            if business_days >= rolling_days:
                break
            cursor += timedelta(days=1)
        start = align_to_business_days(cursor)
        return PeriodSpec(start=start, end=end, label=f"{rolling_days}d", rolling_days=rolling_days)

    if isinstance(start_date, str):
        start = datetime.strptime(start_date, "%Y-%m-%d")
    else:
        start = start_date
    if isinstance(end_date, str):
        end = datetime.strptime(end_date, "%Y-%m-%d")
    else:
        end = end_date
    if start is None or end is None:
        raise ValueError("Either rolling_days or both start_date and end_date must be provided.")

    start = align_to_business_days(start)
    end = align_to_business_days(end)
    return PeriodSpec(start=start, end=end, label=f"{start.date()}_{end.date()}")


def calculate_extended_lookback(
    selected_period: PeriodSpec,
    metric_requirements: dict[str, int] | None = None,
) -> PeriodSpec:
    requirements = metric_requirements or {"max_drawdown_1y": 252}
    longest_requirement = max(requirements.values(), default=252)
    extra_days = int(longest_requirement * 1.6)
    extended_start = align_to_business_days(selected_period.start - timedelta(days=extra_days))
    return PeriodSpec(
        start=extended_start,
        end=selected_period.end,
        label=f"extended_{selected_period.label}",
        rolling_days=None,
    )
