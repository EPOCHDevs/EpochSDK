"""
TearSheet Summary Formatter.

Provides compact, readable summaries of dashboard data for agent context.
Designed to stay small even with many assets/categories.
"""
from typing import Dict, Any, List, Optional
from . import tearsheet_pb2, common_pb2


def format_tearsheet_summary(
    tearsheet: tearsheet_pb2.TearSheet,
    category: str = "ALL",
    max_cards: int = 20
) -> str:
    """
    Format a TearSheet into a compact summary.

    Args:
        tearsheet: Proto TearSheet to summarize
        category: Category name (e.g., "ALL", "AAPL-Stocks")
        max_cards: Max cards to show before truncating (default 20)

    Returns:
        Formatted string summary
    """
    lines = [f"## Category: {category}", ""]

    # Cards section
    lines.extend(_format_cards_section(tearsheet, max_cards))
    lines.append("")

    # Tables section
    lines.extend(_format_tables_section(tearsheet))
    lines.append("")

    # Charts section
    lines.extend(_format_charts_section(tearsheet))

    return "\n".join(lines)


def format_full_tearsheet_summary(
    full_tearsheet: tearsheet_pb2.FullTearSheet,
    max_cards_for_all: int = 20
) -> str:
    """
    Format a FullTearSheet (all categories) into a compact summary.

    Shows full detail for "ALL" category, summaries for per-asset categories.
    """
    lines = ["# Dashboard Summary", ""]

    categories = dict(full_tearsheet.categories)
    all_tearsheet = categories.pop("ALL", None)
    asset_categories = sorted(categories.keys())

    # ALL category - full detail
    if all_tearsheet:
        lines.append(format_tearsheet_summary(all_tearsheet, "ALL", max_cards_for_all))
        lines.append("")
        lines.append("---")
        lines.append("")

    # Per-asset categories - just summary
    if asset_categories:
        lines.append(f"## Per-Asset Categories ({len(asset_categories)} assets)")
        lines.append("")

        # Show first few as samples
        sample_count = min(3, len(asset_categories))
        for cat_name in asset_categories[:sample_count]:
            ts = categories[cat_name]
            card_count = sum(len(card.data) for card in ts.cards.cards)
            table_count = len(ts.tables.tables)
            chart_count = len(ts.charts.charts)
            lines.append(f"- **{cat_name}**: {card_count} metrics, {table_count} tables, {chart_count} charts")

        if len(asset_categories) > sample_count:
            remaining = len(asset_categories) - sample_count
            lines.append(f"- ... and {remaining} more assets")

        lines.append("")
        lines.append(f"**All asset categories**: {', '.join(asset_categories)}")

    return "\n".join(lines)


def _format_cards_section(tearsheet: tearsheet_pb2.TearSheet, max_cards: int) -> List[str]:
    """Format cards section."""
    lines = ["### Cards"]

    if not tearsheet.cards or not tearsheet.cards.cards:
        lines.append("No cards available")
        return lines

    # Collect all card data
    all_metrics = []
    categories = set()

    for card in tearsheet.cards.cards:
        categories.add(card.category) if card.category else None
        for item in card.data:
            val = _extract_scalar_value(item.value)
            vtype = _get_value_type(item.value)
            all_metrics.append({
                "title": item.title,
                "value": val,
                "type": vtype,
                "category": card.category
            })

    total_count = len(all_metrics)
    categories.discard("")  # Remove empty category

    # Show metrics
    display_count = min(max_cards, total_count)
    for m in all_metrics[:display_count]:
        formatted_val = _format_value(m["value"], m["type"])
        lines.append(f"- {m['title']}: {formatted_val}")

    if total_count > display_count:
        lines.append(f"- ... ({total_count - display_count} more metrics)")

    # Summary line
    lines.append("")
    lines.append(f"**Total**: {total_count} metrics")
    if categories:
        lines.append(f"**Categories**: {', '.join(sorted(categories))}")

    return lines


def _format_tables_section(tearsheet: tearsheet_pb2.TearSheet) -> List[str]:
    """Format tables section."""
    lines = ["### Tables"]

    if not tearsheet.tables or not tearsheet.tables.tables:
        lines.append("No tables available")
        return lines

    lines.append("")
    lines.append("| Title | Rows | Cols | Category |")
    lines.append("|-------|------|------|----------|")

    for table in tearsheet.tables.tables:
        row_count = len(table.data.rows) if table.data else 0
        col_count = len(table.columns)
        cat = table.category or "-"
        lines.append(f"| {table.title} | {row_count} | {col_count} | {cat} |")

    lines.append("")
    lines.append(f"**Total**: {len(tearsheet.tables.tables)} tables")

    return lines


