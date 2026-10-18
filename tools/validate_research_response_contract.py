"""Validate the shared saved-response contract using only local schema resources."""

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://epoch.invalid/contracts/"


def validator() -> Draft202012Validator:
    registry = Registry()
    for name in ("openapi.json", "research-response.schema.json"):
        document = json.loads((ROOT / "contracts" / name).read_text())
        registry = registry.with_resource(
            BASE + name, Resource.from_contents(document, default_specification=DRAFT202012)
        )
    return Draft202012Validator(
        {"$ref": BASE + "research-response.schema.json"},
        registry=registry,
        format_checker=FormatChecker(),
    )


if __name__ == "__main__":
    schema = json.loads((ROOT / "contracts/research-response.schema.json").read_text())
    Draft202012Validator.check_schema(schema)
    value = json.loads((ROOT / "contracts/research-response.example.json").read_text())
    validator().validate(value)
    print("Saved research response and its shared declaration/value references are valid")
