"""Use the established source-schema normalizers for Platform presentation clients.

Request closure/constraints resolve against the complete mirrored OpenAPI, so
shared response/request components need no manually maintained field roster.
"""

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
    roots, operations = set(), {}
    for item in document["paths"].values():
        for operation in item.values():
            if not isinstance(operation, dict):
                continue
            ref = (
                operation.get("requestBody", {})
                .get("content", {})
                .get("application/json", {})
                .get("schema", {})
                .get("$ref")
            )
            if ref:
                name = ref.removeprefix("#/components/schemas/")
                roots.add(name)
                method = re.sub(
                    r"(?<!^)(?=[A-Z])", "_", operation["operationId"]
                ).lower()
                operations[method] = name
    if not roots:
        raise ValueError("The source contract has no named presentation request")
    patches = Path(__file__).parent / "fern_patches"
    python = load(
        "source_owned_presentations", patches / "normalize_discovery_sdk_contracts.py"
    )
    python.PACKAGE = "presentation_api"
    python.NATIVE_PREFIXES = tuple(sorted(roots))
    python.normalize(package_root, contract, lenient_responses=True)
    package = package_root / "presentation_api"
    # Fern flattens endpoint request bodies. Validate the source-owned snapshot
    # before HTTP on both actual raw request paths, as the Models client does.
    client = package / "raw_client.py"
    source = client.read_text()
    lines, offsets = source.splitlines(keepends=True), [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))
    edits = []
    for method in ast.walk(ast.parse(source)):
        if (
            not isinstance(method, (ast.FunctionDef, ast.AsyncFunctionDef))
            or method.name not in operations
        ):
            continue
        bodies = [
            keyword.value
            for node in ast.walk(method)
            if isinstance(node, ast.Call)
            for keyword in node.keywords
            if keyword.arg == "json"
        ]
        if len(bodies) != 1 or not isinstance(bodies[0], ast.Dict):
            raise ValueError(
                "Cannot identify the generated flattened request: " + method.name
            )
        body = bodies[0]
        start, end = (
            offsets[body.lineno - 1] + body.col_offset,
            offsets[body.end_lineno - 1] + body.end_col_offset,
        )
        edits.append(
            (
                start,
                end,
                f'{operations[method.name]}.model_validate({{key: value for key, value in ({source[start:end]}).items() if value is not OMIT}}).model_dump(mode="json", by_alias=True, exclude_unset=True)',
            )
        )
    if len(edits) != len(operations) * 2:
        raise ValueError("Both sync and async request paths must be normalized")
    for start, end, value in sorted(edits, reverse=True):
        source = source[:start] + value + source[end:]
    client.write_text("from .types import " + ", ".join(sorted(roots)) + "\n" + source)

    (
        package / "core/platform_request_schema.py"
    ).write_text('''"""Source-owned outbound validation, without a second model/route schema."""
import json
from functools import lru_cache
from importlib.resources import files
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
URI = "https://epoch.trade/contracts/platform-presentations-v2"
@lru_cache
def validator(name):
    document = json.loads(files("epoch_sdk").joinpath("data/platform-presentations.openapi.json").read_text())
    resource = Resource.from_contents({**document, "$schema":"https://json-schema.org/draft/2020-12/schema"})
    return Draft202012Validator({"$ref":URI+"#/components/schemas/"+name}, registry=Registry().with_resource(URI,resource))
def validate_request(name, value):
    error = next(validator(name).iter_errors(value), None)
    if error is not None:
        raise ValueError("Platform presentation request fails source constraint: " + str(error.validator))
''')
    # Restore source-requiredness without stripping nullability. This is narrow
    # to this generated module; raw inner documents are ordinary strings.
    schemas = document["components"]["schemas"]
    for path in (package / "types").glob("*.py"):
        source = path.read_text()
        tree = ast.parse(source)
        lines, offsets = source.splitlines(keepends=True), [0]
        for line in lines:
            offsets.append(offsets[-1] + len(line))
        edits = []
        for cls in tree.body:
            if not isinstance(cls, ast.ClassDef) or cls.name not in schemas:
                continue
            schema = schemas[cls.name]
            for field in cls.body:
                if not isinstance(field, ast.AnnAssign) or not isinstance(
                    field.target, ast.Name
                ):
                    continue
                wire = python.wire_field_name(field)
                if wire not in schema.get("required", []):
                    continue
                definition = schema.get("properties", {}).get(wire, {})
                start = offsets[field.lineno - 1] + field.col_offset
                end = offsets[field.end_lineno - 1] + field.end_col_offset
                annotation = ast.get_source_segment(source, field.annotation)
                if "const" in definition:
                    annotation = "typing.Literal[" + repr(definition["const"]) + "]"
                if field.value is None:
                    if "const" in definition:
                        edits.append((start, end, f"{field.target.id}: {annotation}"))
                    continue
                if isinstance(field.value, ast.Call):
                    default = field.value
                    default.args = [ast.Constant(value=Ellipsis)]
                    default.keywords = [
                        k
                        for k in default.keywords
                        if k.arg not in {"default", "default_factory"}
                    ]
                    value = ast.unparse(default)
                else:
                    value = "pydantic.Field(...)"
                edits.append((start, end, f"{field.target.id}: {annotation} = {value}"))
            if cls.name in roots:
                at = offsets[cls.end_lineno - 1] + cls.end_col_offset
                edits.append(
                    (
                        at,
                        at,
                        f"""

    @pydantic.model_validator(mode="after")
    def _validate_platform_source_request(self):
        from ..core.platform_request_schema import validate_request
        validate_request({cls.name!r}, self.model_dump(mode="json", by_alias=True, exclude_unset=True))
        return self""",
                    )
                )
        for start, end, value in sorted(edits, reverse=True):
            source = source[:start] + value + source[end:]
        if edits:
            ast.parse(source)
            path.write_text(source)

    ts = load(
        "source_owned_presentation_typescript",
        patches / "normalize_closed_typescript_requests.py",
    )
    ts.apply(typescript, contract)
    (typescript / "core/sourceOwnedRequestSchema.js").write_text(ts.HELPER)
    (typescript / "core/platformRequestSchema.js").write_text(""""use strict";
const Ajv2020 = require("ajv/dist/2020").default;
const {getSchemaUtils} = require("./schemas/builders/schema-utils");
const {getObjectLikeUtils} = require("./schemas/builders/object-like");
const {getObjectUtils} = require("./schemas/builders/object/object");
const document = require("../../platform-presentations.openapi.json");
const uri = "https://epoch.trade/contracts/platform-presentations-v2";
const ajv = new Ajv2020({allErrors:true,strict:true});
// OpenAPI's named schema container is registry metadata, not a validation
// keyword. Keep the original local pointers; only referenced schemas compile.
ajv.addKeyword({keyword:"components",schemaType:"object",valid:true});
ajv.addSchema({$schema:"https://json-schema.org/draft/2020-12/schema",components:document.components},uri);
exports.platformRequestSchema = function(schema, name) {
    const validate = ajv.compile({$ref:uri+"#/components/schemas/"+name});
    const exact = {...schema,json:(value,options)=>{
        const result=schema.json(value,options);
        if (!result.ok || validate(result.value)) return result;
        return {ok:false,errors:validate.errors.map(error=>({path:[...(options?.breadcrumbsPrefix??[]),...error.instancePath.split("/").filter(Boolean)],message:`Platform request fails ${error.keyword}`}))};
    }};
    return Object.assign(exact,getSchemaUtils(exact),getObjectLikeUtils(exact),getObjectUtils(exact));
};
""")
    for name in sorted(roots):
        candidates = list((typescript / "serialization").rglob(name + ".js"))
        if len(candidates) != 1:
            raise ValueError(
                "Cannot identify the generated source request serializer: " + name
            )
        path = candidates[0]
        helper = Path(
            os.path.relpath(typescript / "core/sourceOwnedRequestSchema", path.parent)
        ).as_posix()
        if not helper.startswith("."):
            helper = "./" + helper
        with path.open("a") as stream:
            stream.write(
                f"\nexports.{name}=require({json.dumps(helper)}).sourceOwnedClosedRequest(exports.{name},[],true,true);\n"
            )
            stream.write(
                f"exports.{name}=require({json.dumps(helper.replace('sourceOwnedRequestSchema', 'platformRequestSchema'))}).platformRequestSchema(exports.{name},{json.dumps(name)});\n"
            )

    # Fern's primitive number schema widens JSON Schema `const` to number.
    # Restore only actual emitted control fields from source const values;
    # discriminator payload bases intentionally omit their union's state field.
    (typescript / "core/sourceOwnedConst.js").write_text(""""use strict";
const {getSchemaUtils}=require("./schemas/builders/schema-utils");
exports.sourceOwnedConst=function(schema,expected){
    const check=(direction,value,options)=>value===expected?schema[direction](value,options):
        {ok:false,errors:[{path:options?.breadcrumbsPrefix??[],message:"Value differs from source constant"}]};
    const exact={...schema,parse:(value,options)=>check("parse",value,options),json:(value,options)=>check("json",value,options)};
    return Object.assign(exact,getSchemaUtils(exact));
};
""")
    normalized = lambda name: re.sub(r"[^a-z0-9]", "", name.lower())
    for name, schema in schemas.items():
        for wire, definition in schema.get("properties", {}).items():
            if "const" not in definition:
                continue
            literal = json.dumps(definition["const"])
            alias = None
            for directory in (
                typescript / "api/types",
                typescript / "serialization/types",
            ):
                path = directory / (name + ".d.ts")
                source = path.read_text()
                pattern = re.compile(r"(?m)^(\s+)([A-Za-z_$][\w$]*)(\??): ([^;]+);")

                def replace(match, wire=wire, directory=directory, literal=literal):
                    nonlocal alias
                    if normalized(match[2]) != normalized(wire):
                        return match[0]
                    if directory.name == "types" and directory.parent.name == "api":
                        alias = match[2]
                    return f"{match[1]}{match[2]}{match[3]}: {literal};"

                path.write_text(pattern.sub(replace, source))
            if alias is None:
                continue
            path = typescript / "serialization/types" / (name + ".js")
            source = path.read_text()
            expression = re.compile(r"(?m)^(\s+" + re.escape(alias) + r": )(.*)$")
            helper = "../../core/sourceOwnedConst"

            def restore(match, helper=helper, literal=literal):
                primitive = re.compile(
                    r"core\.serialization\.(?:number|string|boolean)\(\)"
                )
                return match[1] + primitive.sub(
                    lambda m: (
                        f"require({json.dumps(helper)}).sourceOwnedConst({m[0]},{literal})"
                    ),
                    match[2],
                )

            path.write_text(expression.sub(restore, source))
    if any(
        schema.get("discriminator") and schema.get("oneOf")
        for schema in schemas.values()
    ):
        # Forward-compatible object fields are independent of finite union
        # discriminators. Do not claim a closed TS union for an unknown state.
        path = typescript / "Client.js"
        path.write_text(
            path.read_text().replace(
                "allowUnrecognizedUnionMembers: true",
                "allowUnrecognizedUnionMembers: false",
            )
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-root", type=Path, required=True)
    parser.add_argument("--typescript", type=Path, required=True)
    parser.add_argument("--openapi", type=Path, required=True)
    args = parser.parse_args()
    normalize(args.package_root, args.typescript, args.openapi)
