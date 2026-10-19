"""Project/check session events, reusing existing workflow and response models."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python/epoch-sdk/src"))

from epoch_sdk.session import SessionEvent
from pydantic import TypeAdapter


def project() -> dict:
    schema = TypeAdapter(SessionEvent).json_schema()
    external = {name: "research-workflow.schema.json#/$defs/" + name
                for name in ("ResearchCompleted", "NeedsInput", "WorkflowHandle", "JsonValue")}

    def rewrite(node):
        if isinstance(node, dict):
            return {key: external.get(value.removeprefix("#/$defs/"), value)
                    if key == "$ref" and isinstance(value, str) else rewrite(value)
                    for key, value in node.items()}
        if isinstance(node, list):
            return [rewrite(value) for value in node]
        return node

    schema = rewrite(schema)
    definitions = schema.pop("$defs", {})
    selected = {}

    def visit(node):
        if isinstance(node, dict):
            ref = node.get("$ref", "")
            if ref.startswith("#/$defs/"):
                name = ref.removeprefix("#/$defs/")
                if name not in selected:
                    selected[name] = definitions[name]
                    visit(definitions[name])
            for value in node.values():
                visit(value)
        elif isinstance(node, list):
            for value in node:
                visit(value)

    visit(schema)
    return {"$schema": "https://json-schema.org/draft/2020-12/schema", **schema, "$defs": selected}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    path = ROOT / "contracts/research-session.schema.json"
    encoded = json.dumps(project(), indent=2, sort_keys=True) + "\n"
    if args.check:
        if not path.exists() or path.read_text() != encoded:
            raise SystemExit("Session event contract differs from the SDK models")
    else:
        path.write_text(encoded)
    print("Session event schema agrees with the SDK models")
