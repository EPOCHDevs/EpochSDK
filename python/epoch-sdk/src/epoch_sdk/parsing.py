"""One strict JSON entry point for graph, SDK and MCP request boundaries."""

import json

from .contracts import Contract


def _object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    value: dict[str, object] = {}
    for key, child in pairs:
        if key in value:
            raise ValueError(f"Duplicate JSON field: {key}")
        value[key] = child
    return value


def _non_finite(value: str) -> object:
    raise ValueError(f"Non-finite JSON number is not supported: {value}")


def parse_json(payload: str | bytes) -> object:
    """Reject ambiguous keys/non-finite numbers before a typed consumer validates."""
    return json.loads(payload, object_pairs_hook=_object, parse_constant=_non_finite)


def parse_request[T: Contract](model: type[T], payload: str | bytes) -> T:
    return model.model_validate(parse_json(payload))
