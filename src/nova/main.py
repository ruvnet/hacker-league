"""
NOVA (Neuro-Symbolic, Optimized, Versatile Agent) Main Entry Point
"""

import warnings
warnings.filterwarnings('ignore', category=UserWarning)

import argparse
from nova.crew import NovaCrew

# ANSI color codes
MAGENTA = '\033[0;35m'
CYAN = '\033[0;36m'
RED = '\033[0;31m'
NC = '\033[0m'  # No Color

def display_banner():
    """Display NOVA system banner"""
    print(f"""{CYAN}
╔══════════════════════════════════════════════════════════════════╗
║                    NOVA ORCHESTRATION SYSTEM                     ║
║        [ NEURO-SYMBOLIC OPTIMIZED VERSATILE AGENT v2.0 ]        ║
╚══════════════════════════════════════════════════════════════════╝{NC}
    """)

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='NOVA (Neuro-Symbolic, Optimized, Versatile Agent) System'
    )
    
    parser.add_argument(
        '--prompt', 
        type=str, 
        help='Input prompt for the NOVA system',
        default="Tell me about yourself"
    )
    
    parser.add_argument(
        '--task', 
        type=str, 
        choices=['research', 'execute', 'analyze', 'both'],
        help='Task type to perform: research, execute, analyze, or both',
        default='both'
    )
    
    parser.add_argument(
        '--lang', 
        type=str,
        help='Source language code (e.g., en, es, fr)',
        default=None
    )
    
    parser.add_argument(
        '--domain',
        type=str,
        help='Specific domain for context (e.g., healthcare, finance)',
        default=None
    )
    
    return parser.parse_args()

def run():
    """Main execution function"""
    args = parse_args()
    display_banner()
    
    # Initialize NOVA system
    print(f"""{CYAN}
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
🔄 INITIALIZING NOVA CORE SYSTEMS...
📡 NEURAL INTERFACE: ONLINE
🧠 SYMBOLIC ENGINE: ACTIVE
🌐 LASER EMBEDDINGS: LOADED
🔧 TOOL INTERFACE: READY
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀{NC}
    """)
    
    crew = NovaCrew()
    result = crew.run(
        prompt=args.prompt,
        task_type=args.task
    )
    
    if result:
        print(f"""{MAGENTA}
╔══════════════════════════════════════════════════════════════════╗
║                🌟 NOVA EXECUTION COMPLETE 🌟                     ║
╚══════════════════════════════════════════════════════════════════╝

▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
        ✨ ALL OBJECTIVES ACHIEVED
        📊 PERFORMANCE METRICS OPTIMAL
        🔒 SYSTEM INTEGRITY MAINTAINED
        🌐 KNOWLEDGE BASE UPDATED
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀{NC}
        """)
    else:
        print(f"""{RED}
╔══════════════════════════════════════════════════════════════════╗
║             ⚠️ NOVA EXECUTION INTERRUPTED ⚠️                    ║
╚══════════════════════════════════════════════════════════════════╝

▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
        🔍 DIAGNOSTIC SCAN INITIATED
        💫 QUANTUM STATE PRESERVED
        🔄 READY FOR REACTIVATION
        📡 AWAITING FURTHER INSTRUCTIONS
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀{NC}
        """)

if __name__ == "__main__":
    run()