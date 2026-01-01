#!/usr/bin/env python3
"""Example 02: Tool Execution

Demonstrates tool invocation through the kernel with built-in tools.
"""

from kernels.common.types import (
    KernelConfig,
    KernelRequest,
    ToolCall,
    VirtualClock,
)
from kernels.variants.strict_kernel import StrictKernel


def main() -> None:
    """Run tool execution example."""
    # Create and boot kernel
    kernel = StrictKernel()
    config = KernelConfig(
        kernel_id="tool-example-001",
        variant="strict",
        clock=VirtualClock(1000),
    )
    kernel.boot(config)

    print("Kernel booted with built-in tools: echo, add")
    print("-" * 50)

    # Example 1: Echo tool
    echo_request = KernelRequest(
        request_id="req-echo-001",
        ts_ms=1000,
        actor="tool-user",
        intent="Echo a message through the kernel",
        tool_call=ToolCall(
            name="echo",
            params={"text": "Hello from the kernel!"},
        ),
    )

    print("\n[Echo Tool]")
    print(f"Request: {echo_request.intent}")
    print(f"Tool: {echo_request.tool_call.name}")
    print(f"Params: {echo_request.tool_call.params}")

    receipt = kernel.submit(echo_request)

    print(f"Status: {receipt.status.value}")
    print(f"Decision: {receipt.decision.value}")
    print(f"Result: {receipt.tool_result}")

    # Example 2: Add tool
    add_request = KernelRequest(
        request_id="req-add-001",
        ts_ms=2000,
        actor="tool-user",
        intent="Add two numbers",
        tool_call=ToolCall(
            name="add",
            params={"a": 17, "b": 25},
        ),
    )

    print("\n[Add Tool]")
    print(f"Request: {add_request.intent}")
    print(f"Tool: {add_request.tool_call.name}")
    print(f"Params: {add_request.tool_call.params}")

    receipt = kernel.submit(add_request)

    print(f"Status: {receipt.status.value}")
    print(f"Decision: {receipt.decision.value}")
    print(f"Result: {receipt.tool_result}")

    # Example 3: Unknown tool (should fail)
    unknown_request = KernelRequest(
        request_id="req-unknown-001",
        ts_ms=3000,
        actor="tool-user",
        intent="Try to use an unknown tool",
        tool_call=ToolCall(
            name="unknown_tool",
            params={},
        ),
    )

    print("\n[Unknown Tool]")
    print(f"Request: {unknown_request.intent}")
    print(f"Tool: {unknown_request.tool_call.name}")

    receipt = kernel.submit(unknown_request)

    print(f"Status: {receipt.status.value}")
    print(f"Decision: {receipt.decision.value}")
    print(f"Error: {receipt.error}")

    # Summary
    evidence = kernel.export_evidence()
    print("\n" + "-" * 50)
    print(f"Total audit entries: {len(evidence.ledger_entries)}")
    print(f"Root hash: {evidence.root_hash[:32]}...")


if __name__ == "__main__":
    main()
