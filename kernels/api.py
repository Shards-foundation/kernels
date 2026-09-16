"""Public, supported API surface for KERNELS.

If it isn't imported here and re-exported via __all__, treat it as internal
and subject to change. This file is the compatibility contract.

Usage:
    from kernels.api import Kernel, KernelRequest, KernelReceipt, Decision
    # or
    from kernels import Kernel, KernelRequest, KernelReceipt, Decision
"""

from __future__ import annotations

# -----------------------------------------------------------------------------
# Evidence surface (stable)
# -----------------------------------------------------------------------------
from kernels.audit.ledger import AuditLedger
from kernels.audit.replay import (
    ReplayResult,
    replay_and_verify,
    verify_evidence_bundle,
)

# -----------------------------------------------------------------------------
# Core types (stable)
# -----------------------------------------------------------------------------
from kernels.common.types import (
    Decision,
    KernelConfig,
    KernelReceipt,
    KernelRequest,
    KernelState,
    ReceiptStatus,
    ToolCall,
    VirtualClock,
)
from kernels.core.runtime import (
    Artifact,
    ArtifactRef,
    ExecutionContext,
    ExecutionIdentity,
    GraphBudget,
    GraphExecutionResult,
    KernelRuntime,
    RuntimeEvent,
    RuntimeExecutionResult,
    RuntimeState,
    TaskGraph,
    TaskNode,
)

# -----------------------------------------------------------------------------
# Tooling surface (stable)
# -----------------------------------------------------------------------------
from kernels.execution.tools import ToolRegistry

# -----------------------------------------------------------------------------
# Jurisdiction (stable)
# -----------------------------------------------------------------------------
from kernels.jurisdiction.policy import JurisdictionPolicy

# -----------------------------------------------------------------------------
# Permit System (v0.2.0+)
# -----------------------------------------------------------------------------
from kernels.permits import (
    NonceRegistry,
    PermitBuilder,
    PermitToken,
    PermitVerificationResult,
    canonical_permit_bytes,
    compute_permit_id,
    generate_nonce,
    sign_permit,
    verify_permit,
    verify_signature,
)

# -----------------------------------------------------------------------------
# Interfaces / protocols (stable)
# -----------------------------------------------------------------------------
from kernels.variants.base import BaseKernel, Kernel
from kernels.variants.dual_channel_kernel import DualChannelKernel
from kernels.variants.evidence_first_kernel import EvidenceFirstKernel
from kernels.variants.permissive_kernel import PermissiveKernel

# -----------------------------------------------------------------------------
# Kernel variants (stable)
# -----------------------------------------------------------------------------
from kernels.variants.strict_kernel import StrictKernel

# -----------------------------------------------------------------------------
# Public API surface
# -----------------------------------------------------------------------------
__all__ = [
    # Core types
    "Decision",
    "KernelConfig",
    "KernelRequest",
    "KernelReceipt",
    "KernelState",
    "ReceiptStatus",
    "ToolCall",
    "VirtualClock",
    # Interfaces
    "Kernel",
    "BaseKernel",
    # Variants
    "StrictKernel",
    "PermissiveKernel",
    "EvidenceFirstKernel",
    "DualChannelKernel",
    # Tooling
    "ToolRegistry",
    "ExecutionContext",
    "ExecutionIdentity",
    "GraphBudget",
    "ArtifactRef",
    "Artifact",
    "TaskNode",
    "TaskGraph",
    "GraphExecutionResult",
    "RuntimeState",
    "KernelRuntime",
    "RuntimeEvent",
    "RuntimeExecutionResult",
    # Evidence
    "AuditLedger",
    "replay_and_verify",
    "verify_evidence_bundle",
    "ReplayResult",
    # Jurisdiction
    "JurisdictionPolicy",
    # Permit System (v0.2.0+)
    "PermitToken",
    "PermitBuilder",
    "PermitVerificationResult",
    "NonceRegistry",
    "canonical_permit_bytes",
    "compute_permit_id",
    "generate_nonce",
    "sign_permit",
    "verify_permit",
    "verify_signature",
]
