"""Project reviewed Backend Files/Space and EpochAI document APIs into the shared contract.

The sources are native openapi_generator output and EpochAI's source-owned
tools/export_document_contract.py output. This creates no new gateway/server.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREFIX = "#/components/schemas/"


def project(contract: dict, backend: dict, ai: dict) -> dict:
    result = json.loads(json.dumps(contract))
    previous = result.get("x-epoch-document-operations", {})
    for path in previous.get("paths", []):
        result["paths"].pop(path, None)
    for name in previous.get("schemas", []):
        result["components"]["schemas"].pop(name, None)
    added_paths, added_schemas = [], []
    for source, prefix, owner in ((backend, "NativeResource_", "EpochBackend"), (ai, "EpochDocument_", "EpochAI")):
        selected: dict[str, object] = {}

        def rewrite(node):
            if isinstance(node, str) and node.startswith(PREFIX):
                name = node.removeprefix(PREFIX)
                if name not in selected:
                    selected[name] = None
                    selected[name] = rewrite(source["components"]["schemas"][name])
                return PREFIX + prefix + name
            if isinstance(node, dict):
                return {key: rewrite(value) for key, value in node.items()}
            if isinstance(node, list):
                return [rewrite(value) for value in node]
            return node

        for path, methods in source["paths"].items():
            if owner == "EpochBackend" and not (path.startswith("/api/v1/files") or path.startswith("/api/v1/space")):
                continue
            if path in result["paths"]:
                raise ValueError(f"A document projection cannot replace an unrelated path: {path}")
            projected = rewrite(methods)
            for operation in projected.values():
                operation["security"] = [{"BearerAuth": []}]
                operation["description"] = f"Existing {owner} API; use its configured service origin. No document processing starts through metadata/content/search reads."
                operation["servers"] = source.get("servers", [{"url": "/", "description": f"Configured {owner} origin"}])
            result["paths"][path] = projected
            added_paths.append(path)
        for name, value in selected.items():
            key = prefix + name
            result["components"]["schemas"][key] = value
            added_schemas.append(key)
    result["x-epoch-document-operations"] = {"paths": sorted(added_paths), "schemas": sorted(added_schemas),
        "backend_sha256": hashlib.sha256(json.dumps(backend, sort_keys=True).encode()).hexdigest(),
        "epochai_sha256": hashlib.sha256(json.dumps(ai, sort_keys=True).encode()).hexdigest()}
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend-openapi", type=Path, required=True)
    parser.add_argument("--epochai-openapi", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    path = ROOT / "contracts/openapi.json"
    current = json.loads(path.read_text())
    expected = project(current, json.loads(args.backend_openapi.read_text()), json.loads(args.epochai_openapi.read_text()))
    if args.check:
        if current != expected:
            raise SystemExit("Document integration contract differs from its reviewed service sources")
    else:
        path.write_text(json.dumps(expected, indent=2, sort_keys=True) + "\n")
