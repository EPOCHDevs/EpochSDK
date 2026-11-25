"""Apply existing source-owned request normalization to Platform model clients."""

from __future__ import annotations

import argparse
import ast
import importlib.util
import json
import os
import re
from pathlib import Path


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def normalize(package_root: Path, typescript: Path, contract: Path) -> None:
    document = json.loads(contract.read_text())
    roots = set()
    for item in document["paths"].values():
        for operation in item.values():
            if not isinstance(operation, dict):
                continue
            schema = operation.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema", {})
            if "$ref" in schema:
                roots.add(schema["$ref"].removeprefix("#/components/schemas/"))
    patches = Path(__file__).parent / "fern_patches"
    python = load("source_owned_models", patches / "normalize_discovery_sdk_contracts.py")
    python.PACKAGE = "models_api"
    python.NATIVE_PREFIXES = tuple(sorted(roots))
    python.normalize(package_root, contract, lenient_responses=True)
    # The shared normalizer restores object keys/constraints but represents
    # request string enums as str. Preserve Models' finite source selection in
    # both its static annotation and Pydantic validation.
    for path in (package_root / 'models_api/types').glob('*.py'):
        source = path.read_text()
        lines = source.splitlines(keepends=True)
        offsets = [0]
        for line in lines: offsets.append(offsets[-1] + len(line))
        edits = []
        for node in ast.parse(source).body:
            if not isinstance(node, ast.ClassDef) or node.name not in roots:
                continue
            schema = document['components']['schemas'][node.name]
            for field in node.body:
                if not isinstance(field, ast.AnnAssign) or not isinstance(field.target, ast.Name): continue
                prop = schema.get('properties', {}).get(field.target.id, {})
                values = prop.get('enum')
                if not values: continue
                literal = 'typing.Literal[' + ', '.join(repr(value) for value in values) + ']'
                if field.target.id not in schema.get('required', []): literal = 'typing.Optional[' + literal + ']'
                annotation = field.annotation
                edits.append((offsets[annotation.lineno - 1] + annotation.col_offset,
                    offsets[annotation.end_lineno - 1] + annotation.end_col_offset, literal))
        for start, end, replacement in sorted(edits, reverse=True): source = source[:start] + replacement + source[end:]
        if edits: path.write_text(source)
    operations = {}
    for item in document["paths"].values():
        for operation in item.values():
            if not isinstance(operation, dict):
                continue
            body = operation.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema", {})
            if "$ref" in body:
                method = re.sub(r"(?<!^)(?=[A-Z])", "_", operation["operationId"]).lower()
                operations[method] = body["$ref"].removeprefix("#/components/schemas/")
    raw_client = package_root / "models_api/raw_client.py"
    text = raw_client.read_text()
    lines = text.splitlines(keepends=True)
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))
    replacements = []
    for method in ast.walk(ast.parse(text)):
        if not isinstance(method, (ast.FunctionDef, ast.AsyncFunctionDef)) or method.name not in operations:
            continue
        bodies = [keyword.value for node in ast.walk(method) if isinstance(node, ast.Call)
                  for keyword in node.keywords if keyword.arg == "json"]
        if len(bodies) != 1 or not isinstance(bodies[0], ast.Dict):
            raise ValueError("Cannot identify flattened request body: " + method.name)
        body = bodies[0]
        start = offsets[body.lineno - 1] + body.col_offset
        end = offsets[body.end_lineno - 1] + body.end_col_offset
        replacements.append((start, end,
            f'{operations[method.name]}.model_validate({{key: value for key, value in ({text[start:end]}).items() if value is not OMIT}}).model_dump(mode="json", exclude_none=True)'))
    if len(replacements) != len(operations) * 2:
        raise ValueError("Both sync and async raw request paths must be normalized")
    for start, end, replacement in sorted(replacements, reverse=True):
        text = text[:start] + replacement + text[end:]
    text = "from .types import " + ", ".join(sorted(roots)) + "\n" + text
    ast.parse(text)
    raw_client.write_text(text)
    ts = load("source_owned_typescript", patches / "normalize_closed_typescript_requests.py")
    ts.apply(typescript, contract)
    (typescript / "core/sourceOwnedRequestSchema.js").write_text(ts.HELPER)
    (typescript / "core/platformRequestSchema.js").write_text('''"use strict";
const Ajv2020 = require("ajv/dist/2020").default;
const {getSchemaUtils} = require("./schemas/builders/schema-utils");
const {getObjectLikeUtils} = require("./schemas/builders/object-like");
const {getObjectUtils} = require("./schemas/builders/object/object");
exports.platformRequestSchema = function(schema, definition) {
    const validate = new Ajv2020({allErrors: true, strict: true}).compile(definition);
    const exact = {...schema, json: (value, options) => {
        const result = schema.json(value, options);
        if (!result.ok || validate(result.value)) return result;
        return {ok: false, errors: validate.errors.map(error => ({
            path: [...(options?.breadcrumbsPrefix ?? []), ...error.instancePath.split("/").filter(Boolean)],
            message: `Platform request fails ${error.keyword}`,
        }))};
    }};
    return Object.assign(exact, getSchemaUtils(exact), getObjectLikeUtils(exact), getObjectUtils(exact));
};
''')
    for name in roots:
        schema = document["components"]["schemas"][name]
        if schema.get("additionalProperties") is not False:
            continue
        serializers = list((typescript / "serialization").rglob(name + ".js"))
        if len(serializers) != 1:
            raise ValueError("Cannot identify source-owned request serializer: " + name)
        path = serializers[0]
        helper = Path(os.path.relpath(typescript / "core/sourceOwnedRequestSchema", path.parent)).as_posix()
        if not helper.startswith("."):
            helper = "./" + helper
        with path.open("a") as output:
            output.write(f"\n// Platform saved-model outbound request validation.\nexports.{name} = require({json.dumps(helper)}).sourceOwnedClosedRequest(exports.{name}, [], true, true);\n")
            validation_helper = helper.replace("sourceOwnedRequestSchema", "platformRequestSchema")
            output.write(f"exports.{name} = require({json.dumps(validation_helper)}).platformRequestSchema(exports.{name}, {json.dumps(schema)});\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-root", type=Path, required=True)
    parser.add_argument("--typescript", type=Path, required=True)
    parser.add_argument("--openapi", type=Path, required=True)
    args = parser.parse_args()
    normalize(args.package_root, args.typescript, args.openapi)
