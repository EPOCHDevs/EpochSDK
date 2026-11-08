"""Validate the public v1 API contract copied from EpochAI, its examples and the review doc's map.

EpochAI generates the contract from its routes and models and checks its examples as model values.
This check is independent of Python: it validates the document as OpenAPI and every example
against the generated JSON Schemas.
"""

import json
import sys
from pathlib import Path
from urllib.parse import quote

from jsonschema import Draft202012Validator, FormatChecker
from openapi_spec_validator import validate
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

ROOT = Path(__file__).resolve().parents[1]
NAME = "public-v1.openapi.json"
BASE = "https://epoch.invalid/contracts/"
INTERNAL = ("/api/", "/internal", "/agents", "/data-extent", "/threads", "/runs", "/assistants", "/store")

document = json.loads((ROOT / "contracts" / NAME).read_text())
validate(document)
REGISTRY = Registry().with_resource(BASE + NAME, Resource.from_contents(document, default_specification=DRAFT202012))


def checker(*parts):
    pointer = "/" + "/".join(str(part).replace("~", "~0").replace("/", "~1") for part in parts)
    return Draft202012Validator({"$ref": BASE + NAME + "#" + quote(pointer, safe="/~")},
                                registry=REGISTRY, format_checker=FormatChecker())


def check_examples(content, *parts):
    count = 0
    for media, body in content.items():
        if "schema" not in body:
            continue
        validator = checker(*parts, media, "schema")
        for name, example in body.get("examples", {}).items():
            errors = sorted(validator.iter_errors(example["value"]), key=str)
            assert not errors, f"{'/'.join(map(str, parts))} {media} example {name}: {errors[0].message}"
            count += 1
    return count


examples = 0
for path, item in document["paths"].items():
    assert path.startswith(("/v1/", "/.well-known/")), path
    assert not any(marker in path for marker in INTERNAL), f"{path} exposes an internal route"
    for method, operation in item.items():
        scopes = operation["x-epoch-scopes"]
        assert set(scopes) <= set(document["x-epoch-scopes"]) | {"session"}, f"{method} {path} scopes {scopes}"
        assert bool(scopes) == ("security" in operation), f"{method} {path}: scopes and authentication disagree"
        reuses = operation["x-epoch-reuses"]
        assert reuses["native"] or reuses.get("gaps"), f"{method} {path} names neither a native route nor a gap"
        if "requestBody" in operation:
            examples += check_examples(operation["requestBody"]["content"], "paths", path, method, "requestBody", "content")
        for status, response in operation["responses"].items():
            examples += check_examples(response.get("content", {}), "paths", path, method, "responses", status, "content")
            if "x-epoch-event-schema" in response:
                event = checker("paths", path, method, "responses", status, "x-epoch-event-schema")
                for name, value in response.get("x-epoch-event-examples", {}).items():
                    errors = sorted(event.iter_errors(value), key=str)
                    assert not errors, f"{method} {path} event {name}: {errors[0].message}"
                    examples += 1
for name, item in document.get("webhooks", {}).items():
    for method, operation in item.items():
        examples += check_examples(operation["requestBody"]["content"], "webhooks", name, method, "requestBody", "content")


def cell(text):
    return text.replace("|", "\\|")


def endpoint_map():
    rows = ["| Operation | SDK method reused | Native routes | Gaps |", "| -- | -- | -- | -- |"]
    for path, item in document["paths"].items():
        for method, operation in item.items():
            reuses = operation["x-epoch-reuses"]
            rows.append("| " + " | ".join([
                f"`{method.upper()} {path}`<br>{cell(operation['summary'])}",
                f"`{cell(reuses['sdk'])}`" if reuses.get("sdk") else "–",
                "<br>".join(cell(route) for route in reuses["native"]) or "–",
                "<br>".join(cell(gap) for gap in reuses.get("gaps", [])) or "–",
            ]) + " |")
    return "\n".join(rows)


START, END = "<!-- endpoint-map:start -->", "<!-- endpoint-map:end -->"
if "--map" in sys.argv:
    print(endpoint_map())
    raise SystemExit
doc = (ROOT / "docs/public-api-v1.md").read_text()
assert START in doc and END in doc, "docs/public-api-v1.md lacks the endpoint map markers"
current = doc.split(START, 1)[1].split(END, 1)[0].strip()
assert current == endpoint_map(), "docs/public-api-v1.md endpoint map is stale; regenerate it with --map"
operations = sum(len(item) for item in document["paths"].values())
print(f"Public v1 contract valid: {operations} operations, {examples} examples")
