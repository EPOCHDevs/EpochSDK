# Epoch SDK

Public SDKs and libraries for the Epoch platform.

## Installation

### Python

```bash
# StratifyX SDK
pip install git+https://github.com/EPOCHDevs/EpochSDK.git#subdirectory=python/stratifyx

# Epoch Protos
pip install git+https://github.com/EPOCHDevs/EpochSDK.git#subdirectory=python/epoch-protos
```

### TypeScript/JavaScript

```bash
# StratifyX SDK
npm install git+https://github.com/EPOCHDevs/EpochSDK.git#subdirectory=typescript/stratifyx

# Epoch Protos
npm install git+https://github.com/EPOCHDevs/EpochSDK.git#subdirectory=typescript/epoch-protos

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
pip install -e /home/ubuntu/EpochSDK/python/epoch-protos

# npm - use file: protocol
npm install file:/home/ubuntu/EpochSDK/typescript/stratifyx
npm install file:/home/ubuntu/EpochSDK/typescript/epoch-protos
```

## Packages

### Python

| Package | Description |
|---------|-------------|
| `stratifyx` | StratifyX Python SDK |
| `epoch-protos` | Protocol Buffer definitions |

### TypeScript

| Package | Description |
|---------|-------------|
| `stratifyx` | StratifyX TypeScript SDK |
| `epoch-protos` | Protocol Buffer definitions |
| `tree-sitter-epochscript` | Tree-sitter grammar for EpochScript |
| `lezer-epochscript` | Lezer grammar for CodeMirror 6 |

## Syncing from EpochBackend

To update packages from the source repository:

```bash
./sync-from-backend.sh
```
