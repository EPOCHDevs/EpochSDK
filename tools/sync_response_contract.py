"""Project the shared answer wire contract from the source-owned Python model."""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python/epoch-sdk/src"))
from epoch_sdk.responses import ResponseTablePage, SavedResearchResponse


def project(model=SavedResearchResponse):
    schema = model.model_json_schema()
    shared = {
        "Column",
        "TableOutputRequest",
        "JsonOutputRequest",
        "TextOutputRequest",
        "JsonSchemaDocument",
    }

    def rewrite(value):
        if isinstance(value, list):
            return [rewrite(item) for item in value]
        if isinstance(value, dict):
            result = {}
            for key, item in value.items():
                if key == "$ref" and item.removeprefix("#/$defs/") in shared:
                    name = item.removeprefix("#/$defs/")
                    result[key] = "openapi.json#/components/schemas/" + (
                        "JsonSchema" if name == "JsonSchemaDocument" else name
                    )
                else:
                    result[key] = rewrite(item)
            return result
        return value

    schema = rewrite(schema)
    schema["$defs"] = {k: v for k, v in schema["$defs"].items() if k not in shared}
    return {"$schema": "https://json-schema.org/draft/2020-12/schema", **schema}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    for filename, model in (
        ("research-response.schema.json", SavedResearchResponse),
        ("research-response-table-page.schema.json", ResponseTablePage),
    ):
        path = ROOT / "contracts" / filename
        text = json.dumps(project(model), indent=2, sort_keys=True) + "\n"
        if args.check:
            if path.read_text() != text:
                raise SystemExit(f"{filename} differs from the source-owned model")
        else:
            path.write_text(text)
    print("Saved answer contract agrees with the model")
