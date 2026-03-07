from __future__ import annotations

import threading

import pytest

from implementations.permits_threadsafe import ThreadSafeNonceRegistry
from implementations.storage import SQLiteAuditStorage


class TestThreadSafeNonceRegistry:
    def test_first_use_and_max_executions(self) -> None:
        registry = ThreadSafeNonceRegistry()

        assert registry.check_and_record("n1", "issuer", "subject", "permit", 2, 100)
        assert registry.check_and_record("n1", "issuer", "subject", "permit", 2, 110)
        assert not registry.check_and_record("n1", "issuer", "subject", "permit", 2, 120)

        stats = registry.stats()
        assert stats["allowed"] == 2
        assert stats["denied"] == 1
        assert stats["registry_size"] == 1

    def test_ttl_cleanup(self) -> None:
        registry = ThreadSafeNonceRegistry(ttl_ms=10)
        assert registry.check_and_record("n1", "issuer", "subject", "permit", 1, 100)
        assert registry.size() == 1

        removed = registry.cleanup(111)
        assert removed == 1
        assert registry.size() == 0
        assert registry.stats()["cleanup_removed"] == 1

    def test_invalid_inputs(self) -> None:
        with pytest.raises(ValueError):
            ThreadSafeNonceRegistry(ttl_ms=-1)

        registry = ThreadSafeNonceRegistry()
        with pytest.raises(ValueError):
            registry.check_and_record("n", "i", "s", "p", 0, 1)
        with pytest.raises(ValueError):
            registry.cleanup(-1)

    def test_thread_safety(self) -> None:
        registry = ThreadSafeNonceRegistry()
        outcomes: list[bool] = []
        lock = threading.Lock()

        def worker() -> None:
            result = registry.check_and_record("n1", "issuer", "subject", "permit", 100, 100)
            with lock:
                outcomes.append(result)

        threads = [threading.Thread(target=worker) for _ in range(30)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        assert len(outcomes) == 30
        assert outcomes.count(True) == 30
        record = registry.get_record("n1", "issuer", "subject")
        assert record is not None
        assert record.use_count == 30


class TestSQLiteAuditStorage:
    @pytest.fixture
    def storage(self, tmp_path) -> SQLiteAuditStorage:
        return SQLiteAuditStorage(str(tmp_path / "audit.db"))

    @staticmethod
    def _entry(seq: int) -> dict[str, object]:
        return {
            "ledger_seq": seq,
            "entry_hash": f"hash-{seq}",
            "prev_hash": f"prev-{seq}",
            "ts_ms": 1000 + seq,
            "request_id": f"req-{seq}",
            "actor": "actor",
            "intent": "intent",
            "decision": "ALLOW",
            "state_from": "RECEIVED",
            "state_to": "DECIDED",
            "extra": {"seq": seq},
        }

    def test_append_and_ordered_list(self, storage: SQLiteAuditStorage) -> None:
        storage.append("kernel", self._entry(2))
        storage.append("kernel", self._entry(1))

        entries = storage.list_entries("kernel")
        assert [entry["ledger_seq"] for entry in entries] == [1, 2]

    def test_health(self, storage: SQLiteAuditStorage) -> None:
        storage.append("kernel", self._entry(1))
        health = storage.health()

        assert health["exists"] is True
        assert health["entry_count"] == 1
        assert str(health["database_path"]).endswith("audit.db")

    def test_missing_required_fields_raises(self, storage: SQLiteAuditStorage) -> None:
        with pytest.raises(ValueError, match="entry missing required fields"):
            storage.append("kernel", {"ledger_seq": 1})
