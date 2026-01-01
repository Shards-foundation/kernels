"""Kernel variants with different enforcement postures."""

from kernels.variants.base import Kernel
from kernels.variants.strict_kernel import StrictKernel
from kernels.variants.permissive_kernel import PermissiveKernel
from kernels.variants.evidence_first_kernel import EvidenceFirstKernel
from kernels.variants.dual_channel_kernel import DualChannelKernel

__all__ = [
    "Kernel",
    "StrictKernel",
    "PermissiveKernel",
    "EvidenceFirstKernel",
    "DualChannelKernel",
]
