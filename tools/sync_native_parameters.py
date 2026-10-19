"""Sync packaged parameter schemas from the shared contract, optionally refreshing from Backend."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHARED = ROOT / "contracts/native-parameters.json"
PACKAGED = ROOT / "python/epoch-sdk/src/epoch_sdk/data/native-parameters.json"


def project(path: Path) -> dict:
    schemas = json.loads(path.read_text())["components"]["schemas"]
    selected = {}

    def add(name: str) -> None:
        if name in selected:
            return
        selected[name] = schemas[name]

        def refs(node: object) -> None:
            if isinstance(node, dict):
                for key, value in node.items():
                    if key == "$ref":
                        assert isinstance(value, str) and value.startswith("#/components/schemas/")
                        add(value.removeprefix("#/components/schemas/"))
                    else:
                        refs(value)
            elif isinstance(node, list):
                for value in node:
                    refs(value)

        refs(schemas[name])

    add("DatePeriodConfig")
    add("ExecutionOptions")
    result = json.loads(json.dumps(selected).replace("#/components/schemas/", "#/$defs/"))
    return {
        "source": "stratifyx_openapi.json#/components/schemas",
        "sha256": hashlib.sha256(json.dumps(result, sort_keys=True).encode()).hexdigest(),
        "schemas": result,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend-openapi", type=Path, help="Reviewed source-owned native API export")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = project(args.backend_openapi) if args.backend_openapi else json.loads(SHARED.read_text())
    if args.check:
        if json.loads(SHARED.read_text()) != expected or json.loads(PACKAGED.read_text()) != expected:
            raise SystemExit("Native parameter snapshots differ; review and sync them")
        print("Shared and packaged native parameters agree")
    else:
        if args.backend_openapi:
            SHARED.write_text(json.dumps(expected, indent=2, sort_keys=True) + "\n")
        PACKAGED.write_text(json.dumps(expected, indent=2, sort_keys=True) + "\n")
