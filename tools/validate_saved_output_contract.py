"""Check the language-neutral saved-output receipt without a native SDK."""

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "contracts/saved-output-manifest.schema.json"
core = ROOT / "contracts/openapi.json"
schema = json.loads(path.read_text())
Draft202012Validator.check_schema(schema)
# Resolve only the two checked-in resources. No HTTP/file fetch fallback is
# installed; declaration schemas remain owned by the existing shared contract.
registry = Registry().with_resources(
    [
        (
            path.as_uri(),
            Resource.from_contents(schema, default_specification=DRAFT202012),
        ),
        (
            core.as_uri(),
            Resource.from_contents(
                json.loads(core.read_text()), default_specification=DRAFT202012
            ),
        ),
    ]
)
validator = Draft202012Validator(
    {"$ref": path.as_uri()}, registry=registry, format_checker=FormatChecker()
)
example = json.loads(
    (ROOT / "contracts/saved-output-manifest.example.json").read_text()
)
validator.validate(example)
print("Saved-output manifest and its shared declaration references are valid")
