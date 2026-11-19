"""Generate the Files and Space clients from Platform's contract (ENG-2819).

Platform owns the Files and Space contract; `tools/sync_platform_files_contract.py` copies it to
`contracts/platform-files.openapi.json`. This runs Fern (`fern/generators.yml`, the generator
versions EpochBackend's StratifyX SDK uses) and places the output in both packages:

  python/epoch-sdk/src/epoch_sdk/files_api/   (import epoch_sdk.files_api)
  typescript/epoch-sdk/files-api/             (import "@epochdevs/epoch-sdk/files-api")

Method and type names match the StratifyX SDK's Files client (`user_files.list_saved_datasets`,
`userFiles.listSavedDatasets`, `DatasetBuild`), so moving a client is an import swap.

  python tools/generate_files_api.py           # needs the fern CLI and Docker
  python tools/generate_files_api.py --check   # no Docker: the output matches the contract
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contracts/platform-files.openapi.json"
FERN = ROOT / "fern"
BUILD = ROOT / "build/fern-files"
PYTHON = ROOT / "python/epoch-sdk/src/epoch_sdk/files_api"
TYPESCRIPT = ROOT / "typescript/epoch-sdk/files-api"
STAMP = ".contract-sha256"


def _digest() -> str:
    return hashlib.sha256(CONTRACT.read_bytes()).hexdigest()


def _check() -> None:
    digest = _digest()
    for directory in (PYTHON, TYPESCRIPT):
        stamp = directory / STAMP
        if not stamp.exists() or stamp.read_text().strip() != digest:
            raise SystemExit(
                f"{directory.relative_to(ROOT)} was not generated from the current contract; "
                "run python tools/generate_files_api.py"
            )


def _place(source: Path, destination: Path) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination)
    (destination / STAMP).write_text(_digest() + "\n")


def _generate() -> None:
    (FERN / "openapi").mkdir(exist_ok=True)
    shutil.copyfile(CONTRACT, FERN / "openapi/platform-files.openapi.json")
    if BUILD.exists():
        shutil.rmtree(BUILD)
    subprocess.run(["fern", "generate", "--local", "--force"], cwd=FERN, check=True)

    _place(BUILD / "python", PYTHON)
    # Docstring examples name the package as Fern generated it; it lives inside epoch_sdk.
    for path in PYTHON.rglob("*.py"):
        text = path.read_text()
        if "from files_api import" in text:
            path.write_text(text.replace("from files_api import", "from epoch_sdk.files_api import"))

    _place(BUILD / "typescript", TYPESCRIPT)
    # Fern emits CommonJS; the rest of the package is ESM.
    (TYPESCRIPT / "package.json").write_text(json.dumps({"type": "commonjs"}, indent=2) + "\n")

    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONPATH": str(ROOT / "python/epoch-sdk/src")}
    subprocess.run(
        [sys.executable, "-c", "from epoch_sdk.files_api import AsyncEpochFiles, EpochFiles"],
        check=True,
        env=env,
    )
    subprocess.run(
        ["node", "-e", "const f = require('./files-api'); if (!f.EpochFilesClient) process.exit(1)"],
        cwd=ROOT / "typescript/epoch-sdk",
        check=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true")
    if parser.parse_args().check:
        _check()
    else:
        _generate()
        _check()


if __name__ == "__main__":
    main()
