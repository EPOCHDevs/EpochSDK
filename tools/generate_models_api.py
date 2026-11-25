"""Generate Platform-owned saved-model clients from the mirrored OpenAPI.

Uses the existing pinned Fern generators and Backend-owned normalization patches.
Run sync_platform_models_contract.py first. --check needs no Docker.
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
CONTRACT = ROOT / "contracts/platform-models.openapi.json"
CONFIG = ROOT / "fern-models"
FERN = ROOT / "build/models-generator/fern"
BUILD = ROOT / "build/fern-models"
PATCHES = ROOT / "tools/fern_patches"
PYTHON = ROOT / "python/epoch-sdk/src/epoch_sdk/models_api"
TYPESCRIPT = ROOT / "typescript/epoch-sdk/models-api"
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
                "run python tools/generate_models_api.py"
            )


def _place(source: Path, destination: Path) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination)
    (destination / STAMP).write_text(_digest() + "\n")


def _generate() -> None:
    (FERN / "openapi").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(CONFIG / "fern.config.json", FERN / "fern.config.json")
    (FERN / "generators.yml").write_text(
        (CONFIG / "generators.yml").read_text().replace("../build/fern-models", str(BUILD))
    )
    shutil.copyfile(CONTRACT, FERN / "openapi/platform-models.openapi.json")
    if BUILD.exists():
        shutil.rmtree(BUILD)
    subprocess.run(["fern", "generate", "--local", "--force", "--no-prompt"], cwd=FERN, check=True)

    # The order EpochBackend's scripts/package_sdk.py applies them in.
    stage = BUILD / "stage"
    stage.mkdir()
    shutil.move(BUILD / "python", stage / "models_api")
    typescript = BUILD / "typescript"
    python_patch = [sys.executable, "-I"]
    subprocess.run([*python_patch, str(ROOT / "tools/normalize_platform_models_clients.py"), "--package-root", str(stage),
                    "--openapi", str(CONTRACT), "--typescript", str(typescript)], check=True)
    for patch in ("lazy_imports", "record_keys", "error_bodies"):
        subprocess.run(["node", str(PATCHES / f"patch_fern_typescript_{patch}.mjs"), str(typescript)], check=True)
    def has_enum(value):
        return isinstance(value, dict) and ("enum" in value or any(has_enum(child) for child in value.values())) or isinstance(value, list) and any(has_enum(child) for child in value)
    if has_enum(json.loads(CONTRACT.read_text())["components"]["schemas"]):
        subprocess.run([*python_patch, str(PATCHES / "patch_fern_python_forward_compatible_enums.py"), str(stage),
                        "--package", "models_api"], check=True)

    _place(stage / "models_api", PYTHON)
    # Docstring examples name the package as Fern generated it; it lives inside epoch_sdk.
    for path in PYTHON.rglob("*.py"):
        text = path.read_text()
        if "from models_api import" in text:
            path.write_text(text.replace("from models_api import", "from epoch_sdk.models_api import"))

    _place(typescript, TYPESCRIPT)
    # Fern emits CommonJS; the rest of the package is ESM.
    (TYPESCRIPT / "package.json").write_text(json.dumps({"type": "commonjs"}, indent=2) + "\n")

    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONPATH": str(ROOT / "python/epoch-sdk/src")}
    subprocess.run(
        [sys.executable, "-c", "from epoch_sdk.models_api import AsyncEpochModels, EpochModels"],
        check=True,
        env=env,
    )
    subprocess.run(
        ["node", "-e", "const f = require('./models-api'); if (!f.EpochModelsClient) process.exit(1)"],
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
