"""Validate language-neutral tool transport and its source-generated catalogue."""
import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def main():
    schema = json.loads((ROOT / "contracts/agent-tools.schema.json").read_text())
    catalogue = json.loads((ROOT / "contracts/agent-tools-native.json").read_text())["catalog"]
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(catalogue)
    expected = {"inspect_source", "build_study"}
    assert catalogue["version"] == 3
    assert {tool["name"] for tool in catalogue["tools"]} == expected
    for tool in catalogue["tools"]:
        Draft202012Validator.check_schema(tool["parameters"])
        assert tool["parameters"]["additionalProperties"] is False
        assert not {"runtime", "tool_call_id", "state"} & set(tool["parameters"]["properties"])
    check = Draft202012Validator(schema)
    handle = {"workspace_id": "workspace", "run_id": "native-run", "tool_call_id": "call", "tool": "discovery"}
    check.validate(handle)
    assert not check.is_valid({**handle, "authorization": "not-a-wire-field"})
    assert not check.is_valid({**handle, "tool": "epoch-ai"})
    print("Agent tools contract valid: 2 active original schemas, closed transport and no injected fields")


if __name__ == "__main__":
    main()
