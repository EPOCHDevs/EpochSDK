from datetime import date, datetime

import pytest
from stratifyx import DatePeriodConfig

from epoch_sdk import RunParameters, date_range


@pytest.mark.parametrize(
    "arguments,expected",
    [
        ({"preset": "last year", "as_of": "2026-10-19"}, ("2025-01-01", "2025-12-31")),
        ({"preset": "last month", "as_of": "2026-01-01"}, ("2025-12-01", "2025-12-31")),
        ({"preset": "last month", "as_of": "2024-03-31"}, ("2024-02-01", "2024-02-29")),
        ({"preset": "year to date", "as_of": "2026-10-16"}, ("2026-01-01", "2026-10-16")),
        ({"preset": "month to date", "as_of": "2026-10-16"}, ("2026-10-01", "2026-10-16")),
        ({"years": 1, "as_of": "2024-02-29"}, ("2023-02-28", "2024-02-29")),
        ({"months": 1, "as_of": "2024-03-31"}, ("2024-02-29", "2024-03-31")),
        ({"months": 15, "as_of": "2026-01-31"}, ("2024-10-31", "2026-01-31")),
        ({"days": 1, "as_of": "2024-03-01"}, ("2024-02-29", "2024-03-01")),
        ({"start": date(2025, 1, 1), "end": "2025-01-01"}, ("2025-01-01", "2025-01-01")),
    ],
)
def test_convenience_ranges_are_native_closed_explicit_dates(arguments, expected):
    period = date_range(**arguments)
    assert isinstance(period, DatePeriodConfig)
    assert RunParameters(period=period).to_wire() == {
        "period": {"start": expected[0], "end": expected[1]}
    }


@pytest.mark.parametrize(
    "arguments",
    [
        {},
        {"preset": "yesterday"},
        {"preset": "last month", "start": "2026-01-01"},
        {"preset": "last year", "months": 1},
        {"months": 1, "days": 30},
        {"months": True},
        {"months": 1.5},
        {"months": "1"},
        {"days": 0},
        {"years": -1},
        {"years": 9999, "as_of": "2026-01-01"},
        {"start": "2025-02-29", "end": "2025-03-01"},
        {"start": "2026-10-20", "end": "2026-10-19"},
        {"start": "20261001", "end": "2026-10-19"},
        {"start": "2026-10-01", "as_of": "2026-10-19"},
        {"preset": "last month", "end": "2026-10-19"},
        {"days": 1, "as_of": datetime(2026, 10, 19)},
    ],
)
def test_ambiguous_or_invalid_ranges_fail_before_any_request(arguments):
    with pytest.raises((ValueError, TypeError)):
        date_range(**arguments)
