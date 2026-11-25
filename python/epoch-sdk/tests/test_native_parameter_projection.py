from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


def test_owner_projection_keeps_nested_native_nullability_and_exact_bounds(tmp_path: Path) -> None:
    source = Path(__file__).resolve().parents[3] / "tools/sync_native_parameters.py"
    spec = importlib.util.spec_from_file_location("native_parameter_projection", source)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    nested = {"type": ["integer", "null"], "maximum": 2**63 - 1, "minimum": -(2**63)}
    schemas = {
        "DatePeriodConfig": {"type": ["object", "null"], "properties": {"retained": nested}},
        "ExecutionOptions": {"type": "object", "properties": {"cash": nested}},
    }
    path = tmp_path / "native.json"
    path.write_text(json.dumps({"components": {"schemas": schemas}}))
    projected = module.project(path)["schemas"]
    assert projected["DatePeriodConfig"]["type"] == "object"
    assert projected["DatePeriodConfig"]["properties"]["retained"] == nested
    assert projected["ExecutionOptions"] == schemas["ExecutionOptions"]

    schemas["DatePeriodConfig"]["type"] = ["object", "number"]
    path.write_text(json.dumps({"components": {"schemas": schemas}}))
    with pytest.raises(ValueError, match="Unexpected native parameter owner type"):
        module.project(path)
