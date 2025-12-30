"""
Proto to Dict Converters.

Uses google.protobuf.json_format for complete, correct conversion.
"""
from typing import Dict, Any, List, Tuple, Optional
from google.protobuf.json_format import MessageToDict

from . import tearsheet_pb2


def tearsheet_to_dict(tearsheet: tearsheet_pb2.TearSheet) -> Dict[str, Any]:
    """
    Convert TearSheet proto to dict format.

    Uses protobuf's built-in MessageToDict for complete conversion.
    preserving_proto_field_name=True keeps snake_case field names.
    """
    return MessageToDict(tearsheet, preserving_proto_field_name=True)


def full_tearsheet_to_dict(full_tearsheet: tearsheet_pb2.FullTearSheet) -> Dict[str, Dict[str, Any]]:
    """Convert FullTearSheet proto to dict mapping category -> tearsheet dict."""
    return MessageToDict(full_tearsheet, preserving_proto_field_name=True).get("categories", {})


def cards_to_compact_list(tearsheet: tearsheet_pb2.TearSheet) -> List[Tuple[str, Optional[float], str]]:
    """
    Convert cards to compact list format: [(title, value, type), ...]

    ~35 bytes per metric vs ~113 bytes in full dict format (3x smaller).
    At 10,000 metrics: ~350KB vs ~1.1MB

    Returns:
        List of (title, value, value_type) tuples.
        value_type is one of: 'pct', 'dec', 'int', 'ts', 'str', 'bool'
    """
    result = []
    for card in tearsheet.cards.cards:
        for item in card.data:
            val = item.value
            value = None
            vtype = 'none'

            if val.HasField('percent_value'):
                value = round(val.percent_value, 4)
                vtype = 'pct'
            elif val.HasField('decimal_value'):
                value = round(val.decimal_value, 4)
                vtype = 'dec'
            elif val.HasField('integer_value'):
                value = val.integer_value
                vtype = 'int'
            elif val.HasField('timestamp_ms'):
                value = val.timestamp_ms
                vtype = 'ts'
            elif val.HasField('string_value'):
                value = val.string_value
                vtype = 'str'
            elif val.HasField('boolean_value'):
                value = val.boolean_value
                vtype = 'bool'
            elif val.HasField('date_value'):
                value = val.date_value
                vtype = 'date'
            elif val.HasField('monetary_value'):
                value = round(val.monetary_value, 2)
                vtype = 'money'
            elif val.HasField('day_duration'):
                value = val.day_duration
                vtype = 'days'
            elif val.HasField('duration_ms'):
                value = val.duration_ms
                vtype = 'dur'

            result.append((item.title, value, vtype))

    return result


def format_cards_for_display(cards: List[Tuple[str, Optional[float], str]]) -> str:
    """
    Format compact cards list for agent display.

    Example output:
        Sharpe Ratio: 0.449
        Annual Return: 9.26%
        Max Drawdown: -35.42%
        Total Trades: 1234
    """
    lines = []
    for title, value, vtype in cards:
        if value is None:
            lines.append(f"{title}: N/A")
        elif vtype == 'pct':
            lines.append(f"{title}: {value}%")
        elif vtype == 'int':
            lines.append(f"{title}: {value:,}" if isinstance(value, int) else f"{title}: {value}")
        else:
            lines.append(f"{title}: {value}")

    return "\n".join(lines)
