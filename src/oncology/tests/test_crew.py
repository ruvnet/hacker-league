"""
Tests for the oncology crew system with OpenRouter integration.
"""

import os
import pytest
from pathlib import Path
from unittest.mock import Mock, patch

from oncology.crew import OncologyCrew
from oncology.cache import OncologyCache

# Test data
SAMPLE_REPORT = """
Clinical History: 65-year-old male with suspicious lung mass
Findings: 2.5 cm spiculated mass in right upper lobe
Impression: Findings highly concerning for primary lung malignancy
"""

SAMPLE_IMAGE_PATH = Path(__file__).parent / "sample_data/image.txt"
SAMPLE_CONFIG_DIR = Path(__file__).parent.parent / "config"

@pytest.fixture
def crew():
    """Create a crew instance for testing."""
    return OncologyCrew(config_dir=str(SAMPLE_CONFIG_DIR))

@pytest.fixture
def cache():
    """Create a cache instance for testing."""
    return OncologyCache(cache_dir=str(Path(__file__).parent / "test_cache"))

def test_crew_initialization(crew):
    """Test crew initialization with config."""
    assert crew.agents is not None
    assert 'medical_expert' in crew.agents
    assert 'image_analyst' in crew.agents
    assert 'genomics_expert' in crew.agents

def test_get_task_crew(crew):
    """Test getting required crew for a task."""
    task_crew = crew.get_task_crew('diagnosis')
    assert 'medical_expert' in task_crew
    assert 'image_analyst' in task_crew

def test_get_task_tools(crew):
    """Test getting required tools for a task."""
    task_tools = crew.get_task_tools('diagnosis')
    assert 'image_analysis' in task_tools
    assert 'report_analysis' in task_tools

@patch('openai.ChatCompletion.create')
def test_process_with_agent(mock_openai, crew):
    """Test processing with an agent using mocked OpenAI."""
    # Mock OpenAI response
    mock_openai.return_value = Mock(
        choices=[Mock(message=Mock(content="Test analysis response"))]
    )
    
    # Test context
    context = {
        'task': 'diagnosis',
        'inputs': {
            'report_text': SAMPLE_REPORT,
            'image_path': str(SAMPLE_IMAGE_PATH)
        },
        'intermediate_results': {},
        'tools_used': []
    }
    
    # Process with medical expert agent
    agent = crew.agents['medical_expert']
    result = crew._process_with_agent(agent, context)
    
    # Verify result structure
    assert isinstance(result, dict)
    assert 'analysis' in result
    assert 'confidence' in result
    assert 'evidence' in result

def test_validate_task_output(crew):
    """Test task output validation."""
    # Valid output
    valid_output = {
        'confidence': 0.95,
        'evidence': ['Finding 1', 'Finding 2'],
        'measurements': {'size': '2.5cm'}
    }
    assert crew.validate_task_output('diagnosis', valid_output)
    
    # Invalid output (low confidence)
    invalid_output = {
        'confidence': 0.5,
        'evidence': ['Finding 1']
    }
    assert not crew.validate_task_output('diagnosis', invalid_output)

@pytest.mark.integration
def test_execute_task_integration(crew):
    """Integration test for task execution."""
    inputs = {
        'report_text': SAMPLE_REPORT,
        'image_path': str(SAMPLE_IMAGE_PATH)
    }
    
    result = crew.execute_task('diagnosis', inputs)
    
    # Verify result structure
    assert isinstance(result, dict)
    assert 'task' in result
    assert 'confidence' in result
    assert 'evidence' in result
    assert 'validation_passed' in result

def test_cache_integration(crew, cache):
    """Test integration between crew and cache."""
    # Execute task
    inputs = {
        'report_text': SAMPLE_REPORT,
        'image_path': str(SAMPLE_IMAGE_PATH)
    }
    
    # First execution should miss cache
    result1 = crew.execute_task('diagnosis', inputs)
    
    # Cache the result
    cache_key = f"diagnosis_{hash(str(inputs))}"
    cache.set('llm', cache_key, result1)
    
    # Second execution should hit cache
    cached_result = cache.get('llm', cache_key)
    assert cached_result is not None
    assert cached_result == result1

@pytest.mark.parametrize("task_name", [
    'diagnosis',
    'pathology_review',
    'radiology_review'
])
def test_different_task_types(crew, task_name):
    """Test execution of different task types."""
    inputs = {
        'report_text': SAMPLE_REPORT,
        'image_path': str(SAMPLE_IMAGE_PATH)
    }
    
    result = crew.execute_task(task_name, inputs)
    assert result['task'] == task_name
    assert result['validation_passed']

def test_error_handling(crew):
    """Test error handling in crew."""
    # Test with invalid task
    with pytest.raises(ValueError):
        crew.execute_task('invalid_task', {})
    
    # Test with missing required input
    with pytest.raises(Exception):
        crew.execute_task('diagnosis', {'report_text': None, 'image_path': None})

def test_concurrent_tasks(crew):
    """Test handling multiple tasks concurrently."""
    import concurrent.futures
    
    inputs = {
        'report_text': SAMPLE_REPORT,
        'image_path': str(SAMPLE_IMAGE_PATH)
    }
    
    # Execute multiple tasks concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(crew.execute_task, 'diagnosis', inputs)
            for _ in range(3)
        ]
        
        results = [f.result() for f in futures]
        
        # Verify all tasks completed successfully
        assert all(r['validation_passed'] for r in results)
        assert len(results) == 3

if __name__ == '__main__':
    pytest.main([__file__, '-v'])