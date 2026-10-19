"""Validate replay-plan wire fixtures using local schemas only.

Cross-reference and source/replay semantics are also checked by the SDK models
and must be enforced by the owning native service; schema success is not proof
that any query has executed or that its financial result is correct.
"""
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://epoch.invalid/contracts/"


def validators():
    registry = Registry()
    names = ["openapi.json", "response-plan-reference.schema.json", "response-plan-draft.schema.json",
             "response-plan-create.schema.json", "response-plan-definition.schema.json", "response-plan.schema.json"]
    for name in names:
        schema = json.loads((ROOT / "contracts" / name).read_text())
        Draft202012Validator.check_schema(schema)
        registry = registry.with_resource(BASE + name,
            Resource.from_contents(schema, default_specification=DRAFT202012))
    return {name: Draft202012Validator({"$ref": BASE + name}, registry=registry,
        format_checker=FormatChecker()) for name in names[1:]}


if __name__ == "__main__":
    checks = validators()
    cases = json.loads((ROOT / "contracts/response-plan.cases.json").read_text())
    for case in cases:
        assert checks[case["schema"]].is_valid(case["value"]) == case["valid"], case["name"]
    print(f"Replay-plan wire contract valid: {len(cases)} fixtures, local references only")
