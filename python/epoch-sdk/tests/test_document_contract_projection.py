"""Service-owned OpenAPI projection preserves identity and cannot expose worker APIs."""
import copy
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
SPEC = spec_from_file_location("sync_document_contract", ROOT / "tools/sync_document_contract.py")
MODULE = module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def source(path, schema, *, worker=False):
    result = {"paths": {path: {"get": {"operationId": schema,
        "responses": {"200": {"description": "ok", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/" + schema}}}}}}}},
        "components": {"schemas": {schema: {"type": "object", "properties": {"child": {"$ref": "#/components/schemas/Shared"}}},
            "Shared": {"type": "string"}, "Worker": {"type": "object", "properties": {"token": {"type": "string"}}}}}}
    if worker:
        result["paths"]["/internal/document-reads/claim"] = {"post": {"responses": {"200": {"description": "private", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Worker"}}}}}}}
    return result


def test_projection_is_idempotent_closes_refs_and_excludes_private_routes():
    contract = {"paths": {"/existing": {"get": {"operationId": "existing"}}},
        "components": {"schemas": {"Existing": {"type": "boolean"}}, "securitySchemes": {"BearerAuth": {"type": "http", "scheme": "bearer"}}}}
    backend = source("/api/v1/files/documents/search", "NativeResult", worker=True)
    ai = source("/api/v1/document-preparations", "AiResult")
    untouched = copy.deepcopy((contract, backend, ai))
    projected = MODULE.project(contract, backend, ai)
    assert (contract, backend, ai) == untouched
    assert projected == MODULE.project(projected, backend, ai)
    assert "/internal/document-reads/claim" not in projected["paths"]
    assert projected["paths"]["/existing"] == contract["paths"]["/existing"]
    assert "Worker" not in str(projected)
    schemas = projected["components"]["schemas"]
    for prefix, result in [("NativeResource_", "NativeResult"), ("EpochDocument_", "AiResult")]:
        assert schemas[prefix + result]["properties"]["child"]["$ref"] == "#/components/schemas/" + prefix + "Shared"
        assert schemas[prefix + "Shared"] == {"type": "string"}
    assert projected["paths"]["/api/v1/document-preparations"]["get"]["security"] == [{"BearerAuth": []}]


def test_projection_cannot_replace_an_unrelated_existing_route():
    contract = {"paths": {"/api/v1/files/existing": {}}, "components": {"schemas": {}}}
    with pytest.raises(ValueError, match="cannot replace"):
        MODULE.project(contract, source("/api/v1/files/existing", "One"), {"paths": {}, "components": {"schemas": {}}})
