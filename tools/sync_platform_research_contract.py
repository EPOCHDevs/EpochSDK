"""Copy Platform's authoritative research lifecycle contract into the SDK."""
import argparse
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--platform-openapi', type=Path, required=True)
parser.add_argument('--check', action='store_true')
args = parser.parse_args()
source = args.platform_openapi.read_text()
if json.loads(source).get('x-epoch-contract-owner') != 'EpochPlatform':
    raise SystemExit('Research lifecycle contract must be owned by EpochPlatform')
targets = [root / 'contracts/platform-research.openapi.json', root / 'typescript/epoch-sdk/platform-research.openapi.json']
if args.check:
    if any(target.read_text() != source for target in targets):
        raise SystemExit('Platform research lifecycle contract differs; sync it')
else:
    for target in targets: target.write_text(source)
