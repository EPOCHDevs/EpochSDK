"""Validate local notebook requests against the shared contract, without services."""

from __future__ import annotations

import ast
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT / "examples/notebooks"
CASES = NOTEBOOKS / "cases"


def main() -> None:
    document = json.loads((ROOT / "contracts/openapi.json").read_text())
    validator = Draft202012Validator(
        {
            "$ref": "#/components/schemas/RunRequest",
            "components": document["components"],
        },
        format_checker=FormatChecker(),
    )
    entries = json.loads((CASES / "index.json").read_text())["cases"]
    seen = set()
    for entry in entries:
        key = entry["id"]
        assert key not in seen and entry["file"] == key + ".json", key
        assert entry["kind"] in {"research", "output_variant", "clarification"}, key
        if entry["kind"] == "output_variant":
            assert entry["source_case"] in seen, f"{key}: list the source case first"
        request = json.loads((CASES / entry["file"]).read_text())
        validator.validate(request)
        assert not {"study_id", "source_execution_id"} & request.keys(), key
        assert not request.get("auto_ingest", False), key
        outputs = request["outputs"]
        assert len({output["name"] for output in outputs}) == len(outputs), key
        for output in outputs:
            if output["type"] == "json":
                Draft202012Validator.check_schema(output["schema"])
            elif output["type"] == "table":
                assert all(column.get("description") for column in output["schema"]), (
                    key
                )
        seen.add(key)
    assert {path.name for path in CASES.glob("*.json")} == {
        "index.json",
        *(entry["file"] for entry in entries),
    }, "Every top-level request belongs in the case catalogue."
    cells = 0
    for path in sorted(NOTEBOOKS.rglob("*.ipynb")):
        notebook = json.loads(path.read_text())
        for cell in notebook["cells"]:
            if cell["cell_type"] == "code":
                assert cell["execution_count"] is None and not cell["outputs"], (
                    path.name
                )
                compile(
                    "".join(cell["source"]),
                    str(path),
                    "exec",
                    flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT,
                )
                cells += 1
    print(
        f"Validated {len(entries)} local requests and {cells} unexecuted notebook code cells."
    )
    print(
        "Offline validation only; no vendor/model calls or market-data results were tested."
    )


if __name__ == "__main__":
    main()
