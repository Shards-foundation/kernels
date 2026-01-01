#!/bin/bash
# Run all unit tests

set -e

cd "$(dirname "$0")/.."

echo "Running Kernels test suite..."
echo "=============================="

python3 -m unittest discover -s tests -v

echo ""
echo "All tests passed."
