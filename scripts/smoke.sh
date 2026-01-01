#!/bin/bash
# Smoke test: verify basic functionality

set -e

cd "$(dirname "$0")/.."

echo "Kernels Smoke Test"
echo "=================="

echo ""
echo "[1/5] Checking Python version..."
python3 --version

echo ""
echo "[2/5] Running minimal example..."
python3 examples/01_minimal_request.py

echo ""
echo "[3/5] Running tool execution example..."
python3 examples/02_tool_execution.py

echo ""
echo "[4/5] Checking CLI help..."
python3 -m kernels --help

echo ""
echo "[5/5] Checking CLI version..."
python3 -m kernels --version

echo ""
echo "=================="
echo "Smoke test passed."
