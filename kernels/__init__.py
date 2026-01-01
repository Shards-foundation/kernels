"""
Kernels: Deterministic Control Planes for AI Systems.

This package provides a deterministic state machine that governs all AI agent
execution through explicit jurisdiction, append-only audit, and fail-closed
semantics.
"""

from kernels._version import __version__
from kernels.common.types import (
    Decision,
    EvidenceBundle,
    KernelConfig,
    KernelRequest,
    KernelReceipt,
    KernelState,
    ReceiptStatus,
)
from kernels.common.errors import (
    KernelError,
    BootError,
    StateError,
    JurisdictionError,
    AmbiguityError,
    ToolError,
    AuditError,
)
from kernels.variants.base import Kernel

__all__ = [
    "__version__",
    "Decision",
    "EvidenceBundle",
    "Kernel",
    "KernelConfig",
    "KernelError",
    "KernelReceipt",
    "KernelRequest",
    "KernelState",
    "ReceiptStatus",
    "BootError",
    "StateError",
    "JurisdictionError",
    "AmbiguityError",
    "ToolError",
    "AuditError",
]
