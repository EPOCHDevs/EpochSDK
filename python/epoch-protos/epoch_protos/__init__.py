"""
EpochProtos - Protocol buffer definitions for Epoch dashboard widgets.

This package contains proto definitions for:
- Common types (Scalar, Array, enums)
- Chart definitions (Line, Bar, Pie, Scatter, etc.)
- Table definitions
- Tearsheet (dashboard) definitions
"""

__version__ = "2.0.9"

# Fix for protoc-generated files that use absolute imports (e.g., `import common_pb2`)
# We need to add this package's directory to sys.path so those imports resolve correctly
import sys as _sys
from pathlib import Path as _Path
_pkg_dir = str(_Path(__file__).parent)
if _pkg_dir not in _sys.path:
    _sys.path.insert(0, _pkg_dir)

# Import all proto modules
from .common_pb2 import *
from .chart_base_pb2 import *
from .table_def_pb2 import *

# Chart types
from .lines_chart_pb2 import *
from .area_chart_pb2 import *
from .bar_chart_pb2 import *
from .heatmap_chart_pb2 import *
from .histogram_chart_pb2 import *
from .boxplot_chart_pb2 import *
from .xrange_chart_pb2 import *
from .pie_chart_pb2 import *
from .scatter_chart_pb2 import *
from .waterfall_chart_pb2 import *
from .spline_chart_pb2 import *
from .bubble_chart_pb2 import *
from .treemap_chart_pb2 import *
from .sankey_chart_pb2 import *
from .arearange_chart_pb2 import *
from .gauge_chart_pb2 import *
from .bullet_chart_pb2 import *
from .timeline_chart_pb2 import *
from .errorbar_chart_pb2 import *
from .bellcurve_chart_pb2 import *

# Union and top-level
from .chart_union_pb2 import *
from .chart_def_pb2 import *
from .tearsheet_pb2 import *

# Converters
from .converters import tearsheet_to_dict, full_tearsheet_to_dict, cards_to_compact_list, format_cards_for_display
