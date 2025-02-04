"""
Oncology System Configuration Package

This package provides configuration management for models,
tasks, and system settings.
"""

import os
import yaml
from pathlib import Path

def load_config(filename: str) -> dict:
    """Load configuration from YAML file."""
    config_dir = Path(__file__).parent
    config_path = config_dir / filename
    
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {filename}")
    
    with open(config_path) as f:
        return yaml.safe_load(f)

def get_models_config() -> dict:
    """Get models configuration."""
    return load_config('models.yaml')

def get_tasks_config() -> dict:
    """Get tasks configuration."""
    return load_config('tasks.yaml')

__all__ = [
    'load_config',
    'get_models_config',
    'get_tasks_config'
]