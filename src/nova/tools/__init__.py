"""
NOVA Tools Package

This package provides custom tools and utilities for extending NOVA's functionality.
"""

from nova.tools.custom_tool import (
    NovaBaseTool,
    NovaDataTool,
    NovaAPITool,
    NovaSymbolicTool,
    create_tool
)

__all__ = [
    'NovaBaseTool',
    'NovaDataTool',
    'NovaAPITool',
    'NovaSymbolicTool',
    'create_tool'
]

# Tool version information
TOOL_VERSIONS = {
    'base': '1.0.0',
    'data': '1.0.0',
    'api': '1.0.0',
    'symbolic': '1.0.0'
}

# Default tool configurations
DEFAULT_TOOL_CONFIG = {
    'timeout': 30,
    'retry_count': 3,
    'cache_enabled': True,
    'cache_ttl': 3600
}

def get_tool_info(tool_name: str) -> dict:
    """Get information about a specific tool"""
    return {
        'version': TOOL_VERSIONS.get(tool_name, 'unknown'),
        'config': DEFAULT_TOOL_CONFIG
    }

def list_available_tools() -> list:
    """List all available tools"""
    return list(TOOL_VERSIONS.keys())