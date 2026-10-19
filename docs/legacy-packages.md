# Historical package snapshots

These are historical repository instructions and snapshots. New Epoch SDK
clients consume the versioned StratifyX packages produced by EpochBackend;
the old sync script is not the new integration-client build path.

`python/epoch-protos/` and `typescript/epoch-protos/` are discarded legacy
artifacts. They are not dependencies or a source for the current shared contract,
SDK or MCP. Their installation instructions and old sync steps have been removed;
the folders remain only as historical material.

# Epoch SDK

Public SDKs and libraries for the Epoch platform.

## Installation

### Python

```bash
# StratifyX SDK
pip install git+https://github.com/EPOCHDevs/EpochSDK.git#subdirectory=python/stratifyx

```

### TypeScript/JavaScript

```bash
# StratifyX SDK
npm install git+https://github.com/EPOCHDevs/EpochSDK.git#subdirectory=typescript/stratifyx

# Tree-sitter grammar
npm install git+https://github.com/EPOCHDevs/EpochSDK.git#subdirectory=typescript/tree-sitter-epochscript

# Lezer grammar (CodeMirror 6)
npm install git+https://github.com/EPOCHDevs/EpochSDK.git#subdirectory=typescript/lezer-epochscript
```

### Local Development (linking)

For local development, link directly to the package folders:

```bash
# Python - install in editable mode
pip install -e /home/ubuntu/EpochSDK/python/stratifyx

# npm - use file: protocol
npm install file:/home/ubuntu/EpochSDK/typescript/stratifyx
```

## Packages

### Python

| Package | Description |
|---------|-------------|
| `stratifyx` | StratifyX Python SDK |

### TypeScript

| Package | Description |
|---------|-------------|
| `stratifyx` | StratifyX TypeScript SDK |
| `tree-sitter-epochscript` | Tree-sitter grammar for EpochScript |
| `lezer-epochscript` | Lezer grammar for CodeMirror 6 |

## Syncing from EpochBackend

To update packages from the source repository:

```bash
./sync-from-backend.sh
```
