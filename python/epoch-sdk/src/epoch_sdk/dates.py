"""Resolve convenient date ranges into the existing native execution type."""

from __future__ import annotations

import calendar
from datetime import date, datetime, timedelta
from typing import Literal

from stratifyx import DatePeriodConfig

type DateInput = date | str


def _date(value: DateInput) -> date:
    if isinstance(value, datetime):
        raise TypeError("Use a calendar date, without a time or time zone")
    if isinstance(value, date):
        return value
    parsed = date.fromisoformat(value)
    if parsed.isoformat() != value:
        raise ValueError("Use an ISO calendar date: YYYY-MM-DD")
    return parsed


def date_range(
    preset: Literal["last year", "last month", "year to date", "month to date"] | None = None,
    *,
    start: DateInput | None = None,
    end: DateInput | None = None,
    as_of: DateInput | None = None,
    years: int | None = None,
    months: int | None = None,
    days: int | None = None,
) -> DatePeriodConfig:
    """Return explicit inclusive calendar dates as a native DatePeriodConfig.

    ``last year`` and ``last month`` mean the previous *complete calendar*
    period. ``years=1``, ``months=1`` or ``days=30`` mean a rolling lookback,
    matching EpochAI's LastN period semantics. Month/year shifts clamp to the
    destination month's last day. These are calendar days, not trading sessions.

    The local calendar date is used only when as_of/end is omitted. For shared
    demos or reproducible requests, pin as_of and show the resolved dates before
    submission. Reconnect with those same dates and the same operation ID.
    """
    relative = [("years", years), ("months", months), ("days", days)]
    chosen = [(name, value) for name, value in relative if value is not None]
    if sum((preset is not None, start is not None, bool(chosen))) != 1:
        raise ValueError("Choose an explicit start, one calendar preset, or one lookback")
    if len(chosen) > 1:
        raise ValueError("Choose only one of years, months or days")
    if end is not None and start is None:
        raise ValueError("Use as_of to anchor a calendar preset or rolling lookback")
    if start is not None and as_of is not None:
        raise ValueError("Use end with an explicit start, not as_of")
    anchor = _date(as_of) if as_of is not None else date.today()
    if start is not None:
        first = _date(start)
        last = _date(end) if end is not None else anchor
    elif preset is not None:
        last = anchor
        if preset == "last year":
            first, last = date(anchor.year - 1, 1, 1), date(anchor.year - 1, 12, 31)
        elif preset == "last month":
            last = anchor.replace(day=1) - timedelta(days=1)
            first = last.replace(day=1)
        elif preset == "year to date":
            first = anchor.replace(month=1, day=1)
        elif preset == "month to date":
            first = anchor.replace(day=1)
        else:
            raise ValueError(f"Unknown calendar preset: {preset!r}")
    else:
        name, count = chosen[0]
        if type(count) is not int or count <= 0:
            raise ValueError("A lookback must be a positive integer")
        last = anchor
        if name == "days":
            first = anchor - timedelta(days=count)
        else:
            shift = count * 12 if name == "years" else count
            absolute_month = anchor.year * 12 + anchor.month - 1 - shift
            year, month_zero = divmod(absolute_month, 12)
            month = month_zero + 1
            if not 1 <= year <= 9999:
                raise ValueError("The lookback exceeds the supported calendar")
            first = date(year, month, min(anchor.day, calendar.monthrange(year, month)[1]))
    if first > last:
        raise ValueError("The start date must not follow the end date")
    return DatePeriodConfig(start=first, end=last)
