"""Generate Platform-owned presentation delivery clients from the mirrored OpenAPI.

Uses the existing pinned Fern generators and Backend-owned normalization patches.
Run sync_platform_presentations_contract.py first. --check needs no Docker.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contracts/platform-presentations.openapi.json"
CONFIG = ROOT / "fern-presentations"
FERN = ROOT / "build/presentations-generator/fern"
BUILD = ROOT / "build/fern-presentations"
PATCHES = ROOT / "tools/fern_patches"
PYTHON = ROOT / "python/epoch-sdk/src/epoch_sdk/presentation_api"
TYPESCRIPT = ROOT / "typescript/epoch-sdk/presentation-api"
STAMP = ".contract-sha256"
MANIFEST = ".generated-files.json"
INPUTS = (
    "tools/generate_presentation_api.py",
    "tools/normalize_platform_presentation_clients.py",
    "fern-presentations/fern.config.json",
    "fern-presentations/generators.yml",
    "tools/fern_patches/normalize_discovery_sdk_contracts.py",
    "tools/fern_patches/normalize_closed_typescript_requests.py",
    "tools/fern_patches/patch_fern_python_forward_compatible_enums.py",
    "tools/fern_patches/patch_fern_typescript_lazy_imports.mjs",
    "tools/fern_patches/patch_fern_typescript_record_keys.mjs",
    "tools/fern_patches/patch_fern_typescript_error_bodies.mjs",
)


def _digest() -> str:
    return hashlib.sha256(CONTRACT.read_bytes()).hexdigest()


def _manifest(directory: Path) -> dict:
    """Bind every generated file to the source contract and generation inputs."""
    return {
        "schema_version": 1,
        "contract_sha256": _digest(),
        "generation_inputs": {
            name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            for name in INPUTS
        },
        "generated_files": {
            path.relative_to(directory).as_posix(): hashlib.sha256(
                path.read_bytes()
            ).hexdigest()
            for path in sorted(directory.rglob("*"))
            if path.is_file()
            and path.name not in {STAMP, MANIFEST}
            and "__pycache__" not in path.parts
            and path.suffix != ".pyc"
        },
    }


def _check() -> None:
    digest = _digest()
    for directory in (PYTHON, TYPESCRIPT):
        stamp = directory / STAMP
        if not stamp.exists() or stamp.read_text().strip() != digest:
            raise SystemExit(
                f"{directory.relative_to(ROOT)} was not generated from the current contract; "
                "run python tools/generate_presentation_api.py"
            )
        manifest = directory / MANIFEST
        if not manifest.exists() or json.loads(manifest.read_text()) != _manifest(
            directory
        ):
            raise SystemExit(
                f"{directory.relative_to(ROOT)} differs from its generated file/input manifest; "
                "run python tools/generate_presentation_api.py"
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
        (CONFIG / "generators.yml")
        .read_text()
        .replace("../build/fern-presentations", str(BUILD))
    )
    shutil.copyfile(CONTRACT, FERN / "openapi/platform-presentations.openapi.json")
    if BUILD.exists():
        shutil.rmtree(BUILD)
    subprocess.run(
        ["fern", "generate", "--local", "--force", "--no-prompt"], cwd=FERN, check=True
    )

    # The order EpochBackend's scripts/package_sdk.py applies them in.
    stage = BUILD / "stage"
    stage.mkdir()
    shutil.move(BUILD / "python", stage / "presentation_api")
    typescript = BUILD / "typescript"
    python_patch = [sys.executable, "-I"]
    subprocess.run(
        [
            *python_patch,
            str(ROOT / "tools/normalize_platform_presentation_clients.py"),
            "--package-root",
            str(stage),
            "--openapi",
            str(CONTRACT),
            "--typescript",
            str(typescript),
        ],
        check=True,
    )
    for patch in ("lazy_imports", "record_keys", "error_bodies"):
        subprocess.run(
            [
                "node",
                str(PATCHES / f"patch_fern_typescript_{patch}.mjs"),
                str(typescript),
            ],
            check=True,
        )
    # The native patch deliberately fails when nothing was widened. Presentation has
    # source/retention discriminators, which must stay closed; use that same source
    # analysis to invoke it only for response-reachable, non-discriminator enums.
    spec = importlib.util.spec_from_file_location(
        "presentation_enum_analysis",
        PATCHES / "patch_fern_python_forward_compatible_enums.py",
    )
    enum_patch = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(enum_patch)
    enums, models, unions, references, responses = enum_patch.analyse(
        stage / "presentation_api"
    )
    if not responses:
        raise ValueError("No model response types found in the generated client")
    reachable = enum_patch.reachable(responses, references)
    closed = enum_patch.discriminators(enums, models, unions)
    if any(
        name in reachable and name not in closed and len(enum_patch.members(node)) >= 2
        for name, (_, node) in enums.items()
    ):
        subprocess.run(
            [
                *python_patch,
                str(PATCHES / "patch_fern_python_forward_compatible_enums.py"),
                str(stage),
                "--package",
                "presentation_api",
            ],
            check=True,
        )

    _place(stage / "presentation_api", PYTHON)
    # Docstring examples name the package as Fern generated it; it lives inside epoch_sdk.
    for path in PYTHON.rglob("*.py"):
        text = path.read_text()
        if "from presentation_api import" in text:
            path.write_text(
                text.replace(
                    "from presentation_api import",
                    "from epoch_sdk.presentation_api import",
                )
            )

    _place(typescript, TYPESCRIPT)
    # Fern emits CommonJS; the rest of the package is ESM.
    (TYPESCRIPT / "package.json").write_text(
        json.dumps({"type": "commonjs"}, indent=2) + "\n"
    )

    env = {
        **os.environ,
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONPATH": str(ROOT / "python/epoch-sdk/src"),
    }
    subprocess.run(
        [
            sys.executable,
            "-c",
            "from epoch_sdk.presentation_api import AsyncEpochPresentations, EpochPresentations",
        ],
        check=True,
        env=env,
    )
    subprocess.run(
        [
            "node",
            "-e",
            "const f = require('./presentation-api'); if (!f.EpochPresentationsClient) process.exit(1)",
        ],
        cwd=ROOT / "typescript/epoch-sdk",
        check=True,
    )
    for directory in (PYTHON, TYPESCRIPT):
        (directory / MANIFEST).write_text(
            json.dumps(_manifest(directory), indent=2) + "\n"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--check", action="store_true")
    if parser.parse_args().check:
        _check()
    else:
        _generate()
        _check()


if __name__ == "__main__":
    main()
