"""
Tests for the main oncology system integration.
"""

import os
import json
import pytest
from pathlib import Path
from unittest.mock import Mock, patch

from oncology.main import OncologySystem, create_system

# Test data
SAMPLE_REPORT = """
Clinical History: 65-year-old male with suspicious lung mass
Findings: 2.5 cm spiculated mass in right upper lobe
Impression: Findings highly concerning for primary lung malignancy
"""

SAMPLE_GENOMIC_DATA = {
    'variants': ['EGFR:p.L858R'],
    'expression': {
        'EGFR': 2.5,
        'TP53': -1.2
    }
}

SAMPLE_IMAGE_PATH = Path(__file__).parent / "sample_data/image.txt"
SAMPLE_CONFIG_DIR = Path(__file__).parent.parent / "config"

@pytest.fixture
def system():
    """Create a system instance for testing."""
    return create_system(str(SAMPLE_CONFIG_DIR))

def test_system_initialization(system):
    """Test system initialization."""
    assert system.crew is not None
    assert system.cache is not None
    assert system.state['initialized']
    assert system.state['error_count'] == 0

def test_analyze_case(system):
    """Test analyzing a single case."""
    case_data = {
        'image_path': str(SAMPLE_IMAGE_PATH),
        'report_text': SAMPLE_REPORT,
        'genomic_data': SAMPLE_GENOMIC_DATA
    }
    
    result = system.analyze_case(case_data, 'diagnosis')
    
    assert isinstance(result, dict)
    assert result.get('validation_passed', False)
    assert 'confidence' in result
    assert 'evidence' in result

def test_cache_usage(system):
    """Test cache usage in analysis."""
    case_data = {
        'image_path': str(SAMPLE_IMAGE_PATH),
        'report_text': SAMPLE_REPORT
    }
    
    # First analysis should miss cache
    result1 = system.analyze_case(case_data)
    
    # Second analysis should hit cache
    result2 = system.analyze_case(case_data)
    
    assert result1 == result2

@patch('openai.ChatCompletion.create')
def test_llm_integration(mock_openai, system):
    """Test LLM integration with mocked OpenAI."""
    mock_openai.return_value = Mock(
        choices=[Mock(message=Mock(content="Test analysis response"))]
    )
    
    case_data = {
        'report_text': SAMPLE_REPORT
    }
    
    result = system.analyze_case(case_data, 'diagnosis')
    assert mock_openai.called
    assert result is not None

def test_batch_analysis(system):
    """Test batch analysis of multiple cases."""
    cases = [
        {
            'image_path': str(SAMPLE_IMAGE_PATH),
            'report_text': SAMPLE_REPORT
        },
        {
            'report_text': SAMPLE_REPORT,
            'genomic_data': SAMPLE_GENOMIC_DATA
        }
    ]
    
    results = system.batch_analyze(cases)
    
    assert len(results) == len(cases)
    assert all(isinstance(r, dict) for r in results)
    assert all('success' in r for r in results)

def test_error_handling(system):
    """Test error handling in analysis."""
    # Test with invalid image path
    case_data = {
        'image_path': 'invalid/path.jpg',
        'report_text': SAMPLE_REPORT
    }
    
    with pytest.raises(Exception):
        system.analyze_case(case_data)
    
    assert system.state['error_count'] > 0

def test_system_status(system):
    """Test system status reporting."""
    status = system.get_system_status()
    
    assert isinstance(status, dict)
    assert 'system_state' in status
    assert 'cache_stats' in status
    assert 'crew_status' in status

@pytest.mark.parametrize("task_type", [
    'diagnosis',
    'pathology_review',
    'radiology_review',
    'genomic_analysis'
])
def test_different_task_types(system, task_type):
    """Test different types of analysis tasks."""
    case_data = {
        'image_path': str(SAMPLE_IMAGE_PATH),
        'report_text': SAMPLE_REPORT,
        'genomic_data': SAMPLE_GENOMIC_DATA
    }
    
    result = system.analyze_case(case_data, task_type)
    assert result is not None
    assert result.get('validation_passed', False)

def test_cleanup(system):
    """Test system cleanup."""
    # Create some cache entries
    case_data = {
        'report_text': SAMPLE_REPORT
    }
    system.analyze_case(case_data)
    
    # Verify cache has entries
    status_before = system.get_system_status()
    assert status_before['cache_stats']['total_size_bytes'] > 0
    
    # Cleanup
    system.cleanup()
    
    # Verify cache is cleared
    status_after = system.get_system_status()
    assert status_after['cache_stats']['total_size_bytes'] == 0

@pytest.mark.integration
def test_full_integration(system):
    """Full integration test with all components."""
    # Prepare test data
    case_data = {
        'image_path': str(SAMPLE_IMAGE_PATH),
        'report_text': SAMPLE_REPORT,
        'genomic_data': SAMPLE_GENOMIC_DATA
    }
    
    try:
        # Run analysis
        result = system.analyze_case(case_data, 'multi_modal_diagnosis')
        
        # Verify result structure
        assert result['validation_passed']
        assert result['confidence'] >= 0.85
        assert len(result['evidence']) > 0
        
        # Check cache
        cache_stats = system.get_system_status()['cache_stats']
        assert cache_stats['total_size_bytes'] > 0
        
        # Verify crew status
        crew_status = system.get_system_status()['crew_status']
        assert crew_status['active_agents'] > 0
        assert crew_status['available_tools'] > 0
        
    finally:
        # Cleanup
        system.cleanup()

def test_concurrent_analysis(system):
    """Test concurrent analysis requests."""
    import concurrent.futures
    
    case_data = {
        'image_path': str(SAMPLE_IMAGE_PATH),
        'report_text': SAMPLE_REPORT
    }
    
    # Run multiple analyses concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(system.analyze_case, case_data)
            for _ in range(3)
        ]
        
        results = [f.result() for f in futures]
        
        # Verify all analyses completed successfully
        assert len(results) == 3
        assert all(r.get('validation_passed', False) for r in results)

if __name__ == '__main__':
    pytest.main([__file__, '-v'])