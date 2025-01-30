"""
NOVA Cache Implementation for Intermediate Results
"""

from typing import Any, Dict, Optional, TypeVar, Callable
from datetime import datetime, timedelta
import asyncio
import hashlib
import json
import threading
import re

T = TypeVar('T')

class NovaCache:
    """Cache manager for NOVA system"""
    
    _instance = None
    _lock = threading.Lock()
    _cleanup_task = None
    
    def __new__(cls, ttl: int = 3600):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(NovaCache, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance
    
    def __init__(self, ttl: int = 3600):
        with self._lock:
            if not self._initialized:
                self.api_cache: Dict[str, Dict[str, Any]] = {}
                self.inference_cache: Dict[str, Dict[str, Any]] = {}
                self.ttl = ttl  # Time to live in seconds
                self.metrics = {
                    'hits': 0,
                    'misses': 0,
                    'evictions': 0
                }
                self._initialized = True
                self._running = True

    def _normalize_content(self, content: str) -> str:
        """Normalize message content for consistent caching"""
        # Remove extra whitespace
        content = re.sub(r'\s+', ' ', content.strip())
        # Convert to lowercase
        content = content.lower()
        # Remove punctuation
        content = re.sub(r'[^\w\s]', '', content)
        return content

    def _generate_key(self, data: Any) -> str:
        """Generate cache key from input data"""
        if isinstance(data, str):
            # Normalize string content
            serialized = self._normalize_content(data)
        elif isinstance(data, dict):
            # For message-based queries, only use role and normalized content
            if 'messages' in data:
                cleaned_messages = []
                for msg in data['messages']:
                    cleaned_msg = {
                        'role': msg['role'],
                        'content': self._normalize_content(msg['content'])
                    }
                    cleaned_messages.append(cleaned_msg)
                cleaned_data = {
                    'messages': cleaned_messages
                }
                if 'model' in data:
                    cleaned_data['model'] = data['model']
                serialized = json.dumps(cleaned_data, sort_keys=True)
                print(f"\nGenerated cache key for messages: {serialized}\n")
            else:
                # Remove any non-deterministic fields
                cleaned_data = {
                    k: v for k, v in sorted(data.items())
                    if k not in ['timestamp', 'request_id', 'session_id']
                }
                serialized = json.dumps(cleaned_data, sort_keys=True)
        else:
            serialized = json.dumps(data, sort_keys=True)
        
        # Use SHA-256 for consistent hashing
        key = hashlib.sha256(serialized.encode()).hexdigest()
        print(f"\nCache key: {key} for data type: {type(data)}\n")
        return key

    def _is_expired(self, timestamp: datetime) -> bool:
        """Check if cache entry is expired"""
        return (datetime.now() - timestamp).total_seconds() > self.ttl

    async def get_api_result(self, query: Any) -> Optional[Any]:
        """Get cached API result"""
        key = self._generate_key(query)
        print(f"\nChecking cache for key: {key}")
        print(f"Current cache keys: {list(self.api_cache.keys())}\n")
        
        if key in self.api_cache:
            entry = self.api_cache[key]
            if not self._is_expired(entry['timestamp']):
                self.metrics['hits'] += 1
                print(f"\nCache HIT for key: {key}\n")
                return entry['result']
            else:
                del self.api_cache[key]
                self.metrics['evictions'] += 1
                print(f"\nCache EXPIRED for key: {key}\n")
        self.metrics['misses'] += 1
        print(f"\nCache MISS for key: {key}\n")
        return None

    async def set_api_result(self, query: Any, result: Any) -> None:
        """Cache API result"""
        key = self._generate_key(query)
        print(f"\nCaching result for key: {key}\n")
        self.api_cache[key] = {
            'result': result,
            'timestamp': datetime.now()
        }

    async def get_inference(self, query: Any) -> Optional[Any]:
        """Get cached inference result"""
        key = self._generate_key(query)
        print(f"\nChecking inference cache for key: {key}")
        print(f"Current inference cache keys: {list(self.inference_cache.keys())}\n")
        
        if key in self.inference_cache:
            entry = self.inference_cache[key]
            if not self._is_expired(entry['timestamp']):
                self.metrics['hits'] += 1
                print(f"\nInference cache HIT for key: {key}\n")
                return entry['result']
            else:
                del self.inference_cache[key]
                self.metrics['evictions'] += 1
                print(f"\nInference cache EXPIRED for key: {key}\n")
        self.metrics['misses'] += 1
        print(f"\nInference cache MISS for key: {key}\n")
        return None

    async def set_inference(self, query: Any, result: Any) -> None:
        """Cache inference result"""
        key = self._generate_key(query)
        print(f"\nCaching inference result for key: {key}\n")
        self.inference_cache[key] = {
            'result': result,
            'timestamp': datetime.now()
        }

    async def get_or_compute(self, 
                           key: Any, 
                           compute_fn: Callable[[], T], 
                           cache_type: str = 'api') -> T:
        """Get from cache or compute and cache result"""
        if cache_type == 'api':
            result = await self.get_api_result(key)
            if result is not None:
                return result
            result = await compute_fn()
            await self.set_api_result(key, result)
            return result
        else:
            result = await self.get_inference(key)
            if result is not None:
                return result
            result = await compute_fn()
            await self.set_inference(key, result)
            return result

    def get_metrics(self) -> Dict[str, float]:
        """Get cache performance metrics"""
        total = self.metrics['hits'] + self.metrics['misses']
        hit_rate = (self.metrics['hits'] / total * 100) if total > 0 else 0
        return {
            **self.metrics,
            'hit_rate': hit_rate,
            'api_cache_size': len(self.api_cache),
            'inference_cache_size': len(self.inference_cache)
        }

    async def cleanup(self) -> None:
        """Remove expired entries"""
        if not self._running:
            return
            
        now = datetime.now()
        
        # Cleanup API cache
        expired_api = [
            key for key, entry in self.api_cache.items()
            if self._is_expired(entry['timestamp'])
        ]
        for key in expired_api:
            del self.api_cache[key]
            self.metrics['evictions'] += 1
            print(f"\nEvicted API cache entry: {key}\n")
            
        # Cleanup inference cache
        expired_inference = [
            key for key, entry in self.inference_cache.items()
            if self._is_expired(entry['timestamp'])
        ]
        for key in expired_inference:
            del self.inference_cache[key]
            self.metrics['evictions'] += 1
            print(f"\nEvicted inference cache entry: {key}\n")

    async def start_cleanup_task(self) -> None:
        """Start periodic cleanup task"""
        if self._cleanup_task is not None:
            return
            
        self._running = True
        while self._running:
            await self.cleanup()
            await asyncio.sleep(self.ttl / 2)  # Run cleanup at half TTL interval
            
    def stop_cleanup_task(self) -> None:
        """Stop the cleanup task"""
        self._running = False
        
    def __del__(self):
        """Cleanup on deletion"""
        self.stop_cleanup_task()
