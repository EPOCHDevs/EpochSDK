# Files and Space client

Platform owns the Files and Space API and its contract (EpochPlatform
`contracts/files.openapi.json`, ENG-2819). This package carries the client for it, generated from
that contract, so a Files change no longer waits for an EpochBackend release.

| Language | Import |
| -- | -- |
| Python | `from epoch_sdk.files_api import AsyncEpochFiles, EpochFiles` and `epoch_sdk.files_api.types` |
| TypeScript | `import { EpochFilesClient, EpochFiles } from "@epochdevs/epoch-sdk/files-api"` |

Methods and types keep the names of the StratifyX SDK's Files client: `user_files.list_saved_datasets`
in Python, `userFiles.listSavedDatasets` in TypeScript, `DatasetBuild`, `StructuredImportOptions`.
Moving a caller is an import swap. The one method gone is `archive_user_file`; Platform dropped that
route in ENG-2810.

Responses keep fields Platform adds later. Python models allow extra fields, and TypeScript parses
responses in passthrough mode, so a new response field never needs a lockstep client release.

## Updating

1. `python tools/sync_platform_files_contract.py --platform-openapi <EpochPlatform>/contracts/files.openapi.json --source-revision <commit>`
2. `python tools/generate_files_api.py` (needs the `fern` CLI 3.30.0 and Docker, with the generator
   images `fernapi/fern-python-sdk:4.46.6` and `fernapi/fern-typescript-node-sdk:0.51.7`)

`python tools/generate_files_api.py --check` (no Docker; CI runs it) fails if the generated code
wasn't made from the current contract. Never edit `python/epoch-sdk/src/epoch_sdk/files_api/` or
`typescript/epoch-sdk/files-api/` by hand.
