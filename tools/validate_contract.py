"""Validate the shared contract, examples and structural fixtures without a language SDK."""

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from openapi_spec_validator import validate

ROOT = Path(__file__).resolve().parents[1]
document = json.loads((ROOT / "contracts/openapi.json").read_text())
validate(document)
examples = 0
for methods in document["paths"].values():
    for operation in methods.values():
        if not isinstance(operation, dict) or "operationId" not in operation:
            continue
        containers = [operation.get("requestBody", {}), *operation["responses"].values()]
        for container in containers:
            for content in container.get("content", {}).values():
                schema = content.get("schema")
                if not schema:
                    continue
                validator = Draft202012Validator(
                    {"allOf": [schema], "components": document["components"]},
                    format_checker=FormatChecker(),
                )
                for example in content.get("examples", {}).values():
                    if "value" in example:
                        validator.validate(example["value"])
                        examples += 1

cases = json.loads((ROOT / "contracts/validation-cases.json").read_text())["cases"]
for case in cases:
    validator = Draft202012Validator(
        {"$ref": f"#/components/schemas/{case['schema']}", "components": document["components"]},
        format_checker=FormatChecker(),
    )
    assert validator.is_valid(case["value"]) == case["schema_valid"], case["name"]
print(f"Shared contract valid: {len(document['paths'])} paths, {examples} examples, {len(cases)} fixtures")
