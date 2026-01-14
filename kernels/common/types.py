"""Core type definitions for Kernels."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class KernelState(Enum):
    """Defined states for the kernel state machine."""

    BOOTING = "BOOTING"
    IDLE = "IDLE"
    VALIDATING = "VALIDATING"
    ARBITRATING = "ARBITRATING"
    EXECUTING = "EXECUTING"
    AUDITING = "AUDITING"
    HALTED = "HALTED"


class Decision(Enum):
    """Possible decisions from kernel arbitration."""

    ALLOW = "ALLOW"
    DENY = "DENY"
    HALT = "HALT"


class ReceiptStatus(Enum):
    """Status of a kernel receipt."""

    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    FAILED = "FAILED"


@dataclass(frozen=True)
class ToolCall:
    """Specification of a tool invocation."""

    name: str
    params: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class KernelRequest:
    """A request submitted to the kernel for arbitration."""

    request_id: str
    ts_ms: int
    actor: str
    intent: str
    tool_call: Optional[ToolCall] = None
    params: dict[str, Any] = field(default_factory=dict)
    evidence: Optional[str] = None


@dataclass(frozen=True)
class KernelReceipt:
    """Receipt returned by the kernel after processing a request."""

    request_id: str
    status: ReceiptStatus
    state_from: KernelState
    state_to: KernelState
    ts_ms: int
    decision: Decision
    error: Optional[str] = None
    evidence_hash: Optional[str] = None
    tool_result: Optional[Any] = None


@dataclass(frozen=True)
class AuditEntry:
    """A single entry in the append-only audit ledger."""

    prev_hash: str
    entry_hash: str
    ts_ms: int
    request_id: str
    actor: str
    intent: str
    decision: Decision
    state_from: KernelState
    state_to: KernelState
    tool_name: Optional[str] = None
    params_hash: Optional[str] = None
    evidence_hash: Optional[str] = None
    error: Optional[str] = None

    # Permit-related fields (added in v0.2.0)
    permit_digest: Optional[str] = None
    permit_verification: Optional[str] = None  # "ALLOW" | "DENY"
    permit_denial_reasons: tuple[str, ...] = field(default_factory=tuple)
    proposal_hash: Optional[str] = None


@dataclass(frozen=True)
class EvidenceBundle:
    """Exportable evidence bundle with full ledger and verification data."""

    ledger_entries: tuple[AuditEntry, ...]
    root_hash: str
    exported_at_ms: int
    kernel_id: str
    variant: str


class VirtualClock:
    """Deterministic clock for kernel operations."""

    def __init__(self, initial_ms: int = 0) -> None:
        """Initialize clock with starting time."""
        self._current_ms = initial_ms

    def now_ms(self) -> int:
        """Return current time in milliseconds."""
        return self._current_ms

    def advance(self, delta_ms: int) -> None:
        """Advance clock by specified milliseconds."""
        if delta_ms < 0:
            raise ValueError("Clock cannot move backward")
        self._current_ms += delta_ms

    def set(self, ts_ms: int) -> None:
        """Set clock to specific time."""
        if ts_ms < self._current_ms:
            raise ValueError("Clock cannot move backward")
        self._current_ms = ts_ms


# Type aliases for SDK compatibility
Request = KernelRequest
Receipt = KernelReceipt


@dataclass
class KernelConfig:
    """Configuration for a kernel instance."""

    kernel_id: str
    variant: str
    fail_closed: bool = True
    require_jurisdiction: bool = True
    require_audit: bool = True
    clock: VirtualClock = field(default_factory=VirtualClock)
    hash_alg: str = "sha256"
    max_param_bytes: int = 65536
    max_intent_length: int = 4096
