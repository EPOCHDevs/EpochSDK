"""Verify the closed SDK projection against EpochAI's source-owned review schema."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Literal, TypedDict

from epoch_sdk.dataset_reviews import (
    DatasetWorkflowProgress,
    interrupt_adapter,
    response_adapter,
)
from pydantic.json_schema import JsonSchemaValue


class ReviewContract(TypedDict):
    version: Literal[1]
    # JSON Schema keywords and schema-defined properties are intentionally open.
    interrupt: JsonSchemaValue
    response: JsonSchemaValue
    progress: JsonSchemaValue


def projection() -> ReviewContract:
    return {
        "version": 1,
        "interrupt": interrupt_adapter.json_schema(),
        "response": response_adapter.json_schema(),
        "progress": DatasetWorkflowProgress.model_json_schema(),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--epochai-schema", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    source = json.loads(args.epochai_schema.read_text())
    if projection() != source:
        raise SystemExit(
            "Dataset review SDK projection differs from EpochAI's source-owned schema"
        )
    root = Path(__file__).resolve().parents[1]
    paths = [
        root / "contracts/dataset-review.schema.json",
        root / "typescript/epoch-sdk/dataset-review.schema.json",
    ]
    encoded = json.dumps(source, indent=2, sort_keys=True) + "\n"
    for path in paths:
        if args.check:
            if not path.exists() or path.read_text() != encoded:
                raise SystemExit(f"Recorded dataset review schema is stale: {path}")
        else:
            path.write_text(encoded)
    print("Dataset review schema agrees with EpochAI and the SDK models")