def _format_charts_section(tearsheet: tearsheet_pb2.TearSheet) -> List[str]:
    """Format charts section."""
    lines = ["### Charts"]

    if not tearsheet.charts or not tearsheet.charts.charts:
        lines.append("No charts available")
        return lines

    lines.append("")
    lines.append("| Title | Type | Category | Data Points |")
    lines.append("|-------|------|----------|-------------|")

    for chart in tearsheet.charts.charts:
        chart_type = chart.WhichOneof("chart_type")
        if not chart_type:
            continue

        chart_data = getattr(chart, chart_type)
        chart_def = chart_data.chart_def
        title = chart_def.title or chart_def.id or "-"
        cat = chart_def.category or "-"

        # Get data point count based on chart type
        data_points = _get_chart_data_points(chart_data, chart_type)
        type_display = chart_type.replace("_def", "").replace("_", " ").title()

        lines.append(f"| {title} | {type_display} | {cat} | {data_points} |")

    lines.append("")
    lines.append(f"**Total**: {len(tearsheet.charts.charts)} charts")

    return lines


def _extract_scalar_value(scalar: common_pb2.Scalar):
    """Extract value from Scalar proto."""
    if scalar.HasField('percent_value'):
        return scalar.percent_value
    elif scalar.HasField('decimal_value'):
        return scalar.decimal_value
    elif scalar.HasField('integer_value'):
        return scalar.integer_value
    elif scalar.HasField('timestamp_ms'):
        return scalar.timestamp_ms
    elif scalar.HasField('string_value'):
        return scalar.string_value
    elif scalar.HasField('boolean_value'):
        return scalar.boolean_value
    elif scalar.HasField('date_value'):
        return scalar.date_value
    elif scalar.HasField('day_duration'):
        return scalar.day_duration
    elif scalar.HasField('monetary_value'):
        return scalar.monetary_value
    elif scalar.HasField('duration_ms'):
        return scalar.duration_ms
    return None


def _get_value_type(scalar: common_pb2.Scalar) -> str:
    """Get type string for Scalar value."""
    if scalar.HasField('percent_value'):
        return 'pct'
    elif scalar.HasField('decimal_value'):
        return 'dec'
    elif scalar.HasField('integer_value'):
        return 'int'
    elif scalar.HasField('timestamp_ms'):
        return 'ts'
    elif scalar.HasField('string_value'):
        return 'str'
    elif scalar.HasField('boolean_value'):
        return 'bool'
    elif scalar.HasField('date_value'):
        return 'date'
    elif scalar.HasField('day_duration'):
        return 'days'
    elif scalar.HasField('monetary_value'):
        return 'money'
    elif scalar.HasField('duration_ms'):
        return 'dur'
    return 'none'


def _format_value(value, vtype: str) -> str:
    """Format value for display."""
    if value is None:
        return "N/A"
    elif vtype == 'pct':
        return f"{value:.2f}%"
    elif vtype == 'dec':
        return f"{value:.4f}"
    elif vtype == 'int':
        return f"{value:,}" if isinstance(value, int) else str(value)
    elif vtype == 'ts':
        # Convert ms timestamp to date string
        try:
            from datetime import datetime
            dt = datetime.fromtimestamp(value / 1000)
            return dt.strftime("%Y-%m-%d")
        except:
            return str(value)
    elif vtype == 'date':
        # date_value is also ms timestamp
        try:
            from datetime import datetime
            dt = datetime.fromtimestamp(value / 1000)
            return dt.strftime("%Y-%m-%d")
        except:
            return str(value)
    elif vtype == 'days':
        return f"{value} days"
    elif vtype == 'money':
        return f"${value:,.2f}"
    elif vtype == 'dur':
        # duration in ms
        secs = value / 1000
        if secs < 60:
            return f"{secs:.1f}s"
        elif secs < 3600:
            return f"{secs/60:.1f}m"
        else:
            return f"{secs/3600:.1f}h"
    elif vtype == 'bool':
        return "Yes" if value else "No"
    else:
        return str(value)


def _get_chart_data_points(chart_data, chart_type: str) -> str:
    """Get data point count for a chart."""
    try:
        if chart_type == "lines_def":
            if chart_data.lines:
                total = sum(len(line.data) for line in chart_data.lines)
                return f"{total} ({len(chart_data.lines)} series)"
            return "0"
        elif chart_type == "bar_def":
            if chart_data.data:
                return str(len(chart_data.data))
            return "0"
        elif chart_type == "pie_def":
            if chart_data.data:
                return str(len(chart_data.data))
            return "0"
        elif chart_type == "heat_map_def":
            if chart_data.data:
                return f"{len(chart_data.data)}x{len(chart_data.data[0].values) if chart_data.data else 0}"
            return "0"
        elif chart_type == "histogram_def":
            if chart_data.data:
                return str(len(chart_data.data))
            return "0"
        elif chart_type == "box_plot_def":
            if chart_data.data:
                return str(len(chart_data.data))
            return "0"
        elif chart_type == "x_range_def":
            if chart_data.data:
                return str(len(chart_data.data))
            return "0"
        elif chart_type == "area_def":
            if chart_data.areas:
                total = sum(len(area.data) for area in chart_data.areas)
                return f"{total} ({len(chart_data.areas)} areas)"
            return "0"
        elif chart_type == "numeric_lines_def":
            if chart_data.lines:
                total = sum(len(line.data) for line in chart_data.lines)
                return f"{total} ({len(chart_data.lines)} series)"
            return "0"
        else:
            return "-"
    except Exception:
        return "-"
