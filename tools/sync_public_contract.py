"""Copy the public v1 OpenAPI document that EpochAI generates from its routes.

EpochAI owns the v1 server, so its routes and models are the source:
  python tools/export_public_api.py   (in EpochAI)
  python tools/sync_public_contract.py --epochai-openapi ../EpochAI/docs/public-api/openapi.json
Use --check to verify the copy. Do not edit contracts/public-v1.openapi.json by hand.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "contracts/public-v1.openapi.json"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--epochai-openapi", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    source = args.epochai_openapi.read_text()
    json.loads(source)
    if args.check:
        if OUTPUT.read_text() != source:
            raise SystemExit("contracts/public-v1.openapi.json differs from EpochAI's export; sync it")
        print("Public v1 contract matches EpochAI's export")
    else:
        OUTPUT.write_text(source)
        print(f"wrote {OUTPUT.relative_to(ROOT)}")
