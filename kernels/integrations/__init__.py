"""
KERNELS Integrations

Adapters and integrations for popular frameworks.
"""

from kernels.integrations.fastapi_adapter import create_fastapi_app
from kernels.integrations.flask_adapter import create_flask_app
from kernels.integrations.mcp_adapter import MCPAdapter

__all__ = [
    "create_fastapi_app",
    "create_flask_app",
    "MCPAdapter",
]
