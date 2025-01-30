"""
NOVA Cache Implementation for LLM Response Caching
"""

import hashlib
import json
import os
import time
import asyncio
import random
from typing import Optional, Dict, Any
from pathlib import Path

class NovaCache:
    """Cache manager for NOVA system"""
    
    _instance = None
    _cache_dir = Path(__file__).parent / '.cache'
    _responses_file = _cache_dir / 'responses.json'
    _responses: Dict[str, str] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NovaCache, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            # Create cache directory if it doesn't exist
            self._cache_dir.mkdir(parents=True, exist_ok=True)
            
            # Load cached responses if file exists
            if self._responses_file.exists():
                try:
                    with self._responses_file.open('r') as f:
                        self._responses = json.load(f)
                    print(f"\nLoaded {len(self._responses)} cached responses\n")
                except Exception as e:
                    print(f"\nError loading cache: {e}\n")
                    self._responses = {}
            
            self._initialized = True
            self.metrics = {
                'hits': 0,
                'misses': 0
            }

    def _generate_key(self, prompt: str) -> str:
        """Generate cache key from prompt"""
        # Normalize prompt
        normalized = prompt.lower().strip()
        # Generate hash
        return hashlib.sha256(normalized.encode()).hexdigest()

    def _save_responses(self):
        """Save responses to file"""
        try:
            with self._responses_file.open('w') as f:
                json.dump(self._responses, f, indent=2)
            print(f"\nSaved {len(self._responses)} responses to cache\n")
        except Exception as e:
            print(f"\nError saving cache: {e}\n")

    async def _stream_response(self, response: str):
        """Stream response with realistic but faster delays for cached content"""
        # Split response into chunks (sentences or phrases)
        chunks = response.split('. ')
        for i, chunk in enumerate(chunks):
            if i > 0:  # Add period back except for last chunk
                chunk = '. ' + chunk if i < len(chunks) - 1 else chunk
            
            # Stream each character with minimal delay
            for char in chunk:
                print(char, end='', flush=True)
                # Very fast typing speed (5-10ms between chars)
                await asyncio.sleep(random.uniform(0.005, 0.01))
            
            if i < len(chunks) - 1:
                # Brief pause between chunks (50-100ms)
                await asyncio.sleep(random.uniform(0.05, 0.1))

    async def get_response(self, prompt: str) -> Optional[str]:
        """Get cached response for prompt"""
        key = self._generate_key(prompt)
        
        if key in self._responses:
            self.metrics['hits'] += 1
            print(f"\nCache HIT for prompt: {prompt}\n")
            # Stream cached response
            await self._stream_response(self._responses[key])
            return self._responses[key]
            
        self.metrics['misses'] += 1
        print(f"\nCache MISS for prompt: {prompt}\n")
        return None

    async def set_response(self, prompt: str, response: str):
        """Cache response for prompt"""
        key = self._generate_key(prompt)
        self._responses[key] = response
        self._save_responses()

    def get_metrics(self) -> Dict[str, Any]:
        """Get cache performance metrics"""
        total = self.metrics['hits'] + self.metrics['misses']
        hit_rate = (self.metrics['hits'] / total * 100) if total > 0 else 0
        return {
            **self.metrics,
            'hit_rate': hit_rate,
            'cache_size': len(self._responses)
        }
