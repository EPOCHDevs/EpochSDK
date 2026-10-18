"""Validate caller-owned JSON Schema documents without external reference retrieval."""

from __future__ import annotations

import json
from urllib.parse import urljoin

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError
from pydantic import JsonValue
from referencing import Registry, Resource
from referencing.exceptions import Unresolvable
from referencing.jsonschema import DRAFT202012

# Keys inside the supplied JSON Schema belong to the caller, including properties,
# definitions and annotation extensions. Outer Epoch request models remain closed.
type JsonSchemaDocument = dict[str, JsonValue] | bool


def validate_schema(schema: JsonSchemaDocument) -> JsonSchemaDocument:
    """Check the dialect, schema and all local references, including unused branches."""
    try:
        json.dumps(schema, allow_nan=False)
        Draft202012Validator.check_schema(schema)
        root: Resource[JsonValue] = Resource.from_contents(
            schema, default_specification=DRAFT202012
        )
        registry = Registry[JsonValue]().with_resource("urn:epoch:output-schema", root).crawl()

        def walk(resource: Resource[JsonValue], resolver_base: str) -> None:
            contents = resource.contents
            if isinstance(contents, bool):
                return
            if not isinstance(contents, dict):
                raise TypeError("JSON Schema must be an object or boolean")
            dialect = contents.get("$schema")
            if dialect not in (None, "https://json-schema.org/draft/2020-12/schema"):
                raise ValueError("Use the JSON Schema 2020-12 dialect")
            resolver = registry.resolver(resolver_base).in_subresource(resource)
            for keyword in ("$ref", "$dynamicRef"):
                ref = contents.get(keyword)
                if ref is None:
                    continue
                if not isinstance(ref, str) or (ref != "" and not ref.startswith("#")):
                    raise ValueError("JSON Schema references must stay within the supplied schema")
                resolved = resolver.lookup(ref)
                if not isinstance(resolved.contents, (dict, bool)):
                    raise TypeError("JSON Schema reference must identify a schema")
            # Resource knows schema-bearing keywords, so examples and properties named
            # '$ref' are not mistaken for reference instructions.
            base = urljoin(resolver_base, resource.id() or "")
            for child in resource.subresources():
                walk(child, base)

        walk(root, "urn:epoch:output-schema")
    except (Unresolvable, SchemaError, TypeError, ValueError) as exc:
        raise ValueError(str(exc)) from exc
    return schema
