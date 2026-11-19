#!/usr/bin/env python3
# Copied from EPOCHDevs/EpochBackend scripts/normalize_discovery_sdk_contracts.py at 381ca0292d (ENG-2819). The Files
# client runs the same pinned Fern generators, so it needs the same fixes. Change both copies
# together while EpochBackend still generates StratifyX.
"""Keep selected generated request models consistent with native OpenAPI.

Fern 4.46.6 can optionalize required nested union/recursive fields and always
emits extra=allow. Restore Discovery requiredness and source-declared closure
through their reachable component graphs, from native OpenAPI. Existing generated
classes, recursive references and value types remain authoritative. Native
request defaults distinguish omission from null; never maintain an independent
field/type/enum list.
"""
from __future__ import annotations

import argparse
import ast
import json
import re
from pathlib import Path


def normalized(name: str) -> str:
    return ''.join(c.lower() for c in name if c.isalnum())


# The generated package's directory name (EpochBackend: stratifyx).
PACKAGE = 'stratifyx'

COMPONENT_MARKER = '# Source-owned Discovery component restored from canonical OpenAPI.'
EXPORT_MARKER = '# Source-owned Discovery component exports.'
NATIVE_PREFIXES = ('NativeObservation', 'DataPreview', 'Discovery', 'DatasetCatalog', 'DatasetSearch', 'DatasetObservation', 'DatasetSourceMetadata', 'ScreenAssets',
                   'AssetUniverse', 'StudyData', 'SubmitPortfolioSnapshot',
                   'Space', 'StructuredImport', 'DatasetReview', 'DatasetBuild',
                   'DatasetEvidence', 'DatasetCitation', 'DatasetProcessingCoverage', 'Web')
# Retiring worker bodies leaves this existing public selection used only as a
# flattened endpoint body. Preserve its source-owned SDK snapshot as before.
REQUEST_SNAPSHOTS = frozenset({'MiContextTaskSelection'})


def primitive_schema(schema: dict, components: dict) -> dict:
    """Resolve only source-declared primitive aliases, never enums or objects."""
    primitive_keys = {'type', 'description', 'title', 'minimum', 'maximum', 'format',
                      'default', 'pattern', 'minLength', 'maxLength'}
    arms = schema.get('anyOf')
    if (set(schema) <= {'anyOf', 'description', 'title', 'default'}
            and isinstance(arms, list) and len(arms) == 2
            and sum(arm == {'type': 'null'} for arm in arms) == 1):
        value = next(arm for arm in arms if arm != {'type': 'null'})
        definition = primitive_schema(value, components)
        if (set(definition) <= primitive_keys
                and definition.get('type') in ('boolean', 'string', 'integer', 'number')):
            return {**definition, 'type': [definition['type'], 'null'],
                    **{key: value for key, value in schema.items() if key != 'anyOf'}}
    if '$ref' in schema:
        referenced = components.get(schema['$ref'].rsplit('/', 1)[-1], {})
        if (set(referenced) <= primitive_keys
                and referenced.get('type') in ('boolean', 'string', 'integer', 'number', 'null')):
            return {**referenced, **{key: value for key, value in schema.items() if key != '$ref'}}
    return schema


def allows_null(schema: dict, components: dict, seen: frozenset[str] = frozenset()) -> bool:
    """Read nullability from the native field/alias, not Fern's Optional annotation."""
    kind = schema.get('type')
    if schema.get('nullable') is True or kind == 'null' or isinstance(kind, list) and 'null' in kind:
        return True
    if any(allows_null(arm, components, seen) for key in ('anyOf', 'oneOf')
           for arm in schema.get(key, [])):
        return True
    if '$ref' in schema:
        reference = schema['$ref']
        name = reference.removeprefix('#/components/schemas/')
        if name == reference or name in seen or name not in components:
            raise ValueError(f'Unresolved native default nullability: {reference}')
        return allows_null(components[name], components, seen | {name})
    return False


def optional_annotation(annotation: str) -> str:
    return annotation if annotation.startswith('typing.Optional[') else f'typing.Optional[{annotation}]'


