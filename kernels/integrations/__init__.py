"""
KERNELS Integrations

Adapters and integrations for popular frameworks.
"""

from kernels.integrations.fastapi_adapter import create_fastapi_app
from kernels.integrations.flask_adapter import create_flask_app
from kernels.integrations.mcp_adapter import MCPAdapter
from kernels.integrations.langchain_adapter import (
    LangChainAdapter,
    GovernedTool,
    LangChainToolResult,
    create_langchain_adapter,
)
from kernels.integrations.huggingface_adapter import (
    HuggingFaceAdapter,
    GovernedHFTool,
    HFToolResult,
    PermitInjector,
    create_huggingface_adapter,
)
from kernels.integrations.generic_adapter import (
    GenericAdapter,
    MoltbookAdapter,
    ToolExecutionResult,
    create_generic_adapter,
    create_moltbook_adapter,
)

__all__ = [
    "create_fastapi_app",
    "create_flask_app",
    "MCPAdapter",
    "LangChainAdapter",
    "GovernedTool",
    "LangChainToolResult",
    "create_langchain_adapter",
    "HuggingFaceAdapter",
    "GovernedHFTool",
    "HFToolResult",
    "PermitInjector",
    "create_huggingface_adapter",
    "GenericAdapter",
    "MoltbookAdapter",
    "ToolExecutionResult",
    "create_generic_adapter",
    "create_moltbook_adapter",
]
