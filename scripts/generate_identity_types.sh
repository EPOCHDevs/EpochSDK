#!/bin/sh
set -eu
uv run --no-project --with datamodel-code-generator==0.92.0 --with pydantic==2.14.1 datamodel-codegen \
  --input contracts/asset-identity-v1.schema.json --input-file-type jsonschema \
  --output python/epoch-sdk/src/epoch_sdk/identity_types.py \
  --output-model-type pydantic_v2.BaseModel --base-class epoch_sdk.discovery_model.DiscoveryModel --use-standard-collections \
  --strict-types str int float bool --field-constraints --collapse-root-models --use-union-operator --target-python-version 3.12 --extra-fields forbid \
  --disable-timestamp --use-schema-description --use-default-kwarg --formatters black isort
cp contracts/asset-identity-v1.schema.json python/epoch-sdk/src/epoch_sdk/data/asset-identity.schema.json
