"""Restore source-owned request models and boolean union tags after pinned Fern generation.

The common normalizer is reused without changing its Backend-owned copy. Request roots and
literal fields are derived from Platform's canonical contract, never from a second field list.
"""

from __future__ import annotations

import argparse
import ast
import importlib.util
import json
import math
import os
import re
from pathlib import Path


def objects(value):
    if isinstance(value, dict):
        if "properties" in value and any(
            type(v.get("const")) is bool for v in value["properties"].values()
        ):
            yield value
        for child in value.values():
            yield from objects(child)
    elif isinstance(value, list):
        for child in value:
            yield from objects(child)


def camel(value):
    return re.sub(r"_([a-z])", lambda m: m[1].upper(), value)


def normalize_typescript_requests(typescript, document, roots):
    spec = importlib.util.spec_from_file_location(
        "request_serializers",
        Path(__file__).parent / "fern_patches/normalize_closed_typescript_requests.py",
    )
    serializers = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(serializers)
    (typescript / "core/sourceOwnedRequestSchema.js").write_text(serializers.HELPER)
    for name in sorted(roots):
        schema = document["components"]["schemas"][name]
        matches = list((typescript / "serialization").rglob(name + ".js"))
        if len(matches) != 1:
            raise ValueError("Cannot identify generated request serializer: " + name)
        path = matches[0]
        text = path.read_text()
        helper = Path(
            os.path.relpath(typescript / "core/sourceOwnedRequestSchema", path.parent)
        ).as_posix()
        if not helper.startswith("."):
            helper = "./" + helper
        helper = f"require({json.dumps(helper)})"
        for field, definition in schema.get("properties", {}).items():
            if definition.get("type") != "integer":
                continue
            minimum = definition.get("minimum", -9007199254740991)
            maximum = definition.get("maximum", 9007199254740991)
            if "exclusiveMinimum" in definition:
                minimum = max(minimum, math.floor(definition["exclusiveMinimum"]) + 1)
            if "exclusiveMaximum" in definition:
                maximum = min(maximum, math.ceil(definition["exclusiveMaximum"]) - 1)
            replacement = f"{helper}.sourceOwnedInteger(core.serialization.number(), {minimum}, {maximum})"
            text, count = re.subn(
                rf"(?m)^(    {camel(field)}: [^\n]*?)core.serialization.number\(\)",
                lambda m, replacement=replacement: m[1] + replacement,
                text,
            )
            if count != 1:
                raise ValueError(
                    "Cannot restore bounded integer: " + name + "." + field
                )
        if schema.get("additionalProperties") is False:
            text += f"\n// Platform source-owned request validation.\nexports.{name} = {helper}.sourceOwnedClosedRequest(exports.{name}, [], true, true);\n"
        path.write_text(text)


