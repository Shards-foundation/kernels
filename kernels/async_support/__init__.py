"""
KERNELS Async Module

Provides async/await support for kernel operations.
"""

from kernels.async_support.async_dispatcher import AsyncDispatcher
from kernels.async_support.async_kernel import (
    AsyncDualChannelKernel,
    AsyncEvidenceFirstKernel,
    AsyncPermissiveKernel,
    AsyncStrictKernel,
)

__all__ = [
    "AsyncStrictKernel",
    "AsyncPermissiveKernel",
    "AsyncEvidenceFirstKernel",
    "AsyncDualChannelKernel",
    "AsyncDispatcher",
]
