"""
Oncology System Cache Implementation

This module implements caching for the oncology system, following patterns from nova.
Caches API responses, analysis results, and tool outputs for efficiency.
"""

import json
import os
import time
from pathlib import Path
from typing import Dict, Any, Optional, Union
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OncologyCache:
    """
    Cache implementation for oncology system.
    Handles caching of:
    - LLM responses
    - Image analysis results
    - Report analysis results
    - Knowledge base queries
    """
    
    def __init__(self, cache_dir: Optional[str] = None):
        """Initialize the cache with configuration."""
        self.cache_dir = Path(cache_dir) if cache_dir else Path.home() / '.oncology_cache'
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories for different cache types
        self.llm_cache = self.cache_dir / 'llm'
        self.image_cache = self.cache_dir / 'image'
        self.report_cache = self.cache_dir / 'report'
        self.knowledge_cache = self.cache_dir / 'knowledge'
        
        for cache_path in [self.llm_cache, self.image_cache, 
                          self.report_cache, self.knowledge_cache]:
            cache_path.mkdir(exist_ok=True)
        
        # Load cache configuration
        self.config = {
            'llm_timeout': 3600,  # 1 hour
            'image_timeout': 86400,  # 24 hours
            'report_timeout': 86400,  # 24 hours
            'knowledge_timeout': 3600,  # 1 hour
            'max_cache_size': 1024 * 1024 * 1024  # 1GB
        }
        
        logger.info("Initialized oncology cache at %s", self.cache_dir)
    
    def _get_cache_path(self, cache_type: str, key: str) -> Path:
        """Get the cache file path for a given type and key."""
        cache_dirs = {
            'llm': self.llm_cache,
            'image': self.image_cache,
            'report': self.report_cache,
            'knowledge': self.knowledge_cache
        }
        
        if cache_type not in cache_dirs:
            raise ValueError(f"Unknown cache type: {cache_type}")
        
        # Use hash of key for filename to avoid path issues
        filename = f"{hash(key)}.json"
        return cache_dirs[cache_type] / filename
    
    def _is_cache_valid(self, cache_path: Path, timeout: int) -> bool:
        """Check if a cache entry is still valid based on timeout."""
        if not cache_path.exists():
            return False
        
        # Check file modification time
        mtime = cache_path.stat().st_mtime
        age = time.time() - mtime
        
        return age < timeout
    
    def get(self, cache_type: str, key: str) -> Optional[Dict[str, Any]]:
        """Get a value from the cache if it exists and is valid."""
        try:
            cache_path = self._get_cache_path(cache_type, key)
            timeout = self.config.get(f'{cache_type}_timeout', 3600)
            
            if self._is_cache_valid(cache_path, timeout):
                with open(cache_path) as f:
                    cached_data = json.load(f)
                logger.debug("Cache hit for %s: %s", cache_type, key)
                return cached_data
            else:
                if cache_path.exists():
                    # Clean up expired cache
                    cache_path.unlink()
                logger.debug("Cache miss (expired) for %s: %s", cache_type, key)
                return None
                
        except Exception as e:
            logger.warning("Cache get failed for %s: %s - %s", 
                         cache_type, key, str(e))
            return None
    
    def set(self, cache_type: str, key: str, value: Dict[str, Any]) -> bool:
        """Set a value in the cache."""
        try:
            cache_path = self._get_cache_path(cache_type, key)
            
            # Check cache size before writing
            if self._get_cache_size() >= self.config['max_cache_size']:
                self._cleanup_old_entries()
            
            # Write to cache
            with open(cache_path, 'w') as f:
                json.dump(value, f)
            
            logger.debug("Cached %s: %s", cache_type, key)
            return True
            
        except Exception as e:
            logger.warning("Cache set failed for %s: %s - %s",
                         cache_type, key, str(e))
            return False
    
    def _get_cache_size(self) -> int:
        """Get total size of all cache files in bytes."""
        total_size = 0
        for cache_dir in [self.llm_cache, self.image_cache,
                         self.report_cache, self.knowledge_cache]:
            for cache_file in cache_dir.glob('*.json'):
                total_size += cache_file.stat().st_size
        return total_size
    
    def _cleanup_old_entries(self) -> None:
        """Remove old cache entries to free up space."""
        logger.info("Cleaning up old cache entries")
        
        # Get all cache files with their modification times
        cache_files = []
        for cache_dir in [self.llm_cache, self.image_cache,
                         self.report_cache, self.knowledge_cache]:
            for cache_file in cache_dir.glob('*.json'):
                cache_files.append((cache_file, cache_file.stat().st_mtime))
        
        # Sort by modification time (oldest first)
        cache_files.sort(key=lambda x: x[1])
        
        # Remove oldest files until under size limit
        while (self._get_cache_size() >= self.config['max_cache_size'] 
               and cache_files):
            old_file = cache_files.pop(0)[0]
            old_file.unlink()
            logger.debug("Removed old cache file: %s", old_file)
    
    def clear(self, cache_type: Optional[str] = None) -> None:
        """Clear cache entries of specified type or all if none specified."""
        try:
            if cache_type:
                cache_dir = self._get_cache_path(cache_type, '').parent
                for cache_file in cache_dir.glob('*.json'):
                    cache_file.unlink()
                logger.info("Cleared %s cache", cache_type)
            else:
                for cache_dir in [self.llm_cache, self.image_cache,
                                self.report_cache, self.knowledge_cache]:
                    for cache_file in cache_dir.glob('*.json'):
                        cache_file.unlink()
                logger.info("Cleared all caches")
                
        except Exception as e:
            logger.error("Cache clear failed: %s", str(e))
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        stats = {
            'total_size_bytes': self._get_cache_size(),
            'cache_types': {}
        }
        
        for cache_type in ['llm', 'image', 'report', 'knowledge']:
            cache_dir = self._get_cache_path(cache_type, '').parent
            cache_files = list(cache_dir.glob('*.json'))
            
            type_stats = {
                'entry_count': len(cache_files),
                'size_bytes': sum(f.stat().st_size for f in cache_files),
                'oldest_entry': min((f.stat().st_mtime for f in cache_files), 
                                  default=None),
                'newest_entry': max((f.stat().st_mtime for f in cache_files),
                                  default=None)
            }
            
            if type_stats['oldest_entry']:
                type_stats['oldest_entry'] = datetime.fromtimestamp(
                    type_stats['oldest_entry']
                ).isoformat()
            if type_stats['newest_entry']:
                type_stats['newest_entry'] = datetime.fromtimestamp(
                    type_stats['newest_entry']
                ).isoformat()
            
            stats['cache_types'][cache_type] = type_stats
        
        return stats

# Example usage:
if __name__ == '__main__':
    # Initialize cache
    cache = OncologyCache()
    
    # Example cache operations
    cache.set('llm', 'test_key', {'response': 'test_value'})
    cached_value = cache.get('llm', 'test_key')
    print(f"Cached value: {cached_value}")
    
    # Print cache stats
    stats = cache.get_stats()
    print(f"Cache stats: {json.dumps(stats, indent=2)}")