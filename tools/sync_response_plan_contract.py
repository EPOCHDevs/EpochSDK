"""Project/check replay-plan schemas while reusing existing shared contracts."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python/epoch-sdk/src"))

from epoch_sdk.response_plans import (
    ResponsePlanDefinition,
    ResponsePlanDraft,
    SavedResponsePlan,
)
from epoch_sdk.responses import ResponsePlanReference

MODELS = [
    ("response-plan-reference.schema.json", ResponsePlanReference),
    ("response-plan-draft.schema.json", ResponsePlanDraft),
    ("response-plan-definition.schema.json", ResponsePlanDefinition),
    ("response-plan.schema.json", SavedResponsePlan),
]


def project(model, external):
    schema = model.model_json_schema()

    def rewrite(node):
        if isinstance(node, str) and node.startswith("#/$defs/"):
            return external.get(node.removeprefix("#/$defs/"), node)
        if isinstance(node, dict):
            return {key: rewrite(value) for key, value in node.items()}
        if isinstance(node, list):
            return [rewrite(value) for value in node]
        return node

    schema = rewrite(schema)
    definitions = schema.pop("$defs", {})
    selected = {}

    def visit(node):
        if isinstance(node, dict):
            reference = node.get("$ref", "")
            if reference.startswith("#/$defs/"):
                name = reference.removeprefix("#/$defs/")
                if name not in selected:
                    selected[name] = definitions[name]
                    visit(definitions[name])
            for value in node.values(): visit(value)
        elif isinstance(node, list):
            for value in node: visit(value)

    visit(schema)
    return {"$schema": "https://json-schema.org/draft/2020-12/schema", **schema, "$defs": selected}


def schemas():
    core = {name: "openapi.json#/components/schemas/" + (
        "JsonSchema" if name == "JsonSchemaDocument" else name)
        for name in ["RunParameters", "DomainError", "Column", "TableOutputRequest",
                     "JsonOutputRequest", "TextOutputRequest", "JsonSchemaDocument"]}
    result = {}
    for filename, model in MODELS:
        result[filename] = project(model, core)
        core[model.__name__] = filename
        if model is ResponsePlanDraft:
            for name in result[filename]["$defs"]:
                core[name] = filename + "#/$defs/" + name
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    for filename, schema in schemas().items():
        path = ROOT / "contracts" / filename
        encoded = json.dumps(schema, indent=2, sort_keys=True) + "\n"
        if args.check:
            if not path.exists() or path.read_text() != encoded:
                raise SystemExit(f"{filename} differs from its source-owned model")
        else: path.write_text(encoded)
    print("Replay-plan schemas agree with the source-owned models")
