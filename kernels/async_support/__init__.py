"""
KERNELS Async Module

Provides async/await support for kernel operations.
"""

from kernels.async_support.async_kernel import (
    AsyncStrictKernel,
    AsyncPermissiveKernel,
    AsyncEvidenceFirstKernel,
    AsyncDualChannelKernel,
)
from kernels.async_support.async_dispatcher import AsyncDispatcher

__all__ = [
    "AsyncStrictKernel",
    "AsyncPermissiveKernel",
    "AsyncEvidenceFirstKernel",
    "AsyncDualChannelKernel",
    "AsyncDispatcher",
]
