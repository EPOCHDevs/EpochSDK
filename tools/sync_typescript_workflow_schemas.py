"""Project the source-owned workflow schemas into the browser package, without new contracts."""
import argparse
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "typescript/epoch-sdk/schemas.generated.json"
BASE = "https://schemas.epoch.invalid/sdk/"


def references(value):
    if isinstance(value, dict):
        if "$ref" in value:
            yield value["$ref"]
        for child in value.values():
            yield from references(child)
    elif isinstance(value, list):
        for child in value:
            yield from references(child)


def generate():
    inputs = {name: (ROOT / "contracts" / name).read_bytes() for name in
              ["openapi.json", "research-response.schema.json"]}
    api = json.loads(inputs["openapi.json"])
    response = json.loads(inputs["research-response.schema.json"])
    pending = ["RunRequest", "RunParameters"]
    pending += [ref.split("/schemas/")[1] for ref in references(response)
                if ref.startswith("openapi.json#/components/schemas/")]
    selected = {}
    while pending:
        name = pending.pop()
        if name in selected:
            continue
        selected[name] = api["components"]["schemas"][name]
        pending += [ref.rsplit("/", 1)[1] for ref in references(selected[name])
                    if ref.startswith("#/components/schemas/")]
    response = copy.deepcopy(response)
    response["$id"] = BASE + "research-response.schema.json"
    bundle = {
        "source_sha256": {k: hashlib.sha256(v).hexdigest() for k, v in inputs.items()},
        "request": {"$id": BASE + "openapi.json", "components": {"schemas": selected}},
        "response": response,
    }
    return json.dumps(bundle, indent=2, sort_keys=True) + "\n"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = generate()
    if args.check:
        if not DEST.exists() or DEST.read_text() != expected:
            raise SystemExit("Browser workflow schemas are stale; run tools/sync_typescript_workflow_schemas.py")
    else:
        DEST.parent.mkdir(parents=True, exist_ok=True)
        DEST.write_text(expected)
    print("TypeScript workflow schema projection is current")
