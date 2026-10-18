"""Snapshot the supervisor's owned interrupt wire without importing its app.

Only the named schema declarations are executed. No graph, model, Backend client,
authentication handler or application startup is imported.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictInt,
    TypeAdapter,
    field_validator,
)
from typing_extensions import TypedDict

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "contracts/supervisor-native.schema.json"
NAMES = {
    "QuestionOptionWire",
    "QuestionWire",
    "AskUserInterruptPayload",
    "UserAnswer",
    "AskUserResponse",
}


def snapshot(source_root: Path) -> dict:
    path = source_root / "agent_src/common/ask_user.py"
    raw = path.read_bytes()
    parsed = ast.parse(raw)
    classes = [
        node
        for node in parsed.body
        if isinstance(node, ast.ClassDef) and node.name in NAMES
    ]
    if {node.name for node in classes} != NAMES:
        raise ValueError(
            "The supervisor wire declarations changed; review the source contract"
        )
    namespace = {
        "__name__": "_epoch_supervisor_wire",
        "TypedDict": TypedDict,
        "Literal": Literal,
        "BaseModel": BaseModel,
        "ConfigDict": ConfigDict,
        "Field": Field,
        "StrictInt": StrictInt,
        "field_validator": field_validator,
    }
    exec(  # noqa: S102 -- Execute only the reviewed schema classes, never application startup.
        compile(
            ast.Module(body=classes, type_ignores=[]),
            str(path),
            "exec",
            dont_inherit=True,
        ),
        namespace,
    )
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "source": {
            "repository": "EPOCHDevs/EpochAI",
            "path": "agent_src/common/ask_user.py",
            "commit": subprocess.check_output(
                ["git", "-C", str(source_root), "rev-parse", "HEAD"], text=True
            ).strip(),
            "sha256": hashlib.sha256(raw).hexdigest(),
        },
        "schemas": {
            "AskUser": TypeAdapter(namespace["AskUserInterruptPayload"]).json_schema(),
            "Answers": TypeAdapter(namespace["AskUserResponse"]).json_schema(),
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--epoch-ai", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    value = json.dumps(snapshot(args.epoch_ai), indent=2) + "\n"
    if args.check:
        if OUTPUT.read_text() != value:
            raise SystemExit(
                "Supervisor wire snapshot differs from the reviewed source"
            )
    else:
        OUTPUT.write_text(value)
    print("Supervisor interrupt/answer wire agrees with its source declarations")
