#!/bin/bash
# Sync SDKs from EpochBackend to EpochSDK
# Run this script to update the SDK copies

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="/home/ubuntu/EpochBackend"

echo "Syncing SDKs from EpochBackend..."

# Python packages
echo ""
echo "=== Python Packages ==="

echo "  Syncing stratifyx..."
rm -rf "$SCRIPT_DIR/python/stratifyx"
cp -r "$BACKEND_DIR/sdks/stratifyx-python-sdk" "$SCRIPT_DIR/python/stratifyx"

echo "  Syncing epoch-protos..."
rm -rf "$SCRIPT_DIR/python/epoch-protos"
cp -r "$BACKEND_DIR/packages/epoch-protos/python" "$SCRIPT_DIR/python/epoch-protos"

# TypeScript packages
echo ""
echo "=== TypeScript Packages ==="

echo "  Syncing stratifyx..."
rm -rf "$SCRIPT_DIR/typescript/stratifyx"
cp -r "$BACKEND_DIR/sdks/stratifyx-typescript-sdk" "$SCRIPT_DIR/typescript/stratifyx"

echo "  Syncing epoch-protos..."
rm -rf "$SCRIPT_DIR/typescript/epoch-protos"
cp -r "$BACKEND_DIR/packages/epoch-protos/typescript" "$SCRIPT_DIR/typescript/epoch-protos"

echo "  Syncing tree-sitter-epochscript..."
rm -rf "$SCRIPT_DIR/typescript/tree-sitter-epochscript"
cp -r "$BACKEND_DIR/packages/epoch-script/grammars/tree-sitter-epochscript" "$SCRIPT_DIR/typescript/tree-sitter-epochscript"

echo "  Syncing lezer-epochscript..."
rm -rf "$SCRIPT_DIR/typescript/lezer-epochscript"
cp -r "$BACKEND_DIR/packages/epoch-script/grammars/lezer-epochscript" "$SCRIPT_DIR/typescript/lezer-epochscript"

echo ""
echo "Done! All SDKs synced."
echo ""
echo "Python packages:"
ls -1 "$SCRIPT_DIR/python"
echo ""
echo "TypeScript packages:"
ls -1 "$SCRIPT_DIR/typescript"
