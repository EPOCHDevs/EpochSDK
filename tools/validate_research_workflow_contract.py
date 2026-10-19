"""Validate research workflow fixtures without private client dependencies."""

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://epoch.invalid/contracts/"


def validator():
    registry = Registry()
    for name in ("openapi.json", "research-response.schema.json", "research-workflow.schema.json"):
        document = json.loads((ROOT / "contracts" / name).read_text())
        registry = registry.with_resource(
            BASE + name, Resource.from_contents(document, default_specification=DRAFT202012),
        )
    return Draft202012Validator(
        {"$ref": BASE + "research-workflow.schema.json"}, registry=registry,
        format_checker=FormatChecker(),
    )


if __name__ == "__main__":
    Draft202012Validator.check_schema(json.loads(
        (ROOT / "contracts/research-workflow.schema.json").read_text(),
    ))
    cases = json.loads((ROOT / "contracts/research-workflow.cases.json").read_text())
    check = validator()
    for case in cases:
        assert check.is_valid(case["value"]) == case["valid"], case["name"]
    print(f"Research workflow contract valid: {len(cases)} fixtures, local references only")
