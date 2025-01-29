"""
NOVA (Neuro-Symbolic, Optimized, Versatile Agent)
A framework for building autonomous, multilingual, and logically consistent AI solutions.

Created by extending the original NOVA methodology by rUv (github.com/ruvnet/nova)
"""

from nova.crew import NovaCrew

__version__ = "2.0.0"
__author__ = "Your Organization"
__credits__ = ["rUv (Original NOVA methodology)", "Your Team"]
__license__ = "MIT"
__maintainer__ = "Your Team"
__email__ = "team@example.com"
__status__ = "Development"

# Version info
VERSION_INFO = {
    'major': 2,
    'minor': 0,
    'patch': 0,
    'release': 'alpha',
    'build': '1'
}

# Component versions
COMPONENT_VERSIONS = {
    'symbolic_engine': '1.0.0',
    'language_processor': '1.0.0',
    'planner': '1.0.0',
    'tool_interface': '1.0.0'
}

# Default configurations
DEFAULT_CONFIG = {
    'log_level': 'INFO',
    'timeout': 300,
    'max_retries': 3
}

# Expose main components
__all__ = [
    'NovaCrew'
]