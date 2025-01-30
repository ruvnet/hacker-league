"""
NOVA Cache Implementation for LLM Response Caching with Encryption
"""

import hashlib
import json
import os
import time
import asyncio
import random
from typing import Optional, Dict, Any
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class NovaCache:
    """Cache manager for NOVA system"""
    
    _instance = None
    _cache_dir = Path(__file__).parent / '.cache'
    _responses_file = _cache_dir / 'responses.enc'
    _key_file = _cache_dir / '.key'
    _responses: Dict[str, str] = {}
    _fernet = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NovaCache, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            # Create cache directory if it doesn't exist
            self._cache_dir.mkdir(parents=True, exist_ok=True)
            
            # Initialize encryption
            self._init_encryption()
            
            # Load cached responses if file exists
            if self._responses_file.exists():
                try:
                    with self._responses_file.open('rb') as f:
                        encrypted_data = f.read()
                        decrypted_data = self._fernet.decrypt(encrypted_data)
                        self._responses = json.loads(decrypted_data)
                    print(f"\nLoaded {len(self._responses)} cached responses\n")
                except Exception as e:
                    print(f"\nError loading cache: {e}\n")
                    self._responses = {}
            
            self._initialized = True
            self.metrics = {
                'hits': 0,
                'misses': 0
            }

    def _init_encryption(self):
        """Initialize encryption key and Fernet instance"""
        if self._key_file.exists():
            # Load existing key
            with self._key_file.open('rb') as f:
                key = f.read()
        else:
            # Generate new key
            salt = os.urandom(16)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            # Use a random password or environment variable
            password = os.getenv('NOVA_CACHE_KEY', os.urandom(32).hex()).encode()
            key = base64.urlsafe_b64encode(kdf.derive(password))
            # Save key
            with self._key_file.open('wb') as f:
                f.write(key)
        
        self._fernet = Fernet(key)

    def _generate_key(self, prompt: str) -> str:
        """Generate cache key from prompt"""
        # Normalize prompt
        normalized = prompt.lower().strip()
        # Generate hash
        return hashlib.sha256(normalized.encode()).hexdigest()

    def _save_responses(self):
        """Save encrypted responses to file"""
        try:
            # Encrypt responses before saving
            data = json.dumps(self._responses)
            encrypted_data = self._fernet.encrypt(data.encode())
            
            with self._responses_file.open('wb') as f:
                f.write(encrypted_data)
            print(f"\nSaved {len(self._responses)} encrypted responses to cache\n")
        except Exception as e:
            print(f"\nError saving cache: {e}\n")

    async def _stream_response(self, response: str, stream_speed: str = 'normal'):
        """Stream response with configurable speed"""
        # Configure delays based on speed setting
        if stream_speed == 'fast':
            char_delay = (0.001, 0.002)  # 1-2ms between chars
            chunk_delay = (0.02, 0.05)   # 20-50ms between chunks
        elif stream_speed == 'slow':
            char_delay = (0.03, 0.05)    # 30-50ms between chars
            chunk_delay = (0.5, 1.0)     # 500ms-1s between chunks
        else:  # normal
            char_delay = (0.005, 0.01)   # 5-10ms between chars
            chunk_delay = (0.05, 0.1)    # 50-100ms between chunks
        
        # Split response into chunks (sentences or phrases)
        chunks = response.split('. ')
        for i, chunk in enumerate(chunks):
            if i > 0:  # Add period back except for last chunk
                chunk = '. ' + chunk if i < len(chunks) - 1 else chunk
            
            # Stream each character with configured delay
            for char in chunk:
                print(char, end='', flush=True)
                await asyncio.sleep(random.uniform(*char_delay))
            
            if i < len(chunks) - 1:
                await asyncio.sleep(random.uniform(*chunk_delay))

    async def get_response(self, prompt: str, stream_speed: str = 'normal') -> Optional[str]:
        """Get cached response for prompt"""
        key = self._generate_key(prompt)
        
        if key in self._responses:
            self.metrics['hits'] += 1
            print(f"\nCache HIT for prompt: {prompt}\n")
            # Stream cached response
            await self._stream_response(self._responses[key], stream_speed)
            return self._responses[key]
            
        self.metrics['misses'] += 1
        print(f"\nCache MISS for prompt: {prompt}\n")
        return None

    async def set_response(self, prompt: str, response: str):
        """Cache response for prompt"""
        key = self._generate_key(prompt)
        self._responses[key] = response
        self._save_responses()

    def clear_cache(self):
        """Clear all cached responses"""
        self._responses = {}
        if self._responses_file.exists():
            self._responses_file.unlink()
        print("\nCache cleared successfully\n")

    def get_cache_size(self) -> int:
        """Get size of cache in bytes"""
        if self._responses_file.exists():
            return self._responses_file.stat().st_size
        return 0

    def get_cache_info(self) -> Dict[str, Any]:
        """Get detailed cache information"""
        return {
            'size_bytes': self.get_cache_size(),
            'num_entries': len(self._responses),
            'cache_file': str(self._responses_file),
            'encrypted': True,
            **self.get_metrics()
        }

    def get_metrics(self) -> Dict[str, Any]:
        """Get cache performance metrics"""
        total = self.metrics['hits'] + self.metrics['misses']
        hit_rate = (self.metrics['hits'] / total * 100) if total > 0 else 0
        return {
            **self.metrics,
            'hit_rate': hit_rate,
            'cache_size': len(self._responses)
        }
