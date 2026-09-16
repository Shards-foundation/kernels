"""Core runtime primitives.

This package contains the canonical runtime execution choke point used by
kernel variants to mediate tool execution through a single interface.
"""

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

__all__ = [
    "ExecutionContext",
    "ExecutionIdentity",
    "GraphBudget",
    "ArtifactRef",
    "Artifact",
    "TaskNode",
    "TaskGraph",
    "GraphExecutionResult",
    "RuntimeState",
    "RuntimeEvent",
    "RuntimeExecutionResult",
    "KernelRuntime",
]
