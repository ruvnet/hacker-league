"""
Oncology System Crew Implementation

This module implements the crew system for oncology analysis using OpenRouter,
following similar patterns to nova and hello_world implementations.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

from .tools.image_analyzer import ImageAnalysisTool
from .tools.text_analyzer import TextAnalysisTool
from .tools.knowledge_base import KnowledgeBaseTool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OncologyCrew:
    """
    Manages a crew of specialized agents for oncology analysis.
    Uses OpenRouter for LLM access and coordinates multi-modal analysis.
    """
    
    def __init__(self, config_dir: Optional[str] = None):
        """Initialize the oncology crew with configuration."""
        self.config_dir = Path(config_dir) if config_dir else Path(__file__).parent / 'config'
        self.models_config = self._load_config('models.yaml')
        self.tasks_config = self._load_config('tasks.yaml')
        
        # Initialize specialized agents
        self.agents = {
            'medical_expert': self._init_agent('medical_expert'),
            'image_analyst': self._init_agent('image_analyst'),
            'genomics_expert': self._init_agent('genomics_expert')
        }
        
        # Initialize tools
        self.tools = {
            'image_analysis': ImageAnalysisTool(
                self.tasks_config['tool_configs']['image_analysis']
            ),
            'text_analysis': TextAnalysisTool(
                self.tasks_config['tool_configs']['report_analysis']
            ),
            'knowledge_base': KnowledgeBaseTool(
                self.tasks_config['tool_configs']['knowledge_base']
            )
        }
        
        logger.info("Oncology crew initialized with %d agents and %d tools",
                   len(self.agents), len(self.tools))
    
    def _load_config(self, filename: str) -> Dict:
        """Load configuration from YAML file."""
        config_path = self.config_dir / filename
        try:
            with open(config_path) as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error("Failed to load config %s: %s", filename, str(e))
            raise
    
    def _init_agent(self, agent_type: str) -> Dict:
        """Initialize an agent with its configuration."""
        if agent_type not in self.models_config:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        agent_config = self.models_config[agent_type]
        return {
            'config': agent_config,
            'llm': agent_config['llm'],
            'role': agent_config['role'],
            'tools': []  # Will be populated based on tasks
        }
    
    def get_task_crew(self, task_name: str) -> List[str]:
        """Get the crew members required for a specific task."""
        for category in self.tasks_config:
            if task_name in self.tasks_config[category]:
                task = self.tasks_config[category][task_name]
                return task['required_agents']
        raise ValueError(f"Unknown task: {task_name}")
    
    def get_task_tools(self, task_name: str) -> List[str]:
        """Get the tools required for a specific task."""
        for category in self.tasks_config:
            if task_name in self.tasks_config[category]:
                task = self.tasks_config[category][task_name]
                return task['tools']
        raise ValueError(f"Unknown task: {task_name}")
    
    def validate_task_output(self, task_name: str, output: Any) -> bool:
        """Validate task output against configured requirements."""
        for category in self.tasks_config:
            if task_name in self.tasks_config[category]:
                task = self.tasks_config[category][task_name]
                validation = task['validation']
                
                # Check confidence threshold
                if 'confidence' in output:
                    if output['confidence'] < validation['confidence_threshold']:
                        logger.warning("Output confidence below threshold")
                        return False
                
                # Check evidence requirement
                if validation.get('require_evidence', False):
                    if 'evidence' not in output or not output['evidence']:
                        logger.warning("Required evidence missing from output")
                        return False
                
                # Additional validation based on task type
                if 'require_measurements' in validation and validation['require_measurements']:
                    if 'measurements' not in output or not output['measurements']:
                        logger.warning("Required measurements missing from output")
                        return False
                
                return True
        
        raise ValueError(f"Unknown task: {task_name}")
    
    def execute_task(self, task_name: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task using the appropriate crew and tools."""
        # Get required crew and tools
        required_agents = self.get_task_crew(task_name)
        required_tools = self.get_task_tools(task_name)
        
        logger.info("Executing task '%s' with %d agents and %d tools",
                   task_name, len(required_agents), len(required_tools))
        
        # Initialize task context
        context = {
            'task': task_name,
            'inputs': inputs,
            'intermediate_results': {},
            'tools_used': []
        }
        
        try:
            # Execute tools based on task requirements
            for tool_name in required_tools:
                if tool_name in self.tools:
                    tool_result = self.tools[tool_name](inputs)
                    context['intermediate_results'][tool_name] = tool_result
                    context['tools_used'].append(tool_name)
            
            # Have each required agent process the results
            agent_outputs = {}
            for agent_name in required_agents:
                if agent_name in self.agents:
                    agent = self.agents[agent_name]
                    agent_output = self._process_with_agent(agent, context)
                    agent_outputs[agent_name] = agent_output
            
            # Combine outputs into final result
            final_output = self._combine_outputs(task_name, agent_outputs)
            
            # Validate output
            if not self.validate_task_output(task_name, final_output):
                raise ValueError("Task output failed validation")
            
            return final_output
            
        except Exception as e:
            logger.error("Task execution failed: %s", str(e))
            raise
    
    def _process_with_agent(self, agent: Dict, context: Dict) -> Dict[str, Any]:
        """Process context with a specific agent using OpenRouter."""
        # TODO: Implement OpenRouter API call similar to nova/hello_world
        # For now, return a mock response
        return {
            'analysis': f"Analysis from {agent['role']}",
            'confidence': 0.95,
            'evidence': ['Evidence 1', 'Evidence 2']
        }
    
    def _combine_outputs(self, task_name: str, agent_outputs: Dict[str, Dict]) -> Dict[str, Any]:
        """Combine outputs from multiple agents into a final result."""
        # Get task validation requirements
        for category in self.tasks_config:
            if task_name in self.tasks_config[category]:
                task = self.tasks_config[category][task_name]
                validation = task['validation']
                
                # Combine confidences (e.g., take minimum)
                confidences = [
                    output.get('confidence', 0)
                    for output in agent_outputs.values()
                ]
                combined_confidence = min(confidences) if confidences else 0
                
                # Combine evidence
                combined_evidence = []
                for output in agent_outputs.values():
                    if 'evidence' in output:
                        combined_evidence.extend(output['evidence'])
                
                return {
                    'task': task_name,
                    'confidence': combined_confidence,
                    'evidence': combined_evidence,
                    'agent_outputs': agent_outputs,
                    'validation_passed': combined_confidence >= validation['confidence_threshold']
                }
        
        raise ValueError(f"Unknown task: {task_name}")

# Example usage:
if __name__ == '__main__':
    # Initialize crew
    crew = OncologyCrew()
    
    # Example task execution
    task_input = {
        'image_path': 'path/to/image.jpg',
        'report_text': 'Sample medical report text'
    }
    
    result = crew.execute_task('diagnosis', task_input)
    print(f"Task result: {result}")