"""SQLite persistence backend for KERNELS audit ledger entries."""

from __future__ import annotations

import json
import logging
import sqlite3
from pathlib import Path
from typing import Any

LOGGER = logging.getLogger(__name__)


class SQLiteAuditStorage:
    """Persist and retrieve audit entries in a local SQLite database."""

    def __init__(self, database_path: str) -> None:
        self._database_path = Path(database_path)
        self._database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._database_path)
        connection.execute("PRAGMA journal_mode=WAL")
        connection.execute("PRAGMA foreign_keys=ON")
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS audit_entries (
                    kernel_id TEXT NOT NULL,
                    ledger_seq INTEGER NOT NULL,
                    entry_hash TEXT NOT NULL,
                    prev_hash TEXT NOT NULL,
                    ts_ms INTEGER NOT NULL,
                    request_id TEXT NOT NULL,
                    actor TEXT NOT NULL,
                    intent TEXT NOT NULL,
                    decision TEXT NOT NULL,
                    state_from TEXT NOT NULL,
                    state_to TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    PRIMARY KEY (kernel_id, ledger_seq)
                )
                """
            )

    def append(self, kernel_id: str, entry: dict[str, Any]) -> None:
        """Insert a single audit entry row."""
        required_fields = {
            "ledger_seq",
            "entry_hash",
            "prev_hash",
            "ts_ms",
            "request_id",
            "actor",
            "intent",
            "decision",
            "state_from",
            "state_to",
        }
        missing = sorted(required_fields - set(entry.keys()))
        if missing:
            raise ValueError(f"entry missing required fields: {', '.join(missing)}")

        payload_json = json.dumps(entry, sort_keys=True, separators=(",", ":"))
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO audit_entries (
                    kernel_id, ledger_seq, entry_hash, prev_hash, ts_ms,
                    request_id, actor, intent, decision, state_from, state_to, payload_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    kernel_id,
                    int(entry["ledger_seq"]),
                    str(entry["entry_hash"]),
                    str(entry["prev_hash"]),
                    int(entry["ts_ms"]),
                    str(entry["request_id"]),
                    str(entry["actor"]),
                    str(entry["intent"]),
                    str(entry["decision"]),
                    str(entry["state_from"]),
                    str(entry["state_to"]),
                    payload_json,
                ),
            )

    def list_entries(self, kernel_id: str) -> list[dict[str, Any]]:
        """Return all entries for a kernel ordered by ledger sequence."""
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT payload_json FROM audit_entries
                WHERE kernel_id = ?
                ORDER BY ledger_seq ASC
                """,
                (kernel_id,),
            ).fetchall()

        return [json.loads(row[0]) for row in rows]

    def health(self) -> dict[str, Any]:
        """Return a minimal observability health payload for this storage backend."""
        with self._connect() as connection:
            entry_count = int(connection.execute("SELECT COUNT(*) FROM audit_entries").fetchone()[0])
        payload = {
            "database_path": str(self._database_path),
            "entry_count": entry_count,
            "exists": self._database_path.exists(),
        }
        LOGGER.debug("sqlite audit storage health", extra=payload)
        return payload
