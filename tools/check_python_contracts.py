"""Check Python binding conformance without rewriting the language-neutral contract."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python/epoch-sdk/src"))

from epoch_sdk.contracts import (
    AccessRequirement,
    Acknowledgement,
    Column,
    DataRequirement,
    DomainError,
    ErrorResponse,
    FetchPageRequest,
    FreshFetchRequest,
    Gap,
    IngestRequest,
    JsonOutputRequest,
    Question,
    RefreshRequest,
    RunParameters,
    RunRequest,
    TableOutputRequest,
    TextOutputRequest,
)

MODELS = (
    ("Column", Column),
    ("TableOutputRequest", TableOutputRequest),
    ("JsonOutputRequest", JsonOutputRequest),
    ("TextOutputRequest", TextOutputRequest),
    ("RunParameters", RunParameters),
    ("RunRequest", RunRequest),
    ("IngestRequest", IngestRequest),
    ("FreshFetchRequest", FreshFetchRequest),
    ("FetchPageRequest", FetchPageRequest),
    ("RefreshRequest", RefreshRequest),
    ("Gap", Gap),
    ("Question", Question),
    ("DataRequirement", DataRequirement),
    ("AccessRequirement", AccessRequirement),
    ("Error", DomainError),
    ("ErrorResponse", ErrorResponse),
    ("Acknowledgement", Acknowledgement),
)


def project(document: dict) -> dict:
    document = json.loads(json.dumps(document))
    components = document["components"]["schemas"]
    public_model_names = {model.__name__ for _, model in MODELS} | {"ErrorCode"}
    for name, model in MODELS:
        schema = model.model_json_schema(ref_template="#/components/schemas/{model}")
        definitions = schema.pop("$defs", {})
        # Native parameter types come exclusively from Backend's wire projection
        # below. SDK releases can rename internal union models without changing
        # that API; do not leak those generated implementation details here.
        components.update(
            {key: value for key, value in definitions.items() if key in public_model_names}
        )
        components[name] = schema
    native = json.loads((ROOT / "contracts/native-parameters.json").read_text())
    components.update(
        json.loads(json.dumps(native["schemas"]).replace("#/$defs/", "#/components/schemas/"))
    )
    components.pop("DomainError", None)
    # Keep the v0.8 standard JSON Schema name and object/boolean wire contract.
    components.pop("JsonSchemaDocument", None)
    document = json.loads(
        json.dumps(document)
        .replace("#/components/schemas/DomainError", "#/components/schemas/Error")
        .replace("#/components/schemas/JsonSchemaDocument", "#/components/schemas/JsonSchema")
    )
    return document


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check Python bindings against the shared contract")
    parser.add_argument("--check", action="store_true", help="Compatibility flag; this command only checks")
    parser.parse_args()
    contract = ROOT / "contracts/openapi.json"
    actual = json.loads(contract.read_text())
    if actual != project(actual):
        raise SystemExit("Python bindings differ from the shared contract; align both deliberately")
    print("Python request/error schemas match the shared contract")
