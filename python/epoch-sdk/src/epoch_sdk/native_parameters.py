"""Reuse native SDK parameter types; enforce the source-owned Backend wire schema."""

from __future__ import annotations

import json
from importlib.resources import files
from typing import Annotated, TypedDict, cast

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import ValidationError
from pydantic import BeforeValidator, JsonValue, WithJsonSchema
from pydantic.json_schema import JsonSchemaValue
from stratifyx import DatePeriodConfig, ExecutionOptions


class _NativeSchemaBundle(TypedDict):
    source: str
    sha256: str
    # Schema names/properties are owned by the native OpenAPI namespace.
    schemas: dict[str, JsonSchemaValue]


_bundle = cast(
    _NativeSchemaBundle,
    json.loads(files("epoch_sdk").joinpath("data/native-parameters.json").read_text()),
)


def _wire_schema(name: str) -> JsonSchemaValue:
    # Native parameter schemas are small and acyclic. Inline their source-owned
    # references so a standalone graph/MCP input schema needs no external resolver.
    def expand(node: JsonValue, active: frozenset[str]) -> JsonValue:
        if isinstance(node, list):
            return [expand(value, active) for value in node]
        if not isinstance(node, dict):
            return node
        ref = node.get("$ref")
        if isinstance(ref, str):
            if not ref.startswith("#/$defs/"):
                raise ValueError("Native parameter references must be local")
            target = ref.removeprefix("#/$defs/")
            if target in active:
                raise ValueError("Recursive native parameter schema needs an explicit projection")
            resolved = expand(_bundle["schemas"][target], active | {target})
            siblings = {key: expand(value, active) for key, value in node.items() if key != "$ref"}
            return {"allOf": [resolved], **siblings} if siblings else resolved
        return {key: expand(value, active) for key, value in node.items()}

    result = expand(_bundle["schemas"][name], frozenset({name}))
    if not isinstance(result, dict):
        raise TypeError("Native parameter root must be an object schema")
    return result


def _validate(value: object, model: type[DatePeriodConfig | ExecutionOptions], name: str) -> object:
    if isinstance(value, model):
        wire = value.model_dump(mode="json", by_alias=True, exclude_unset=True)
    else:
        wire = value
    try:
        wire_json: JsonValue = json.loads(json.dumps(wire, allow_nan=False))
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid Backend {name}: expected finite JSON values") from exc
    validator = Draft202012Validator(
        {"$ref": f"#/$defs/{name}", "$defs": _bundle["schemas"]}, format_checker=FormatChecker()
    )
    try:
        # jsonschema's public validate method leaves *args/**kwargs untyped.
        # The input is finite JsonValue above and the output stays a native SDK type.
        validator.validate(wire_json)  # pyright: ignore[reportUnknownMemberType]
    except ValidationError as exc:
        raise ValueError(f"Invalid Backend {name}: {exc.message}") from exc
    # Native types remain authoritative; never add client-owned copies of their fields.
    return model.model_validate(wire)


def _period(value: object) -> object:
    return _validate(value, DatePeriodConfig, "DatePeriodConfig")


def _execution(value: object) -> object:
    return _validate(value, ExecutionOptions, "ExecutionOptions")


NativePeriod = Annotated[
    DatePeriodConfig, BeforeValidator(_period), WithJsonSchema(_wire_schema("DatePeriodConfig"))
]
NativeExecutionOptions = Annotated[
    ExecutionOptions, BeforeValidator(_execution), WithJsonSchema(_wire_schema("ExecutionOptions"))
]
