import json
from pathlib import Path

from jsonschema import Draft7Validator

ROOT = Path(__file__).resolve().parents[3]


def test_identity_schema_copies_and_native_fixture_shapes():
    source = (ROOT / "contracts/asset-identity-v1.schema.json").read_bytes()
    assert (ROOT / "typescript/epoch-sdk/asset-identity.schema.json").read_bytes() == source
    assert (
        ROOT / "python/epoch-sdk/src/epoch_sdk/data/asset-identity.schema.json"
    ).read_bytes() == source
    schema = json.loads(source)
    Draft7Validator.check_schema(schema)
    fixture_root = ROOT / "contracts/fixtures/native-identity"
    fixtures = json.loads((fixture_root / "provenance.json").read_text())
    validator = Draft7Validator(
        {"$ref": "#/definitions/AssetSpecification", "definitions": schema["definitions"]}
    )
    for name in fixtures["files"]:
        validator.validate(json.loads((fixture_root / name).read_text()))
    shares = schema["definitions"]["AssetSpecification"]["properties"]["ipo_shares"]
    assert shares["minimum"] == -(2**63)
    assert shares["maximum"] == 2**63 - 1
