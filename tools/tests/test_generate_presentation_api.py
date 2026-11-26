"""Presentation generation integrity checks without running Docker or Fern."""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location(
    "generate_presentation_api",
    Path(__file__).resolve().parents[1] / "generate_presentation_api.py",
)
generator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(generator)


class ManifestTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        root = Path(self.temporary.name)
        contract = root / "contract.json"
        contract.write_text("{}")
        (root / "generator.py").write_text("source pipeline")
        self.modules = (root / "python", root / "typescript")
        self.settings = patch.multiple(
            generator,
            ROOT=root,
            CONTRACT=contract,
            INPUTS=("generator.py",),
            PYTHON=self.modules[0],
            TYPESCRIPT=self.modules[1],
        )
        self.settings.start()
        self.addCleanup(self.settings.stop)
        for directory in self.modules:
            directory.mkdir()
            (directory / "client.txt").write_text("generated client")
            (directory / generator.STAMP).write_text(generator._digest() + "\n")
            (directory / generator.MANIFEST).write_text(
                json.dumps(generator._manifest(directory))
            )

    def test_unchanged_generated_modules_pass_with_local_bytecode(self):
        for directory in self.modules:
            cache = directory / "__pycache__"
            cache.mkdir()
            (cache / "client.pyc").write_bytes(b"local interpreter cache")
        generator._check()

    def test_modified_bytes_reject_even_with_unchanged_contract_stamp(self):
        (self.modules[0] / "client.txt").write_text("tampered generated client")
        with self.assertRaisesRegex(SystemExit, "generated file/input manifest"):
            generator._check()

    def test_missing_generated_file_rejects(self):
        (self.modules[1] / "client.txt").unlink()
        with self.assertRaisesRegex(SystemExit, "generated file/input manifest"):
            generator._check()

    def test_extra_generated_file_rejects(self):
        (self.modules[1] / "unexpected.txt").write_text("extra client")
        with self.assertRaisesRegex(SystemExit, "generated file/input manifest"):
            generator._check()

    def test_generation_input_changes_require_regeneration(self):
        (generator.ROOT / "generator.py").write_text("changed pipeline")
        with self.assertRaisesRegex(SystemExit, "generated file/input manifest"):
            generator._check()


if __name__ == "__main__":
    unittest.main()
