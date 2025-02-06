import warnings
warnings.filterwarnings('ignore', category=UserWarning)

import argparse
from beverages.crew import BeverageCrew

# ANSI color codes
MAGENTA = '\033[0;35m'
RED = '\033[0;31m'
NC = '\033[0m'  # No Color

def display_banner():
    print("""
╔══════════════════════════════════════════════════════════════════╗
║            BEVERAGE PRODUCT DEVELOPMENT SYSTEM v2.0              ║
║           Market Research & Innovation Analysis Core             ║
╚══════════════════════════════════════════════════════════════════╝
    """)

def parse_args():
    parser = argparse.ArgumentParser(description='Beverage Product Development System')
    parser.add_argument('--prompt', type=str, help='Prompt for the AI system', default="Tell me about yourself")
    parser.add_argument('--task', type=str, choices=['research', 'execute', 'analyze', 'both'], 
                       help='Task to perform: research, execute, analyze, or both', default='both')
    return parser.parse_args()

def run():
    args = parse_args()
    display_banner()
    crew = BeverageCrew()
    result = crew.run(prompt=args.prompt, task_type=args.task)
    if result:
        print("""
╔══════════════════════════════════════════════════════════════════╗
║             🌟 PRODUCT ANALYSIS COMPLETE 🌟                      ║
╚══════════════════════════════════════════════════════════════════╝

""" + MAGENTA + """▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
        ✨ MARKET INSIGHTS GATHERED
        📊 PRODUCT STRATEGY DEFINED
        🔒 INNOVATION POTENTIAL VALIDATED
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀""" + NC + """
        """)
    else:
        print("""
╔══════════════════════════════════════════════════════════════════╗
║             ⚠️ ANALYSIS PROCESS INTERRUPTED ⚠️                  ║
╚══════════════════════════════════════════════════════════════════╝

""" + RED + """▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
        🔍 SAVING PARTIAL INSIGHTS
        💫 PRESERVING MARKET DATA
        🔄 READY FOR REACTIVATION
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀""" + NC + """
        """)

if __name__ == "__main__":
    run()
