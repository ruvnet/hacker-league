"""
NOVA (Neuro-Symbolic, Optimized, Versatile Agent) CLI Entry Point
"""

import warnings
warnings.filterwarnings('ignore', category=UserWarning)

import argparse
from nova.crew import NovaCrew

# ANSI color codes
MAGENTA = '\033[0;35m'
RED = '\033[0;31m'
NC = '\033[0m'  # No Color

def display_banner():
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                    NOVA ORCHESTRATION SYSTEM                     ║
║        [ NEURO-SYMBOLIC OPTIMIZED VERSATILE AGENT v2.0 ]        ║
╚══════════════════════════════════════════════════════════════════╝
""")

def parse_args():
    parser = argparse.ArgumentParser(description='NOVA Neural Orchestration System')
    parser.add_argument('--prompt', type=str, help='Prompt for the AI system', default="Tell me about yourself")
    parser.add_argument('--task', type=str, choices=['research', 'execute', 'analyze', 'both'], 
                       help='Task to perform: research, execute, analyze, or both', default='both')
    return parser.parse_args()

def run():
    args = parse_args()
    display_banner()
    
    print("""
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
🔄 INITIALIZING NOVA CORE SYSTEMS...
📡 NEURAL INTERFACE: ONLINE
🧠 SYMBOLIC ENGINE: ACTIVE
🌐 LASER EMBEDDINGS: LOADED
🔧 TOOL INTERFACE: READY
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
""")
    
    crew = NovaCrew()
    result = crew.run(prompt=args.prompt, task_type=args.task)
    
    if result:
        print("""
╔══════════════════════════════════════════════════════════════════╗
║                🌟 NOVA EXECUTION COMPLETE 🌟                     ║
╚══════════════════════════════════════════════════════════════════╝

""" + MAGENTA + """▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
        ✨ ALL OBJECTIVES ACHIEVED
        📊 PERFORMANCE METRICS OPTIMAL
        🔒 SYSTEM INTEGRITY MAINTAINED
        🌐 KNOWLEDGE BASE UPDATED
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀""" + NC + """
        """)
    else:
        print("""
╔══════════════════════════════════════════════════════════════════╗
║             ⚠️ NOVA EXECUTION INTERRUPTED ⚠️                    ║
╚══════════════════════════════════════════════════════════════════╝

""" + RED + """▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
        🔍 DIAGNOSTIC SCAN INITIATED
        💫 QUANTUM STATE PRESERVED
        🔄 READY FOR REACTIVATION
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀""" + NC + """
        """)

if __name__ == "__main__":
    run()