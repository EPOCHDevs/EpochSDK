"""Mirror Platform's source-owned saved-model contract into both installed SDKs."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
PATHS = [
    ROOT / "contracts/platform-models.openapi.json",
    ROOT / "python/epoch-sdk/src/epoch_sdk/data/platform-models.openapi.json",
    ROOT / "typescript/epoch-sdk/platform-models.openapi.json",
]
SOURCE = ROOT / "contracts/platform-models.source.json"
# Resolve Platform-owned schema references within the complete contract.
_URI = "https://epoch.trade/contracts/platform-models-v1"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--platform-openapi", type=Path)
    parser.add_argument("--source-revision")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    content = (args.platform_openapi or PATHS[0]).read_bytes()
    document = json.loads(content)
    if document.get("x-epoch-contract-owner") != "EpochPlatform":
        raise SystemExit("Expected the Platform-owned saved-model contract")
    digest = hashlib.sha256(content).hexdigest()
    if args.check:
        if any(not path.exists() or path.read_bytes() != content for path in PATHS):
            raise SystemExit("Platform saved-model contract copies have drifted")
        receipt = json.loads(SOURCE.read_text())
        if (
            receipt.get("sha256") != digest
            or receipt.get("repository") != "EPOCHDevs/EpochPlatform"
            or receipt.get("path") != "contracts/models.openapi.json"
            or not re.fullmatch(r"[0-9a-f]{40}", receipt.get("revision", ""))
        ):
            raise SystemExit("Platform saved-model source receipt has drifted")
        for name, model in (
            ("save", "SaveModelRequest"),
            ("summary", "SavedModelSummary"),
            ("page", "SavedModelPage"),
            ("facts", "SavedModelFacts"),
            ("manifest", "SavedModelManifest"),
        ):
            Draft202012Validator(
                {"$ref": f"{_URI}#/components/schemas/{model}"},
                registry=Registry().with_resource(
                    _URI,
                    Resource.from_contents(
                        {
                            "$schema": "https://json-schema.org/draft/2020-12/schema",
                            **document,
                        }
                    ),
                ),
            ).validate(
                json.loads(
                    (
                        ROOT / f"contracts/fixtures/platform-models/{name}.json"
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
                    "path": "contracts/models.openapi.json",
                    "revision": args.source_revision,
                    "sha256": digest,
                },
                indent=2,
            )
            + "\n"
        )


if __name__ == "__main__":
    main()
