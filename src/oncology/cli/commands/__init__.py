"""
Command modules for the Oncology System CLI.
Each module handles a specific category of operations.
"""

from .kb import KBCommands
from .genomic import GenomicCommands
from .bio import BioCommands
from .doc import DocCommands

__all__ = ['KBCommands', 'GenomicCommands', 'BioCommands', 'DocCommands']