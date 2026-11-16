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
from typing import Literal, NotRequired

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
# Each source file and the declarations it owns. The interrupt's wire moved to the presentation
# module; the answer models stayed with the ask_user tool.
SOURCES = {
    "agent_src/presentation/questions.py": [
        "QuestionOptionWire",
        "QuestionWire",
        "AskUserPresentationWire",
        "AskUserInterruptPayload",
    ],
    "agent_src/common/ask_user.py": ["UserAnswer", "AskUserResponse"],
}


def snapshot(source_root: Path) -> dict:
    namespace = {
        "__name__": "_epoch_supervisor_wire",
        "TypedDict": TypedDict,
        "NotRequired": NotRequired,
        "Literal": Literal,
        "BaseModel": BaseModel,
        "ConfigDict": ConfigDict,
        "Field": Field,
        "StrictInt": StrictInt,
        "field_validator": field_validator,
    }
    sources = []
    for relative, names in SOURCES.items():
        path = source_root / relative
        raw = path.read_bytes()
        by_name = {
            node.name: node
            for node in ast.parse(raw).body
            if isinstance(node, ast.ClassDef) and node.name in names
        }
        if set(by_name) != set(names):
            raise ValueError(
                f"The supervisor wire declarations in {relative} changed; review the source contract"
            )
        exec(  # noqa: S102 -- Execute only the reviewed schema classes, never application startup.
            compile(
                ast.Module(body=[by_name[name] for name in names], type_ignores=[]),
                str(path),
                "exec",
                dont_inherit=True,
            ),
            namespace,
        )
        sources.append({"path": relative, "sha256": hashlib.sha256(raw).hexdigest()})
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "source": {
            "repository": "EPOCHDevs/EpochAI",
            "commit": subprocess.check_output(
                ["git", "-C", str(source_root), "rev-parse", "HEAD"], text=True
            ).strip(),
            "files": sources,
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
