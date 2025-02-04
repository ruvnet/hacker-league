"""
Oncology System Package

This package provides tools and utilities for medical image analysis,
report processing, and knowledge-based diagnosis support using LLMs.
"""

from .main import OncologySystem, create_system
from .crew import OncologyCrew
from .cache import OncologyCache

__version__ = '0.1.0'
__author__ = 'Roo'

__all__ = [
    'OncologySystem',
    'create_system',
    'OncologyCrew',
    'OncologyCache'
]