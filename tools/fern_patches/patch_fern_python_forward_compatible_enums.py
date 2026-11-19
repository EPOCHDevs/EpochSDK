#!/usr/bin/env python3
# Copied from EPOCHDevs/EpochBackend scripts/patch_fern_python_forward_compatible_enums.py at 381ca0292d (ENG-2819). The Files
# client runs the same pinned Fern generators, so it needs the same fixes. Change both copies
# together while EpochBackend still generates StratifyX.
"""Make the generated Python SDK's enums accept values added after it was built (ENG-2781).

Fern generates closed `StrEnum`s: a value Backend adds later fails pydantic validation in a
client built before the change, and the caller loses the whole response. Fern's own
`forward_compatible_python_enums` cannot be used here:

- Our unions tell their arms apart by enums (often one value each). An enum that accepts any
  value lets a body match the wrong arm.
- It stores every unknown value on one shared `_UNKNOWN` member, so two unknown values
  overwrite each other.
- It adds a required argument to every `visit()`.

This patch instead gives each enum a response can carry a `_missing_` that turns an unknown
string into a member of its own: it equals its raw string, is never any known member and is
not added to the enum. Its `visit()` raises a clear error instead of returning None.

These stay closed:
- enums only requests use: the SDK keeps rejecting a value it does not know before sending
  (owner, 14 Nov);
- enums that tell union arms apart, and single-value enums.
"""
from __future__ import annotations

import argparse
import ast
from pathlib import Path

MISSING = '''
    @classmethod
    def _missing_(cls, value: typing.Any) -> typing.Optional["{name}"]:
        # Forward compatible (ENG-2781): a value Backend added after this SDK was built
        # parses as a member of its own, so one new value cannot fail a whole response.
        # It equals its raw string and is never a known member.
        if not isinstance(value, str):
            return None
        member = str.__new__(cls, value)
        member._name_ = value
        member._value_ = value
        return member
'''
UNHANDLED = (
    '        raise ValueError(f"{type(self).__name__} has no case for {self.value!r}, '
    'a value added after this SDK was built")\n'
)


def is_str_enum(node: ast.ClassDef) -> bool:
    return any(isinstance(base, ast.Attribute) and base.attr == 'StrEnum'
               or isinstance(base, ast.Name) and base.id == 'StrEnum' for base in node.bases)


def members(node: ast.ClassDef) -> list[str]:
    return [statement.targets[0].id for statement in node.body
            if isinstance(statement, ast.Assign) and len(statement.targets) == 1
            and isinstance(statement.targets[0], ast.Name)
            and isinstance(statement.value, ast.Constant) and isinstance(statement.value.value, str)]


def names_in(annotation: ast.AST) -> set[str]:
    found = set()
    for node in ast.walk(annotation):
        if isinstance(node, ast.Name):
            found.add(node.id)
        elif isinstance(node, ast.Attribute):
            found.add(node.attr)
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            found.add(node.value)  # string forward references
    return found


def union_arms(node: ast.AST) -> list[str] | None:
    if (isinstance(node, ast.Subscript) and isinstance(node.value, ast.Attribute)
            and node.value.attr == 'Union'):
        items = node.slice.elts if isinstance(node.slice, ast.Tuple) else [node.slice]
        return [item.id for item in items if isinstance(item, ast.Name)]
    return None


def analyse(package: Path):
    enums: dict[str, tuple[Path, ast.ClassDef]] = {}
    models: dict[str, dict[str, set[str]]] = {}
    unions: list[list[str]] = []
    references: dict[str, set[str]] = {}  # every type name a model or alias refers to
    responses: set[str] = set()  # types a client method returns or an error carries
    for path in sorted(package.rglob('*.py')):
        tree = ast.parse(path.read_text())
        for node in tree.body:
            if isinstance(node, ast.ClassDef) and is_str_enum(node):
                enums[node.name] = (path, node)
            elif isinstance(node, ast.ClassDef):
                models[node.name] = {statement.target.id: names_in(statement.annotation)
                                     for statement in node.body
                                     if isinstance(statement, ast.AnnAssign)
                                     and isinstance(statement.target, ast.Name)}
                references.setdefault(node.name, set()).update(*models[node.name].values())
            elif isinstance(node, (ast.Assign, ast.AnnAssign)) and node.value is not None:
                arms = union_arms(node.value)
                if arms:
                    unions.append(arms)
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                for target in targets:
                    if isinstance(target, ast.Name):
                        references.setdefault(target.id, set()).update(names_in(node.value))
        is_client = path.name in ('client.py', 'raw_client.py')
        is_error = 'errors' in path.relative_to(package).parts
        if is_client or is_error:
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if node.returns is not None:
                        responses.update(names_in(node.returns))
                    if is_error:  # an error's body is a response too
                        for argument in node.args.args + node.args.kwonlyargs:
                            if argument.annotation is not None:
                                responses.update(names_in(argument.annotation))
    return enums, models, unions, references, responses


def reachable(roots: set[str], references: dict[str, set[str]]) -> set[str]:
    seen, pending = set(), list(roots)
    while pending:
        name = pending.pop()
        if name in seen:
            continue
        seen.add(name)
        pending.extend(references.get(name, ()))
    return seen


def discriminators(enums, models, unions) -> set[str]:
    """Enums whose type differs between union arms for the same field: they pick the arm."""
    closed: set[str] = set()
    for arms in unions:
        arms = [models[arm] for arm in arms if arm in models]
        for field in {field for arm in arms for field in arm}:
            per_arm = [frozenset(arm[field] & enums.keys()) for arm in arms if field in arm]
            if len(per_arm) > 1 and len(set(per_arm)) > 1:
                closed.update(*per_arm)
    return closed


def patch(path: Path, node: ast.ClassDef) -> None:
    lines = path.read_text().splitlines(keepends=True)
    visit = next((statement for statement in node.body
                  if isinstance(statement, ast.FunctionDef) and statement.name == 'visit'), None)
    if visit is None:
        raise SystemExit(f'{path}: enum {node.name} has no generated visit()')
    if any(isinstance(statement, ast.FunctionDef) and statement.name == '_missing_'
           for statement in node.body):
        raise SystemExit(f'{path}: enum {node.name} already defines _missing_')
    # Bottom-up, so earlier line numbers stay valid.
    lines.insert(visit.end_lineno, UNHANDLED)
    lines.insert(visit.lineno - 1 - len(visit.decorator_list), MISSING.format(name=node.name) + '\n')
    path.write_text(''.join(lines))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('package_root', type=Path, help='Directory containing the generated package')
    parser.add_argument('--package', default='stratifyx', help='The generated package directory name')
    args = parser.parse_args()
    package = args.package_root / args.package
    enums, models, unions, references, responses = analyse(package)
    if not responses:
        raise SystemExit('No client response types found; the generated SDK changed shape')
    in_responses = reachable(responses, references)
    closed = discriminators(enums, models, unions)
    patched = request_only = 0
    for name, (path, node) in sorted(enums.items()):
        if name in closed or len(members(node)) < 2:
            continue
        if name not in in_responses:
            request_only += 1
            continue
        patch(path, node)
        patched += 1
    if not patched:
        raise SystemExit('No enum was made forward compatible; the generated SDK changed shape')
    print(f'Forward-compatible enums: {patched}; closed: {request_only} request-only, '
          f'{len(enums) - patched - request_only} union discriminators or single value')


if __name__ == '__main__':
    main()