def numeric_constraints(schema: dict, components: dict) -> dict:
    """Reject coercion on request numbers/booleans without changing enums/dates."""
    definition = primitive_schema(schema, components)
    kind = definition.get('type')
    if isinstance(kind, list):
        kind = next((value for value in kind if value != 'null'), None)
    if kind not in ('integer', 'number', 'boolean') or 'enum' in definition or 'const' in definition:
        return {}
    constraints = {'strict': True}
    if kind == 'number':
        constraints['allow_inf_nan'] = False
    for key, argument in (('minimum', 'ge'), ('maximum', 'le')):
        if key in definition:
            bound = definition[key]
            if type(bound) not in (int, float) or kind == 'boolean':
                raise ValueError(f'Invalid numeric Discovery bound: {definition}')
            constraints[argument] = bound
    return constraints


def module_name(name: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()


def constrained(annotation: str, schema: dict) -> str:
    constraints = []
    for key, argument, kinds in (
        ('minimum', 'ge', ('integer', 'number')),
        ('maximum', 'le', ('integer', 'number')),
        ('minLength', 'min_length', ('string',)),
        ('maxLength', 'max_length', ('string',)),
        ('minItems', 'min_length', ('array',)),
        ('maxItems', 'max_length', ('array',)),
        ('pattern', 'pattern', ('string',)),
    ):
        if key not in schema:
            continue
        kind = schema.get('type')
        if kind not in kinds and not (isinstance(kind, list) and
                                     set(kind) - {'null'} <= set(kinds)):
            raise ValueError(f'Invalid {key} constraint on Discovery schema: {schema}')
        value = schema[key]
        if key == 'pattern':
            if not isinstance(value, str):
                raise ValueError('Discovery string pattern must be a string')
        elif type(value) not in (int, float):
            raise ValueError(f'Discovery {key} must be numeric')
        constraints.append(f'{argument}={value!r}')
    if 'description' in schema:
        if not isinstance(schema['description'], str):
            raise ValueError('Discovery description must be a string')
        constraints.append(f'description={schema["description"]!r}')
    return (f'typing.Annotated[{annotation}, pydantic.Field({", ".join(constraints)})]'
            if constraints else annotation)


def has_string_constraints(schema: dict, components: dict | None = None) -> bool:
    schema = primitive_schema(schema, components or {})
    return (any(key in schema for key in ('pattern', 'minLength', 'maxLength', 'minItems', 'maxItems'))
            or isinstance(schema.get('items'), dict) and has_string_constraints(schema['items'], components))


def schema_type(schema: dict, imports: set[str], components: dict) -> str:
    if 'anyOf' in schema:
        primitive = primitive_schema(schema, components)
        if primitive != schema:
            return schema_type(primitive, imports, components)
    if '$ref' in schema:
        name = schema['$ref'].rsplit('/', 1)[-1]
        referenced = primitive_schema(schema, components)
        # Native reflection can name a primitive alias (e.g. optional_bool),
        # while Fern spells its Python alias differently. Resolve only plain
        # primitives from their source schema; preserve enums and constraints.
        if '$ref' not in referenced:
            return schema_type(referenced, imports, components)
        imports.add(name)
        return name
    kind = schema.get('type')
    if isinstance(kind, list):
        nonnull = [value for value in kind if value != 'null']
        if len(nonnull) != 1:
            raise ValueError(f'Unsupported Discovery component type: {schema}')
        kind = nonnull[0]
    if kind == 'array':
        item = schema_type(schema['items'], imports, components)
        if allows_null(schema['items'], components):
            item = optional_annotation(item)
        return constrained(f'typing.List[{item}]', schema)
    if kind == 'object' and isinstance(schema.get('additionalProperties'), dict) and 'properties' not in schema:
        return f'typing.Dict[str, {schema_type(schema["additionalProperties"], imports, components)}]'
    primitives = {'string': 'str', 'integer': 'int', 'number': 'float',
                  'boolean': 'bool', 'null': 'None'}
    if kind not in primitives:
        raise ValueError(f'Unsupported inline Discovery component schema: {schema}')
    return constrained(primitives[kind], schema)


def restore_request_components(package: Path, schemas: dict) -> int:
    """Fern flattens endpoint bodies; keep their source-owned request snapshots.

    Names, fields, requiredness and referenced types come only from the native
    component schemas. Existing Fern models and its endpoint signatures remain
    authoritative. No wrapper body/type roster is maintained here.
    """
    restored = {}
    changed = 0
    models = package / PACKAGE / 'types'
    for name, schema in sorted(schemas.items()):
        if (not (name.startswith(NATIVE_PREFIXES) and name.endswith('Request') or name in REQUEST_SNAPSHOTS)
                or 'properties' not in schema):
            continue
        path = models / f'{module_name(name)}.py'
        if path.exists() and COMPONENT_MARKER not in path.read_text():
            continue
        imports: set[str] = set()
        fields = []
        required = set(schema.get('required', []))
        for field, definition in schema['properties'].items():
            annotation = schema_type(definition, imports, schemas)
            constraints = numeric_constraints(definition, schemas)
            if 'description' in definition:
                description = definition['description']
                if not isinstance(description, str):
                    raise ValueError(f'Invalid Discovery description: {name}.{field}')
                constraints['description'] = description
            definition = primitive_schema(definition, schemas)
            if field not in required:
                if 'default' in definition:
                    # A default permits omission; nullability remains source-owned.
                    if allows_null(definition, schemas):
                        annotation = optional_annotation(annotation)
                    elif definition['default'] is None:
                        raise ValueError(f'Nonnullable native default is null: {name}.{field}')
                    constraints['default'] = definition['default']
                else:
                    annotation = optional_annotation(annotation)
                    constraints['default'] = None
            if constraints:
                arguments = ', '.join(f'{key}={value!r}' for key, value in constraints.items())
                annotation += f' = pydantic.Field({arguments})'
            fields.append(f'    {field}: {annotation}')
        output = '\n'.join([
            COMPONENT_MARKER, 'from __future__ import annotations', '', 'import typing',
            'import pydantic', 'from ..core.pydantic_utilities import UniversalBaseModel',
            *[f'from .{module_name(reference)} import {reference}' for reference in sorted(imports)],
            '', '', f'class {name}(UniversalBaseModel):', *fields, '',
            '    model_config: typing.ClassVar[pydantic.ConfigDict] = '
            'pydantic.ConfigDict(extra="forbid", frozen=True)', '',
        ])
        ast.parse(output)
        if not path.exists() or path.read_text() != output:
            path.write_text(output)
            changed += 1
        restored[name] = f'.{module_name(name)}'
    for path, prefix in ((models / '__init__.py', ''), (package / PACKAGE / '__init__.py', 'types.')):
        if not restored or not path.exists():
            continue
        old = path.read_text()
        base = old.split(EXPORT_MARKER, 1)[0].rstrip() + '\n'
        output = base + '\n' + EXPORT_MARKER + '\nif typing.TYPE_CHECKING:\n'
        output += ''.join(f'    from .{prefix}{module_name(name)} import {name}\n' for name in restored)
        mapping = restored if not prefix else {name: '.types' for name in restored}
        output += f'_dynamic_imports.update({mapping!r})\n'
        output += f'__all__.extend({list(restored)!r})\n'
        ast.parse(output)
        if output != old:
            path.write_text(output)
    return changed


def reachable_components(schemas: dict, roots: list[str]) -> dict:
    pending = list(roots)
    reached = {}
    def references(value):
        if isinstance(value, dict):
            reference = value.get('$ref')
            if isinstance(reference, str) and reference.startswith('#/components/schemas/'):
                yield reference.rsplit('/', 1)[-1]
            for child in value.values():
                yield from references(child)
        elif isinstance(value, list):
            for child in value:
                yield from references(child)
    while pending:
        name = pending.pop()
        if name in reached:
            continue
        if name not in schemas:
            raise ValueError(f'Missing native Discovery component reference: {name}')
        reached[name] = schemas[name]
        pending.extend(references(schemas[name]))
    return reached


def reachable_discovery_schemas(schemas: dict) -> dict:
    """Keep Discovery contracts and close objects reachable from its requests.

    Response-only foreign components keep their existing generation policy.
    The request graph is source-owned, including recursive screen aliases.
    """
    reached = {name: schema for name, schema in schemas.items()
               if name.startswith(NATIVE_PREFIXES) or name in REQUEST_SNAPSHOTS}
    reached.update(reachable_components(schemas, [name for name in schemas
        if name.startswith(NATIVE_PREFIXES) and name.endswith('Request')]))
    return reached


def wire_field_name(field: ast.AnnAssign) -> str:
    assert isinstance(field.target, ast.Name)
    if isinstance(field.value, ast.Call):
        for keyword in field.value.keywords:
            if keyword.arg == 'alias':
                if not isinstance(keyword.value, ast.Constant) or not isinstance(keyword.value.value, str):
                    raise ValueError('Generated field has a nonliteral wire alias')
                return keyword.value.value
    return field.target.id


def required_declaration(field: ast.AnnAssign, annotation: str) -> str:
    """Remove only defaults; a required wire alias/description must survive."""
    assert isinstance(field.target, ast.Name)
    suffix = ''
    if isinstance(field.value, ast.Call):
        call = field.value
        function = call.func
        if not ((isinstance(function, ast.Attribute) and function.attr == 'Field')
                or (isinstance(function, ast.Name) and function.id == 'Field')):
            raise ValueError('Unsupported generated default expression for required field')
        keywords = [keyword for keyword in call.keywords if keyword.arg not in ('default', 'default_factory')]
        if keywords:
            suffix = ' = ' + ast.unparse(ast.Call(func=function, args=[], keywords=keywords))
    return f'    {field.target.id}: {annotation}{suffix}\n'


def constrained_declaration(field: ast.AnnAssign, constraints: dict) -> str:
    """Keep Fern aliases/defaults/descriptions while adding native input rules."""
    value = field.value
    if isinstance(value, ast.Call):
        if not ((isinstance(value.func, ast.Attribute) and value.func.attr == 'Field')
                or (isinstance(value.func, ast.Name) and value.func.id == 'Field')):
            raise ValueError('Unsupported generated default expression for constrained field')
        keywords = [item for item in value.keywords if item.arg not in constraints]
        arguments = value.args
    else:
        keywords = [] if value is None else [ast.keyword(arg='default', value=value)]
        arguments = []
    keywords.extend(ast.keyword(arg=key, value=ast.Constant(value=value))
                    for key, value in constraints.items())
    field.value = ast.Call(func=ast.Attribute(value=ast.Name(id='pydantic'), attr='Field'),
                           args=arguments, keywords=keywords)
    return '    ' + ast.unparse(field) + '\n'


def native_default_declaration(field: ast.AnnAssign, definition: dict, schemas: dict) -> str:
    """Restore a source default without replacing generated aliases or value types."""
    nullable = allows_null(definition, schemas)
    annotation = field.annotation
    if (not nullable and isinstance(annotation, ast.Subscript)
            and isinstance(annotation.value, ast.Attribute)
            and isinstance(annotation.value.value, ast.Name)
            and annotation.value.value.id == 'typing'
            and annotation.value.attr == 'Optional'):
        field.annotation = annotation.slice
    elif nullable:
        field.annotation = ast.parse(optional_annotation(ast.unparse(annotation)), mode='eval').body
    default = definition['default']
    if default is None and not nullable:
        raise ValueError(f'Nonnullable native default is null: {ast.unparse(field.target)}')
    value = field.value
    if isinstance(value, ast.Call):
        if not ((isinstance(value.func, ast.Attribute) and value.func.attr == 'Field')
                or (isinstance(value.func, ast.Name) and value.func.id == 'Field')):
            raise ValueError('Unsupported generated default expression for native default')
        keywords = [item for item in value.keywords if item.arg not in ('default', 'default_factory')]
    else:
        keywords = []
    keywords.insert(0, ast.keyword(arg='default', value=ast.parse(repr(default), mode='eval').body))
    field.value = ast.Call(func=ast.Attribute(value=ast.Name(id='pydantic'), attr='Field'),
                           args=[], keywords=keywords)
    return '    ' + ast.unparse(field) + '\n'


def identity_required_declaration(field: ast.AnnAssign, definition: dict, schemas: dict) -> str:
    annotation = field.annotation
    if (isinstance(annotation, ast.Subscript) and isinstance(annotation.value, ast.Attribute)
            and isinstance(annotation.value.value, ast.Name)
            and annotation.value.value.id == 'typing' and annotation.value.attr == 'Optional'):
        annotation = annotation.slice
    text = ast.unparse(annotation)
    if allows_null(definition, schemas):
        text = optional_annotation(text)
    return required_declaration(field, text)


def response_components(document: dict, schemas: dict) -> dict:
    """Every component a response can carry, directly or nested."""
    roots = []
    def references(value):
        if isinstance(value, dict):
            reference = value.get('$ref')
            if isinstance(reference, str) and reference.startswith('#/components/schemas/'):
                roots.append(reference.rsplit('/', 1)[-1])
            for child in value.values():
                references(child)
        elif isinstance(value, list):
            for child in value:
                references(child)
    for operations in document.get('paths', {}).values():
        for operation in operations.values():
            if isinstance(operation, dict):
                references(operation.get('responses', {}))
    return reachable_components(schemas, roots)


def normalize(package: Path, spec: Path, lenient_responses: bool = False) -> int:
    document = json.loads(spec.read_text())
    schemas = document['components']['schemas']
    # EpochSDK's Files client (ENG-2819): a model a response can carry keeps fields the server adds
    # later, as its response enums keep values added later. Only request-only models are closed.
    lenient = response_components(document, schemas) if lenient_responses else {}
    # Exact compilation inputs remain public after the discovery route family
    # is removed. Their closure cannot depend on a retired discovery request.
    probe_schemas = reachable_components(schemas, [name for name in ('ProbeMarketRequest', 'AssetScreen')
                                                  if name in schemas])
    request_schemas = reachable_components(schemas, [name for name in schemas
        if name.startswith(NATIVE_PREFIXES) and name.endswith('Request')])
    request_schemas.update(probe_schemas)
    identity_schemas = reachable_components(schemas, ['StockProfileIdentity']) if 'StockProfileIdentity' in schemas else {}
    reached = {**reachable_discovery_schemas(schemas), **probe_schemas, **identity_schemas}
    identity_objects = {'#/components/schemas/' + name for name, schema in identity_schemas.items()
                        if 'properties' in schema}
    identity_envelopes = {name: schema for name, schema in schemas.items()
                          if any(field.get('$ref') in identity_objects
                                 for field in schema.get('properties', {}).values())}
    # Close the outer response as declared by native OpenAPI, without extending
    # identity-only scalar, default or nullability changes to its other fields.
    closure_only = identity_envelopes.keys() - reached.keys()
    reached.update(identity_envelopes)
    # Native tagged web alternatives are inline schemas. Fern names their
    # classes from distinguishing properties; those generated names are not a
    # contract. Match the complete wire field set to the canonical alternative.
    inline_web = [(name, arm) for name, schema in reached.items()
                  if name.startswith('Web') for arm in schema.get('oneOf', [])
                  if arm.get('additionalProperties') is False and 'properties' in arm]
    by_name = {normalized(name): (name, schema)
               for name, schema in reached.items()
               if 'properties' in schema}
    # Fern sometimes clones a referenced object under ParentField (notably a
    # field named constructor). Its wire owner is still the canonical $ref;
    # derive that alias rather than maintaining another list of model names.
    for parent, schema in reached.items():
        for field, definition in schema.get('properties', {}).items():
            reference = definition.get('$ref', '').removeprefix('#/components/schemas/')
            if reference in reached and 'properties' in reached[reference]:
                by_name.setdefault(normalized(parent + field), (reference, reached[reference]))
    changed = restore_request_components(package, schemas)
    for path in sorted((package / PACKAGE / 'types').glob('*.py')):
        source = path.read_text()
        tree = ast.parse(source)
        lines = source.splitlines(keepends=True)
        replacements: list[tuple[int, int, str]] = []
        for cls in tree.body:
            if not isinstance(cls, ast.ClassDef):
                continue
            component = by_name.get(normalized(cls.name))
            if component is None:
                fields = {wire_field_name(field) for field in cls.body
                          if isinstance(field, ast.AnnAssign) and isinstance(field.target, ast.Name)
                          and field.target.id != 'model_config'}
                matches = [(name, arm) for name, arm in inline_web
                           if normalized(cls.name).startswith(normalized(name))
                           and fields == set(arm['properties'])]
                if len(matches) > 1:
                    raise ValueError(f'Ambiguous native inline web model: {cls.name}')
                component = matches[0] if matches else None
            if component is None:
                continue
            component_name, schema = component
            required = set(schema.get('required', []))
            identity_nonnullable_fields = set()
            for field in cls.body:
                if not isinstance(field, ast.AnnAssign) or not isinstance(field.target, ast.Name):
                    continue
                name = field.target.id
                wire_name = wire_field_name(field)
                old = ''.join(lines[field.lineno - 1:field.end_lineno])
                if name == 'model_config' and schema.get('additionalProperties') is False and component_name not in lenient:
                    new = old.replace('extra="allow"', 'extra="forbid"')
                    if new != old:
                        replacements.append((field.lineno - 1, field.end_lineno, new))
                else:
                    if component_name in closure_only:
                        continue
                    replacement = old
                    definition = schema.get('properties', {}).get(wire_name, {})
                    if has_string_constraints(definition, schemas):
                        # Retain current default/alias/requiredness behavior,
                        # restoring nested item constraints from native schema.
                        annotation = schema_type(definition, set(), schemas)
                        current = ast.unparse(field.annotation)
                        if wire_name not in required and current.startswith('typing.Optional['):
                            annotation = f'typing.Optional[{annotation}]'
                        if wire_name in required:
                            replacement = required_declaration(field, annotation)
                        else:
                            suffix = ' = ' + ast.unparse(field.value) if field.value is not None else ''
                            replacement = f'    {name}: {annotation}{suffix}\n'
                    elif wire_name in required and component_name in identity_schemas:
                        replacement = identity_required_declaration(field, definition, schemas)
                    elif wire_name in required and (component_name.startswith(NATIVE_PREFIXES) or component_name in request_schemas):
                        annotation = field.annotation
                        if (isinstance(annotation, ast.Subscript)
                                and isinstance(annotation.value, ast.Attribute)
                                and isinstance(annotation.value.value, ast.Name)
                                and annotation.value.value.id == 'typing'
                                and annotation.value.attr == 'Optional'):
                            inner = ast.get_source_segment(source, annotation.slice)
                            if inner is None:
                                raise ValueError(f'Cannot read generated annotation: {path}:{field.lineno}')
                            replacement = required_declaration(field, inner)
                        elif field.value is not None and 'const' in schema['properties'].get(wire_name, {}):
                            inner = ast.get_source_segment(source, annotation)
                            if inner is None:
                                raise ValueError(f'Cannot read generated annotation: {path}:{field.lineno}')
                            replacement = required_declaration(field, inner)
                    if component_name in identity_schemas:
                        definition = schema.get('properties', {}).get(wire_name, {})
                        if wire_name not in required and not allows_null(definition, schemas):
                            identity_nonnullable_fields.update({wire_name, field.target.id})
                        constraints = numeric_constraints(definition, schemas)
                        if constraints:
                            node = ast.parse(replacement.strip()).body[0]
                            replacement = constrained_declaration(node, constraints)
                    if component_name in request_schemas and COMPONENT_MARKER not in source:
                        constraints = numeric_constraints(schema['properties'].get(wire_name, {}), schemas)
                        if constraints:
                            node = ast.parse(replacement.strip()).body[0]
                            replacement = constrained_declaration(node, constraints)
                        native = primitive_schema(definition, schemas)
                        if wire_name not in required and 'default' in native:
                            node = ast.parse(replacement.strip()).body[0]
                            replacement = native_default_declaration(node, native, schemas)
                    if replacement != old:
                        replacements.append((field.lineno - 1, field.end_lineno, replacement))
            managed_guard = next((node for node in cls.body
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                and node.name == '_validate_native_identity_members'), None)
            if component_name in identity_schemas and (identity_nonnullable_fields or managed_guard):
                guard = ''
                if identity_nonnullable_fields:
                    keys = repr(tuple(sorted(identity_nonnullable_fields)))
                    guard = ("    @pydantic.model_validator(mode='before')\n    @classmethod\n"
                             "    def _validate_native_identity_members(cls, value):\n"
                             "        if isinstance(value, typing.Mapping):\n"
                             f"            for key in {keys}:\n"
                             "                if key in value and value[key] is None:\n"
                             "                    raise ValueError(f'{key} allows omission but not explicit null')\n"
                             "        return value\n")
                if managed_guard:
                    start = min([managed_guard.lineno] + [node.lineno for node in managed_guard.decorator_list]) - 1
                    previous = ''.join(lines[start:managed_guard.end_lineno])
                    if previous != guard:
                        replacements.append((start, managed_guard.end_lineno, guard))
                elif guard:
                    replacements.append((cls.end_lineno, cls.end_lineno, '\n' + guard))
        if replacements:
            for start, end, replacement in sorted(replacements, reverse=True):
                lines[start:end] = [replacement]
            output = ''.join(lines)
            ast.parse(output)
            path.write_text(output)
            changed += 1
    return changed


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--package-root', type=Path, required=True)
    parser.add_argument('--openapi', type=Path, required=True)
    parser.add_argument('--package', default=PACKAGE)
    parser.add_argument('--lenient-responses', action='store_true')
    args = parser.parse_args()
    PACKAGE = args.package
    print(json.dumps({'normalized_discovery_model_files': normalize(args.package_root, args.openapi, args.lenient_responses)}))
