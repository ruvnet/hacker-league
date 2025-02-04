"""
Tests for the oncology system cache implementation.
"""

import os
import json
import time
import shutil
import pytest
from pathlib import Path
from datetime import datetime, timedelta

from oncology.cache import OncologyCache

# Test data
TEST_CACHE_DIR = Path(__file__).parent / "test_cache"
LARGE_DATA = {"data": "x" * 1024 * 1024}  # 1MB of data

@pytest.fixture
def cache():
    """Create a cache instance for testing."""
    # Setup
    if TEST_CACHE_DIR.exists():
        shutil.rmtree(TEST_CACHE_DIR)
    
    cache = OncologyCache(cache_dir=str(TEST_CACHE_DIR))
    
    yield cache
    
    # Teardown
    if TEST_CACHE_DIR.exists():
        shutil.rmtree(TEST_CACHE_DIR)

def test_cache_initialization(cache):
    """Test cache initialization."""
    assert TEST_CACHE_DIR.exists()
    assert (TEST_CACHE_DIR / 'llm').exists()
    assert (TEST_CACHE_DIR / 'image').exists()
    assert (TEST_CACHE_DIR / 'report').exists()
    assert (TEST_CACHE_DIR / 'knowledge').exists()

def test_basic_cache_operations(cache):
    """Test basic cache set/get operations."""
    # Test data
    test_data = {
        'result': 'test result',
        'timestamp': datetime.now().isoformat()
    }
    
    # Set cache
    assert cache.set('llm', 'test_key', test_data)
    
    # Get cache
    cached_data = cache.get('llm', 'test_key')
    assert cached_data is not None
    assert cached_data['result'] == test_data['result']

def test_cache_expiration(cache):
    """Test cache expiration."""
    test_data = {'result': 'test result'}
    
    # Override timeout for testing
    cache.config['llm_timeout'] = 1  # 1 second timeout
    
    # Set cache
    cache.set('llm', 'test_key', test_data)
    
    # Immediate get should work
    assert cache.get('llm', 'test_key') is not None
    
    # Wait for expiration
    time.sleep(1.1)
    
    # Get after expiration should return None
    assert cache.get('llm', 'test_key') is None

def test_cache_size_limit(cache):
    """Test cache size limiting."""
    # Set small cache size limit for testing
    cache.config['max_cache_size'] = 2 * 1024 * 1024  # 2MB
    
    # Add multiple large entries
    for i in range(3):  # Should exceed 2MB total
        cache.set('llm', f'large_key_{i}', LARGE_DATA)
    
    # Check that cache size is maintained
    assert cache._get_cache_size() <= cache.config['max_cache_size']

def test_cache_cleanup(cache):
    """Test cache cleanup functionality."""
    # Add some entries
    for i in range(3):
        cache.set('llm', f'key_{i}', {'data': f'value_{i}'})
    
    # Clear specific cache type
    cache.clear('llm')
    assert cache.get('llm', 'key_0') is None
    
    # Add more entries
    cache.set('image', 'img_key', {'data': 'image_data'})
    
    # Clear all caches
    cache.clear()
    assert cache.get('image', 'img_key') is None

def test_cache_stats(cache):
    """Test cache statistics reporting."""
    # Add some test data
    cache.set('llm', 'key1', {'data': 'value1'})
    cache.set('image', 'key2', {'data': 'value2'})
    
    stats = cache.get_stats()
    
    assert isinstance(stats, dict)
    assert 'total_size_bytes' in stats
    assert 'cache_types' in stats
    assert all(t in stats['cache_types'] for t in ['llm', 'image', 'report', 'knowledge'])

def test_concurrent_access(cache):
    """Test concurrent cache access."""
    import threading
    
    def cache_operation(thread_id):
        # Each thread writes and reads multiple times
        for i in range(10):
            key = f'thread_{thread_id}_key_{i}'
            data = {'thread': thread_id, 'iteration': i}
            
            # Write
            cache.set('llm', key, data)
            
            # Read
            cached = cache.get('llm', key)
            assert cached is not None
            assert cached['thread'] == thread_id
            assert cached['iteration'] == i
    
    # Create multiple threads
    threads = [
        threading.Thread(target=cache_operation, args=(i,))
        for i in range(5)
    ]
    
    # Start all threads
    for t in threads:
        t.start()
    
    # Wait for all threads to complete
    for t in threads:
        t.join()

def test_invalid_cache_type(cache):
    """Test handling of invalid cache types."""
    with pytest.raises(ValueError):
        cache.get('invalid_type', 'key')
    
    with pytest.raises(ValueError):
        cache.set('invalid_type', 'key', {'data': 'value'})

def test_cache_persistence(cache):
    """Test cache persistence across instances."""
    # First instance
    cache.set('llm', 'persist_key', {'data': 'persist_value'})
    
    # Create new instance pointing to same directory
    new_cache = OncologyCache(cache_dir=str(TEST_CACHE_DIR))
    
    # Check if data persisted
    cached_data = new_cache.get('llm', 'persist_key')
    assert cached_data is not None
    assert cached_data['data'] == 'persist_value'

def test_different_data_types(cache):
    """Test caching different data types."""
    test_cases = [
        ('string_data', 'test string'),
        ('int_data', 42),
        ('float_data', 3.14),
        ('list_data', [1, 2, 3]),
        ('dict_data', {'key': 'value'}),
        ('bool_data', True),
        ('none_data', None)
    ]
    
    for key, value in test_cases:
        # Wrap in dict as cache expects dict
        cache.set('llm', key, {'value': value})
        cached = cache.get('llm', key)
        assert cached['value'] == value

def test_cache_error_handling(cache):
    """Test error handling in cache operations."""
    # Test with non-serializable data
    class NonSerializable:
        pass
    
    with pytest.raises(Exception):
        cache.set('llm', 'bad_key', {'data': NonSerializable()})
    
    # Test with invalid file permissions
    # Make cache directory read-only
    os.chmod(TEST_CACHE_DIR, 0o444)
    
    # Attempt to write should fail gracefully
    assert not cache.set('llm', 'test_key', {'data': 'value'})
    
    # Restore permissions for cleanup
    os.chmod(TEST_CACHE_DIR, 0o777)

if __name__ == '__main__':
    pytest.main([__file__, '-v'])