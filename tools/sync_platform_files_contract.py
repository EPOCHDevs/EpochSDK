"""Mirror Platform's source-owned file contract into both installed SDKs."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
PATHS = [
    ROOT / "contracts/platform-files.openapi.json",
    ROOT / "python/epoch-sdk/src/epoch_sdk/data/platform-files.openapi.json",
    ROOT / "typescript/epoch-sdk/platform-files.openapi.json",
]
SOURCE = ROOT / "contracts/platform-files.source.json"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--platform-openapi", type=Path)
    parser.add_argument("--source-revision")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    content = (args.platform_openapi or PATHS[0]).read_bytes()
    document = json.loads(content)
    if document.get("x-epoch-contract-owner") != "EpochPlatform":
        raise SystemExit("Expected the Platform-owned file contract")
    digest = hashlib.sha256(content).hexdigest()
    if args.check:
        if any(not path.exists() or path.read_bytes() != content for path in PATHS):
            raise SystemExit("Platform file contract copies have drifted")
        receipt = json.loads(SOURCE.read_text())
        if (
            receipt.get("sha256") != digest
            or receipt.get("repository") != "EPOCHDevs/EpochPlatform"
            or receipt.get("path") != "contracts/files.openapi.json"
            or not re.fullmatch(r"[0-9a-f]{40}", receipt.get("revision", ""))
        ):
            raise SystemExit("Platform file source receipt has drifted")
        for name, model in (
            ("version", "FileVersion"),
            ("save", "FileEditRequest"),
            ("grid", "FileEditGrid"),
        ):
            Draft202012Validator(document["components"]["schemas"][model]).validate(
                json.loads(
                    (
                        ROOT / f"contracts/fixtures/platform-files/{name}.json"
                    ).read_text()
                )
            )
    else:
        if not args.source_revision or not re.fullmatch(
            r"[0-9a-f]{40}", args.source_revision
        ):
            raise SystemExit("Pass the reviewed Platform --source-revision")
        for path in PATHS:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        SOURCE.write_text(
            json.dumps(
                {
                    "repository": "EPOCHDevs/EpochPlatform",
                    "path": "contracts/files.openapi.json",
                    "revision": args.source_revision,
                    "sha256": digest,
                },
                indent=2,
            )
            + "\n"
        )


if __name__ == "__main__":
    main()
