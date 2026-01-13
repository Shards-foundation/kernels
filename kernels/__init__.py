"""KERNELS — Deterministic Control Planes for AI Systems.

Public API surface is defined in kernels.api. Only items exported there
are part of the supported, stable interface. Everything else is internal
and subject to change without notice.

Usage:
    from kernels import StrictKernel, KernelRequest, Decision
    # or explicitly:
    from kernels.api import StrictKernel, KernelRequest, Decision
"""

# Re-export the public API surface
from kernels.api import *  # noqa: F401, F403
from kernels.api import __all__ as _api_all

# Version
from kernels._version import __version__

# Errors (also part of public surface, but kept separate for clarity)
from kernels.common.errors import (
    KernelError,
    BootError,
    StateError,
    JurisdictionError,
    AmbiguityError,
    ToolError,
    AuditError,
)

# Evidence bundle type
from kernels.common.types import EvidenceBundle

__all__ = [
    "__version__",
    # Errors
    "KernelError",
    "BootError",
    "StateError",
    "JurisdictionError",
    "AmbiguityError",
    "ToolError",
    "AuditError",
    # Evidence
    "EvidenceBundle",
    # Plus everything from api.py
    *_api_all,
]
