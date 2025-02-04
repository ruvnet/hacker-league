"""
Pytest configuration for oncology system tests.
"""

import os
import json
import pytest
from pathlib import Path

# Create sample test data
@pytest.fixture(scope="session")
def sample_data_dir():
    """Create and populate sample data directory for tests."""
    data_dir = Path(__file__).parent / "sample_data"
    data_dir.mkdir(exist_ok=True)
    
    # Create sample report
    report_path = data_dir / "report.txt"
    if not report_path.exists():
        report_text = """
Clinical History:
65-year-old male with suspicious lung mass found on screening CT.

Findings:
2.5 cm spiculated mass in right upper lobe, anterior segment.
No mediastinal lymphadenopathy.
No pleural effusion.

Impression:
Findings highly concerning for primary lung malignancy.
Recommend PET/CT for staging.
"""
        report_path.write_text(report_text)
    
    # Create sample image (text representation for testing)
    image_path = data_dir / "image.txt"
    if not image_path.exists():
        image_data = {
            "type": "ct_scan",
            "dimensions": [512, 512, 128],
            "pixel_spacing": [0.7, 0.7, 1.0],
            "findings": {
                "mass": {
                    "location": "RUL",
                    "size_mm": 25,
                    "characteristics": ["spiculated", "solid"]
                }
            }
        }
        image_path.write_text(json.dumps(image_data, indent=2))
    
    # Create sample genomic data
    genomic_path = data_dir / "variants.vcf"
    if not genomic_path.exists():
        vcf_content = """##fileformat=VCFv4.2
##source=TestData
#CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO
chr7    55249071        .       T       G       100     PASS    GENE=EGFR;EFFECT=missense
"""
        genomic_path.write_text(vcf_content)
    
    return data_dir

# Environment setup
@pytest.fixture(scope="session", autouse=True)
def setup_test_env():
    """Setup test environment variables."""
    # Store original env vars
    original_env = {}
    test_env = {
        'OPENROUTER_API_KEY': 'test_key',
        'CACHE_DIR': str(Path(__file__).parent / 'test_cache'),
        'LOG_LEVEL': 'DEBUG'
    }
    
    # Set test env vars
    for key, value in test_env.items():
        if key in os.environ:
            original_env[key] = os.environ[key]
        os.environ[key] = value
    
    yield
    
    # Restore original env vars
    for key in test_env:
        if key in original_env:
            os.environ[key] = original_env[key]
        else:
            del os.environ[key]

# Mock OpenRouter responses
@pytest.fixture
def mock_openrouter_response():
    """Mock response from OpenRouter API."""
    return {
        "id": "test_response_id",
        "choices": [{
            "message": {
                "content": """Analysis Result:
- Suspicious mass in right upper lobe
- Features suggest primary lung malignancy
- Recommend further staging

Confidence: 0.92
Evidence:
1. Spiculated mass morphology
2. Size > 2cm
3. Location in RUL"""
            }
        }]
    }

# Test configurations
@pytest.fixture
def test_config():
    """Test configuration settings."""
    return {
        'models': {
            'medical_expert': {
                'llm': 'anthropic/claude-3-opus-20240229',
                'role': 'Medical Expert',
                'verbose': True
            }
        },
        'tasks': {
            'diagnosis': {
                'required_agents': ['medical_expert'],
                'tools': ['image_analysis', 'report_analysis'],
                'validation': {
                    'confidence_threshold': 0.85
                }
            }
        }
    }

# Cleanup fixture
@pytest.fixture(autouse=True)
def cleanup_test_files():
    """Clean up test files after each test."""
    yield
    
    # Paths to clean up
    cleanup_paths = [
        Path(__file__).parent / 'test_cache',
        Path(__file__).parent / 'test_output'
    ]
    
    for path in cleanup_paths:
        if path.exists():
            if path.is_file():
                path.unlink()
            else:
                import shutil
                shutil.rmtree(path)

# Test metrics
@pytest.fixture
def performance_metrics():
    """Define expected performance metrics for tests."""
    return {
        'accuracy_threshold': 0.90,
        'min_confidence': 0.85,
        'max_latency_seconds': 5.0,
        'min_evidence_count': 2
    }

# Custom markers
def pytest_configure(config):
    """Configure custom pytest markers."""
    markers = [
        "integration: mark test as integration test",
        "slow: mark test as slow running",
        "gpu: mark test as requiring GPU",
        "medical: mark test as requiring medical domain knowledge"
    ]
    for marker in markers:
        config.addinivalue_line("markers", marker)

# Test reporting
@pytest.fixture(scope="session")
def test_report_dir():
    """Create and manage test report directory."""
    report_dir = Path(__file__).parent / "test_reports"
    report_dir.mkdir(exist_ok=True)
    return report_dir

def pytest_runtest_makereport(item, call):
    """Custom test reporting logic."""
    if call.when == "call":
        # Add custom reporting logic here if needed
        pass