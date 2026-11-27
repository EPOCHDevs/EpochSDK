"""Project native execution and Platform research operation APIs into the shared OpenAPI contract.

Native schema names are prefixed to keep historical illustrative /v1 models
separate. This is a projection of existing service routes, not a new gateway.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contracts/openapi.json"
PREFIX = "#/components/schemas/"


def project(source: Path, contract: dict) -> dict:
    native = json.loads(source.read_text())
    extension_examples = json.loads((ROOT / "contracts/execution-extension.examples.json").read_text())
    selected = {}

    def rewrite(node):
        if isinstance(node, str) and node.startswith(PREFIX):
            name = node.removeprefix(PREFIX)
            if name not in selected:
                selected[name] = None
                selected[name] = rewrite(native["components"]["schemas"][name])
            return PREFIX + "Native_" + name
        if isinstance(node, dict):
            # OpenAPI discriminator.mapping values are references as well;
            # preserving only $ref leaves generated union targets dangling.
            return {key: rewrite(value) for key, value in node.items()}
        if isinstance(node, list):
            return [rewrite(value) for value in node]
        return node

    paths = {
        path: rewrite(operations)
        for path, operations in native["paths"].items()
        if path.startswith("/api/v1/integration/execution-requests")
        or path == "/api/v1/studies/executions/{executionId}/inputs"
        or path == "/api/v1/studies/executions/{executionId}/acquisition-provenance"
        or path == "/api/v1/agents/threads/{threadId}/studies/definitions"
        or path == "/api/v1/research/responses/{responseId}"
        or path == "/api/v1/research/responses/{responseId}/acquisition-provenance"
        or path == "/api/v1/studies/executions/{executionId}/response-tables"
        or path == "/api/v1/contexts/publications/{publicationId}/presentation"
    }
    previous = contract.get("x-epoch-native-operations", {})
    for path in previous.get("paths", []):
        contract["paths"].pop(path, None)
    for name in previous.get("schemas", []):
        contract["components"]["schemas"].pop(name, None)
    for methods in paths.values():
        for operation in methods.values():
            operation["security"] = [{"BearerAuth": []}]
            operation["servers"] = native["servers"]
            operation["description"] = (
                "Existing EpochBackend native API. Use the configured Backend origin. "
                "The owning service validates the exact caller/source contract."
            )
            response = operation.get("responses", {}).get("200", {}).get("content", {}).get("application/json", {})
            response_ref = response.get("schema", {}).get("$ref")
            # Input catalogues, prepared facts and definition creation have
            # different native DTOs/statuses. Never attach an operation-record
            # example to their responses or invent a second creation protocol.
            if response_ref not in {
                PREFIX + "Native_SdkExecutionRecord"
            }:
                example = extension_examples.get(operation["operationId"], {})
                for container, name in (
                    (operation.get("requestBody", {}), "request"),
                    *[(body, "response") for code, body in operation.get("responses", {}).items()
                      if str(code).startswith("2")],
                ):
                    for media, content in container.get("content", {}).items():
                        if media == "application/json" and name in example:
                            content["examples"] = {"nativeExtension": {"value": example[name]}}
                continue
            operation["description"] += (
                " Readable operation IDs attach to the original accepted owner-scoped inputs; "
                "changed inputs conflict with HTTP 409. See docs/reconnect-operations.md."
            )
            execution_input = {
                "operation_id": "refresh-sp500-2025",
                "study_id": "11111111-1111-4111-8111-111111111111",
                "source_execution_id": "22222222-2222-4222-8222-222222222222",
                "parameters": {"period": {"start": "2025-01-01", "end": "2025-12-31"}},
            }
            execution_record = {
                "request_id": "req_" + "2" * 32,
                "execution_id": "33333333-3333-4333-8333-333333333333",
                "request": execution_input,
                "phase": "active",
                "created_at_ms": 1,
            }
            operation["responses"]["200"]["content"]["application/json"]["examples"] = {
                "acceptedOperation": {
                    "value": execution_record
                },
            }
            if "requestBody" in operation:
                request_example = execution_input
                operation["requestBody"]["content"]["application/json"]["examples"] = {
                    "acceptedInputs": {"value": request_example},
                }
    contract["paths"].update(paths)
    for name, schema in selected.items():
        contract["components"]["schemas"]["Native_" + name] = {
            **schema,
            "x-native-schema-name": name,
        }
    contract["x-epoch-native-operations"] = {
        "source": "EpochBackend/stratifyx_openapi.json",
        "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "paths": sorted(paths),
        "schemas": sorted("Native_" + name for name in selected),
    }
    platform_path = ROOT / "contracts/platform-research.openapi.json"
    platform = json.loads(platform_path.read_text())
    previous_platform = contract.get("x-epoch-platform-research-operations", {})
    for path in previous_platform.get("paths", []): contract["paths"].pop(path, None)
    for name in previous_platform.get("schemas", []): contract["components"]["schemas"].pop(name, None)
    def platform_refs(value):
        if isinstance(value, str) and value.startswith(PREFIX): return PREFIX + "Platform_" + value.removeprefix(PREFIX)
        if isinstance(value, dict): return {key: platform_refs(field) for key, field in value.items()}
        if isinstance(value, list): return [platform_refs(field) for field in value]
        return value
    platform_paths = platform_refs(platform["paths"])
    for methods in platform_paths.values():
        for operation in methods.values(): operation["security"] = [{"BearerAuth": []}]
    contract["paths"].update(platform_paths)
    platform_schemas = {"Platform_" + name: platform_refs(schema) for name, schema in platform["components"]["schemas"].items()}
    contract["components"]["schemas"].update(platform_schemas)
    contract["x-epoch-platform-research-operations"] = {"source": "EpochPlatform/contracts/research.openapi.json",
        "sha256": hashlib.sha256(platform_path.read_bytes()).hexdigest(), "paths": sorted(platform_paths), "schemas": sorted(platform_schemas)}
    contract["info"]["description"] = (
        "Shared language-neutral Epoch contracts. Platform owns research lifecycle under /api/v1/integration/requests; "
        "Backend owns native execution admission and response artifacts; Platform checks research against Backend's "
        "stored records itself. "
        "Native_ and Platform_ names preserve each source-owned DTO. Public /v1 is defined by public-v1.openapi.json. "
        "See docs/research-flow.md and docs/reconnect-operations.md."
    )
    return contract


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend-openapi", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    actual = json.loads(CONTRACT.read_text())
    expected = project(args.backend_openapi, json.loads(json.dumps(actual)))
    if args.check:
        if actual != expected:
            raise SystemExit(
                "Native operation projection differs from the Backend export"
            )
    else:
        CONTRACT.write_text(json.dumps(expected, indent=2, sort_keys=True) + "\n")
    print("Shared native operation contracts agree with Backend")
