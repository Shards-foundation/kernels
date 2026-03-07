#!/bin/bash
# Smoke test: verify basic functionality and integration touchpoints

set -euo pipefail

cd "$(dirname "$0")/.."
export PYTHONPATH="${PYTHONPATH:-}:$(pwd)"

echo "Kernels Smoke Test"
echo "=================="

echo ""
echo "[1/8] Checking Python version..."
python3 --version

echo ""
echo "[2/8] Running minimal example..."
python3 examples/01_minimal_request.py

echo ""
echo "[3/8] Running tool execution example..."
python3 examples/02_tool_execution.py

echo ""
echo "[4/8] Running permit integration example..."
python3 examples/permit_integration_example.py

echo ""
echo "[5/8] Checking CLI help..."
python3 -m kernels --help

echo ""
echo "[6/8] Checking CLI version..."
python3 -m kernels --version

echo ""
echo "[7/8] Validating thread-safe nonce registry smoke..."
python3 - <<'PY'
from implementations.permits_threadsafe import ThreadSafeNonceRegistry

registry = ThreadSafeNonceRegistry(ttl_ms=5)
assert registry.check_and_record("nonce", "issuer", "subject", "permit", 1, 100)
assert not registry.check_and_record("nonce", "issuer", "subject", "permit", 1, 101)
assert registry.cleanup(200) == 1
assert registry.stats()["cleanup_removed"] == 1
print("Thread-safe nonce registry smoke passed")
PY

echo ""
echo "[8/8] Validating SQLite storage smoke..."
python3 - <<'PY'
from pathlib import Path
from tempfile import TemporaryDirectory

from implementations.storage import SQLiteAuditStorage

with TemporaryDirectory() as temp_dir:
    db_path = Path(temp_dir) / "audit.db"
    storage = SQLiteAuditStorage(str(db_path))
    storage.append(
        "kernel-smoke",
        {
            "ledger_seq": 1,
            "entry_hash": "h1",
            "prev_hash": "GENESIS",
            "ts_ms": 123,
            "request_id": "r1",
            "actor": "actor",
            "intent": "intent",
            "decision": "ALLOW",
            "state_from": "RECEIVED",
            "state_to": "DECIDED",
        },
    )
    assert len(storage.list_entries("kernel-smoke")) == 1
    assert storage.health()["entry_count"] == 1
print("SQLite storage smoke passed")
PY

echo ""
echo "=================="
echo "Smoke test passed."