def normalize(package_root: Path, typescript: Path, contract: Path):
    document = json.loads(contract.read_text())
    roots = set()
    for item in document["paths"].values():
        for operation in item.values():
            if not isinstance(operation, dict):
                continue
            schema = (
                operation.get("requestBody", {})
                .get("content", {})
                .get("application/json", {})
                .get("schema", {})
            )
            if "$ref" in schema:
                roots.add(schema["$ref"].removeprefix("#/components/schemas/"))
    spec = importlib.util.spec_from_file_location(
        "source_models",
        Path(__file__).parent / "fern_patches/normalize_discovery_sdk_contracts.py",
    )
    source_models = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(source_models)
    original_schema_type = source_models.schema_type

    def schema_type(definition, imports, components):
        # OpenAPI's unconstrained JSON schema is used for the redacted projection.
        if set(definition) <= {"description", "title"}:
            return "typing.Any"
        if "enum" in definition:
            literal = (
                "typing.Literal[" + ", ".join(repr(v) for v in definition["enum"]) + "]"
            )
            return source_models.constrained(literal, definition)
        return original_schema_type(definition, imports, components)

    source_models.schema_type = schema_type
    original_numeric = source_models.numeric_constraints

    def numeric_constraints(definition, components):
        constraints = original_numeric(definition, components)
        for source, target in [("exclusiveMinimum", "gt"), ("exclusiveMaximum", "lt")]:
            if source in definition:
                constraints[target] = definition[source]
        return constraints

    source_models.numeric_constraints = numeric_constraints
    source_models.PACKAGE = "shares_api"
    source_models.NATIVE_PREFIXES = tuple(sorted(roots))
    source_models.normalize(package_root, contract, lenient_responses=True)

    normalize_typescript_requests(typescript, document, roots)

    alternatives = {}
    for schema in objects(document["components"]["schemas"]):
        fields = frozenset(schema["properties"])
        constants = {
            k: v["const"]
            for k, v in schema["properties"].items()
            if type(v.get("const")) is bool
        }
        if fields in alternatives and alternatives[fields] != constants:
            raise ValueError(
                "Cannot identify generated alternatives by their wire field sets"
            )
        alternatives[fields] = constants
    seen_python, seen_typescript = set(), set()
    for path in (package_root / "shares_api/types").glob("*.py"):
        text = path.read_text()
        for cls in ast.parse(text).body:
            if not isinstance(cls, ast.ClassDef):
                continue
            fields = {
                source_models.wire_field_name(field): field
                for field in cls.body
                if isinstance(field, ast.AnnAssign)
                and isinstance(field.target, ast.Name)
                and field.target.id != "model_config"
            }
            constants = alternatives.get(frozenset(fields))
            if not constants:
                continue
            for name, value in constants.items():
                field = fields[name]
                original = ast.get_source_segment(text, field.annotation)
                replacement = f"typing.Literal[{value!r}]"
                text, count = re.subn(
                    rf"(?m)^(    {field.target.id}: )" + re.escape(original),
                    lambda m, replacement=replacement: m[1] + replacement,
                    text,
                )
                if count != 1:
                    raise ValueError("Boolean literal field could not be restored")
            seen_python.add(frozenset(fields))
        path.write_text(text)
    for path in (typescript / "api/types").glob("*.d.ts"):
        text = path.read_text()
        fields = frozenset(re.findall(r"^    (\w+)\??:", text, re.MULTILINE))
        matches = [
            (wire, constants)
            for wire, constants in alternatives.items()
            if fields == frozenset(map(camel, wire))
        ]
        if not matches:
            continue
        if len(matches) != 1:
            raise ValueError("Ambiguous generated TypeScript alternative")
        wire, constants = matches[0]
        serializer = (
            typescript / "serialization/types" / (path.stem.removesuffix(".d") + ".js")
        )
        raw_types = serializer.with_suffix(".d.ts")
        runtime, raw = serializer.read_text(), raw_types.read_text()
        for name, value in constants.items():
            literal, field = json.dumps(value), camel(name)
            text, count = re.subn(
                rf"(?m)^(    {field}: )boolean;",
                lambda m, literal=literal: m[1] + literal + ";",
                text,
            )
            if count != 1:
                raise ValueError("TypeScript literal declaration could not be restored")
            runtime, count = re.subn(
                rf"(?m)^(    {field}: [^\n]*?)core.serialization.boolean\(\)",
                lambda m, literal=literal: (
                    m[1] + f"core.serialization.booleanLiteral({literal})"
                ),
                runtime,
            )
            if count != 1:
                raise ValueError("TypeScript literal decoder could not be restored")
            raw, count = re.subn(
                rf"(?m)^(        {name}: )boolean;",
                lambda m, literal=literal: m[1] + literal + ";",
                raw,
            )
            if count != 1:
                raise ValueError(
                    "TypeScript wire literal declaration could not be restored"
                )
        path.write_text(text)
        serializer.write_text(runtime)
        raw_types.write_text(raw)
        seen_typescript.add(wire)
    if seen_python != set(alternatives) or seen_typescript != set(alternatives):
        raise ValueError(
            "A canonical boolean alternative is missing from generated clients"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-root", type=Path, required=True)
    parser.add_argument("--typescript", type=Path, required=True)
    parser.add_argument("--openapi", type=Path, required=True)
    args = parser.parse_args()
    normalize(args.package_root, args.typescript, args.openapi)
