"""
NOVA CLI Entry Point
"""

import argparse
import asyncio
from nova.crew import NovaCrew
from nova.cache import NovaCache

def format_size(size_bytes: int) -> str:
    """Format size in bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} TB"

def main():
    parser = argparse.ArgumentParser(description='NOVA (Neuro-Symbolic Optimized Versatile Agent)')
    
    # Task options
    parser.add_argument('--prompt', type=str, default="Tell me about yourself",
                      help='The prompt to process')
    parser.add_argument('--task', type=str, choices=['research', 'execute', 'analyze', 'both'],
                      default='both', help='Type of task to perform')
    
    # Cache management options
    cache_group = parser.add_argument_group('Cache Management')
    cache_group.add_argument('--clear-cache', action='store_true',
                          help='Clear the response cache')
    cache_group.add_argument('--cache-info', action='store_true',
                          help='Show cache information')
    cache_group.add_argument('--stream-speed', type=str,
                          choices=['fast', 'normal', 'slow'], default='normal',
                          help='Speed of response streaming')
    
    args = parser.parse_args()
    
    # Handle cache management commands
    cache = NovaCache()
    
    if args.clear_cache:
        cache.clear_cache()
        print("Cache cleared successfully")
        return
        
    if args.cache_info:
        info = cache.get_cache_info()
        print("\nNOVA Cache Information:")
        print("----------------------")
        print(f"Cache Size: {format_size(info['size_bytes'])}")
        print(f"Number of Entries: {info['num_entries']}")
        print(f"Cache File: {info['cache_file']}")
        print(f"Encrypted: {'Yes' if info['encrypted'] else 'No'}")
        print(f"Hit Rate: {info['hit_rate']:.2f}%")
        print(f"Cache Hits: {info['hits']}")
        print(f"Cache Misses: {info['misses']}")
        return
    
    # Initialize NOVA system
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                    NOVA ORCHESTRATION SYSTEM                     ║
║        [ NEURO-SYMBOLIC OPTIMIZED VERSATILE AGENT v2.0 ]        ║
╚══════════════════════════════════════════════════════════════════╝


▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
🔄 INITIALIZING NOVA CORE SYSTEMS...
📡 NEURAL INTERFACE: ONLINE
🧠 SYMBOLIC ENGINE: ACTIVE
🌐 LASER EMBEDDINGS: LOADED
🔧 TOOL INTERFACE: READY
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
""")
    
    nova = NovaCrew()
    try:
        nova.run(prompt=args.prompt, task_type=args.task)
    except KeyboardInterrupt:
        print("""
╔══════════════════════════════════════════════════════════════════╗
║             ⚠️ NOVA EXECUTION INTERRUPTED ⚠️                    ║
╚══════════════════════════════════════════════════════════════════╝

▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
        🔍 DIAGNOSTIC SCAN INITIATED
        💫 QUANTUM STATE PRESERVED
        🔄 READY FOR REACTIVATION
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
""")

if __name__ == '__main__':
    main()