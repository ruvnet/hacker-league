"""
NOVA Configuration Management

This module handles loading and validating NOVA system configurations.
"""

import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path

class ConfigurationError(Exception):
    """Exception raised for configuration errors"""
    pass

class NovaConfig:
    """NOVA configuration manager"""
    
    def __init__(self, config_dir: Optional[str] = None):
        self.config_dir = config_dir or os.path.dirname(__file__)
        self.agents_config = {}
        self.tasks_config = {}
        self.analysis_config = {}
        self._load_configurations()
        
    def _load_configurations(self):
        """Load all configuration files"""
        try:
            # Load agents configuration
            with open(os.path.join(self.config_dir, 'agents.yaml'), 'r') as f:
                self.agents_config = yaml.safe_load(f)
            
            # Load tasks configuration
            with open(os.path.join(self.config_dir, 'tasks.yaml'), 'r') as f:
                self.tasks_config = yaml.safe_load(f)
            
            # Load analysis configuration
            with open(os.path.join(self.config_dir, 'analysis.yaml'), 'r') as f:
                self.analysis_config = yaml.safe_load(f)
                
            # Validate configurations
            self._validate_configurations()
            
        except Exception as e:
            raise ConfigurationError(f"Failed to load configurations: {str(e)}")
            
    def _validate_configurations(self):
        """Validate loaded configurations"""
        # Validate agents configuration
        if not self.agents_config:
            raise ConfigurationError("Agents configuration is empty")
        
        required_agent_keys = ['researcher', 'executor', 'analyzer']
        for key in required_agent_keys:
            if key not in self.agents_config:
                raise ConfigurationError(f"Missing required agent configuration: {key}")
        
        # Validate tasks configuration
        if not self.tasks_config:
            raise ConfigurationError("Tasks configuration is empty")
            
        required_task_keys = ['research_task', 'execution_task', 'analysis_task']
        for key in required_task_keys:
            if key not in self.tasks_config:
                raise ConfigurationError(f"Missing required task configuration: {key}")
        
        # Validate analysis configuration
        if not self.analysis_config:
            raise ConfigurationError("Analysis configuration is empty")
            
        required_analysis_keys = ['metrics', 'validation']
        for key in required_analysis_keys:
            if key not in self.analysis_config:
                raise ConfigurationError(f"Missing required analysis configuration: {key}")
    
    def get_agent_config(self, agent_name: str) -> Dict[str, Any]:
        """Get configuration for specific agent"""
        if agent_name not in self.agents_config:
            raise ConfigurationError(f"Unknown agent: {agent_name}")
        return self.agents_config[agent_name]
    
    def get_task_config(self, task_name: str) -> Dict[str, Any]:
        """Get configuration for specific task"""
        if task_name not in self.tasks_config:
            raise ConfigurationError(f"Unknown task: {task_name}")
        return self.tasks_config[task_name]
    
    def get_analysis_config(self, section: str) -> Dict[str, Any]:
        """Get configuration for specific analysis section"""
        if section not in self.analysis_config:
            raise ConfigurationError(f"Unknown analysis section: {section}")
        return self.analysis_config[section]
    
    def update_config(self, config_type: str, updates: Dict[str, Any]):
        """Update configuration with new values"""
        if config_type == "agents":
            self.agents_config.update(updates)
        elif config_type == "tasks":
            self.tasks_config.update(updates)
        elif config_type == "analysis":
            self.analysis_config.update(updates)
        else:
            raise ConfigurationError(f"Unknown configuration type: {config_type}")
        
        # Validate after updates
        self._validate_configurations()
        
        # Save updated configurations
        self._save_configurations(config_type)
    
    def _save_configurations(self, config_type: str):
        """Save updated configurations to files"""
        try:
            if config_type == "agents":
                with open(os.path.join(self.config_dir, 'agents.yaml'), 'w') as f:
                    yaml.safe_dump(self.agents_config, f)
            elif config_type == "tasks":
                with open(os.path.join(self.config_dir, 'tasks.yaml'), 'w') as f:
                    yaml.safe_dump(self.tasks_config, f)
            elif config_type == "analysis":
                with open(os.path.join(self.config_dir, 'analysis.yaml'), 'w') as f:
                    yaml.safe_dump(self.analysis_config, f)
        except Exception as e:
            raise ConfigurationError(f"Failed to save configurations: {str(e)}")

# Create global configuration instance
config = NovaConfig()

# Export configuration instance
__all__ = ['config', 'ConfigurationError']