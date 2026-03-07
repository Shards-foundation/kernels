"""Thread-safe nonce registry implementation for permit replay protection."""

from __future__ import annotations

import logging
from dataclasses import replace
from threading import RLock

from kernels.permits import NonceRecord

LOGGER = logging.getLogger(__name__)


class ThreadSafeNonceRegistry:
    """Thread-safe nonce registry with optional TTL cleanup for long-running services."""

    def __init__(self, ttl_ms: int | None = None) -> None:
        if ttl_ms is not None and ttl_ms < 0:
            raise ValueError("ttl_ms must be >= 0 when provided")

        self._registry: dict[tuple[str, str, str], NonceRecord] = {}
        self._ttl_ms = ttl_ms
        self._lock = RLock()
        self._stats = {
            "allowed": 0,
            "denied": 0,
            "cleanup_runs": 0,
            "cleanup_removed": 0,
        }

    def check_and_record(
        self,
        nonce: str,
        issuer: str,
        subject: str,
        permit_id: str,
        max_executions: int,
        current_time_ms: int,
    ) -> bool:
        """Atomically check replay status and record nonce usage."""
        if max_executions < 1:
            raise ValueError("max_executions must be >= 1")
        if current_time_ms < 0:
            raise ValueError("current_time_ms must be >= 0")

        key = (nonce, issuer, subject)
        with self._lock:
            self._cleanup_locked(current_time_ms)

            record = self._registry.get(key)
            if record is None:
                self._registry[key] = NonceRecord(
                    nonce=nonce,
                    issuer=issuer,
                    subject=subject,
                    first_seen_ms=current_time_ms,
                    use_count=1,
                    permit_id=permit_id,
                )
                self._stats["allowed"] += 1
                return True

            if record.use_count >= max_executions:
                self._stats["denied"] += 1
                LOGGER.warning(
                    "nonce replay denied",
                    extra={"nonce": nonce, "issuer": issuer, "subject": subject, "permit_id": permit_id},
                )
                return False

            self._registry[key] = replace(record, use_count=record.use_count + 1)
            self._stats["allowed"] += 1
            return True

    def get_record(self, nonce: str, issuer: str, subject: str) -> NonceRecord | None:
        """Retrieve a nonce record if present."""
        with self._lock:
            return self._registry.get((nonce, issuer, subject))

    def has_nonce(self, nonce: str, issuer: str, subject: str) -> bool:
        """Check whether a nonce has been seen before."""
        with self._lock:
            return (nonce, issuer, subject) in self._registry

    def size(self) -> int:
        """Return number of tracked nonce records."""
        with self._lock:
            return len(self._registry)

    def stats(self) -> dict[str, int]:
        """Return observability counters for monitoring and debugging."""
        with self._lock:
            return {
                "allowed": int(self._stats["allowed"]),
                "denied": int(self._stats["denied"]),
                "cleanup_runs": int(self._stats["cleanup_runs"]),
                "cleanup_removed": int(self._stats["cleanup_removed"]),
                "registry_size": len(self._registry),
            }

    def cleanup(self, current_time_ms: int) -> int:
        """Cleanup expired records and return number removed."""
        if current_time_ms < 0:
            raise ValueError("current_time_ms must be >= 0")

        with self._lock:
            return self._cleanup_locked(current_time_ms)

    def _cleanup_locked(self, current_time_ms: int) -> int:
        if self._ttl_ms is None:
            return 0

        stale_keys = [
            key
            for key, record in self._registry.items()
            if current_time_ms - record.first_seen_ms > self._ttl_ms
        ]
        for key in stale_keys:
            del self._registry[key]

        self._stats["cleanup_runs"] += 1
        self._stats["cleanup_removed"] += len(stale_keys)
        if stale_keys:
            LOGGER.info("nonce cleanup removed stale records", extra={"removed": len(stale_keys)})
        return len(stale_keys)
