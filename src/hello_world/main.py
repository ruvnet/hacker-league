import warnings
warnings.filterwarnings('ignore', category=UserWarning)

from hello_world.crew import HelloWorldCrew

# ANSI color codes
MAGENTA = '\033[0;35m'
RED = '\033[0;31m'
NC = '\033[0m'  # No Color

def display_banner():
    print("""
╔══════════════════════════════════════════════════════════════════╗
║              NEURAL NETWORK ORCHESTRATION SYSTEM                 ║
║                     [ CODENAME: CREWAI ]                        ║
╚══════════════════════════════════════════════════════════════════╝
    """)

def run():
    display_banner()
    crew = HelloWorldCrew()
    result = crew.run()
    if result:
        print("""
╔══════════════════════════════════════════════════════════════════╗
║             🌟 NEURAL PROCESSING COMPLETE 🌟                     ║
╚══════════════════════════════════════════════════════════════════╝

""" + MAGENTA + """▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
        ✨ ALL OBJECTIVES ACHIEVED
        📊 PERFORMANCE METRICS OPTIMAL
        🔒 SYSTEM INTEGRITY MAINTAINED
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀""" + NC + """
        """)
    else:
        print("""
╔══════════════════════════════════════════════════════════════════╗
║             ⚠️ NEURAL PROCESSING INTERRUPTED ⚠️                 ║
╚══════════════════════════════════════════════════════════════════╝

""" + RED + """▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
        🔍 DIAGNOSTIC SCAN INITIATED
        💫 QUANTUM STATE PRESERVED
        🔄 READY FOR REACTIVATION
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀""" + NC + """
        """)

if __name__ == "__main__":
    run()
