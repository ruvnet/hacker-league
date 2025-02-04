"""
Oncology System Main Entry Point

This module provides the main entry point for the oncology system,
integrating the crew, cache, and tools for medical analysis.
"""

import os
import sys
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
import json

from .crew import OncologyCrew
from .cache import OncologyCache
from .tools.image_analyzer import ImageAnalysisTool
from .tools.text_analyzer import TextAnalysisTool
from .tools.knowledge_base import KnowledgeBaseTool

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class OncologySystem:
    """
    Main system class that coordinates all components for oncology analysis.
    """
    
    def __init__(self, config_dir: Optional[str] = None):
        """Initialize the oncology system."""
        self.config_dir = Path(config_dir) if config_dir else Path(__file__).parent / 'config'
        
        # Initialize components
        logger.info("Initializing oncology system components...")
        self.crew = OncologyCrew(config_dir=str(self.config_dir))
        self.cache = OncologyCache()
        
        # Track system state
        self.state = {
            'initialized': True,
            'last_task': None,
            'error_count': 0
        }
        
        logger.info("Oncology system initialized successfully")
    
    def analyze_case(self, 
                    case_data: Dict[str, Any],
                    task_type: str = 'diagnosis') -> Dict[str, Any]:
        """
        Analyze a medical case with specified data.
        
        Args:
            case_data: Dictionary containing case information:
                - image_path: Path to medical image (optional)
                - report_text: Clinical report text (optional)
                - genomic_data: Genomic data (optional)
            task_type: Type of analysis to perform (e.g., 'diagnosis', 'pathology_review')
        
        Returns:
            Dictionary containing analysis results
        """
        logger.info("Starting case analysis for task: %s", task_type)
        
        try:
            # Check cache first
            cache_key = f"{task_type}_{hash(str(case_data))}"
            cached_result = self.cache.get('llm', cache_key)
            if cached_result:
                logger.info("Using cached result for case")
                return cached_result
            
            # Execute task with crew
            result = self.crew.execute_task(task_type, case_data)
            
            # Cache successful result
            if result.get('validation_passed', False):
                self.cache.set('llm', cache_key, result)
            
            # Update system state
            self.state['last_task'] = {
                'type': task_type,
                'timestamp': result.get('timestamp'),
                'success': True
            }
            
            return result
            
        except Exception as e:
            logger.error("Case analysis failed: %s", str(e))
            self.state['error_count'] += 1
            raise
    
    def batch_analyze(self, 
                     cases: List[Dict[str, Any]],
                     task_type: str = 'diagnosis') -> List[Dict[str, Any]]:
        """
        Analyze multiple cases in batch mode.
        
        Args:
            cases: List of case data dictionaries
            task_type: Type of analysis to perform
        
        Returns:
            List of analysis results
        """
        logger.info("Starting batch analysis of %d cases", len(cases))
        results = []
        
        for i, case_data in enumerate(cases):
            try:
                logger.info("Processing case %d/%d", i+1, len(cases))
                result = self.analyze_case(case_data, task_type)
                results.append(result)
            except Exception as e:
                logger.error("Failed to process case %d: %s", i+1, str(e))
                results.append({
                    'error': str(e),
                    'case_index': i,
                    'success': False
                })
        
        return results
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status and statistics."""
        status = {
            'system_state': self.state,
            'cache_stats': self.cache.get_stats(),
            'crew_status': {
                'active_agents': len(self.crew.agents),
                'available_tools': len(self.crew.tools)
            }
        }
        
        return status
    
    def cleanup(self) -> None:
        """Cleanup system resources."""
        try:
            # Clear temporary files
            self.cache.clear()
            logger.info("System cleanup completed")
        except Exception as e:
            logger.error("Cleanup failed: %s", str(e))

def create_system(config_dir: Optional[str] = None) -> OncologySystem:
    """Factory function to create and configure the oncology system."""
    return OncologySystem(config_dir)

# Example usage:
if __name__ == '__main__':
    # Create system instance
    system = create_system()
    
    # Example case data
    case_data = {
        'image_path': 'path/to/image.jpg',
        'report_text': 'Example medical report text...',
        'genomic_data': {
            'variants': ['BRCA1:c.181T>G']
        }
    }
    
    try:
        # Analyze single case
        result = system.analyze_case(case_data)
        print(f"Analysis result: {json.dumps(result, indent=2)}")
        
        # Get system status
        status = system.get_system_status()
        print(f"System status: {json.dumps(status, indent=2)}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    finally:
        system.cleanup()