"""
Formatting utilities for the CLI interface.
Provides ANSI color codes and emojis for consistent styling.
"""

class Colors:
    """ANSI color codes for clinical formatting"""
    HEADER = '\033[95m'      # Purple for headers
    ALERT = '\033[91m'       # Red for alerts/warnings
    SUCCESS = '\033[92m'     # Green for success
    INFO = '\033[94m'        # Blue for info
    EMPHASIS = '\033[93m'    # Yellow for emphasis
    ENDC = '\033[0m'         # End color
    BOLD = '\033[1m'         # Bold text
    UNDERLINE = '\033[4m'    # Underlined text

class Emojis:
    """Clinical emojis for visual indicators"""
    DNA = "🧬"              # Genomic data
    WARNING = "⚠️"           # Warning/Alert
    SUCCESS = "✅"           # Success/Validated
    ERROR = "❌"             # Error/Failed
    INFO = "i️"             # Information
    MICROSCOPE = "🔬"       # Analysis
    CHART = "📊"            # Data/Statistics
    LINK = "🔗"             # Reference/Link
    CLOCK = "⏱️"            # Time/Duration
    REPORT = "📋"           # Report/Results
    PATHWAY = "🔄"          # Pathway/Process
    GENE = "🔍"             # Gene/Search
    DRUG = "💊"             # Medication
    LAB = "🧪"              # Laboratory
    BRAIN = "🧠"            # AI/Analysis

def print_header(title: str) -> None:
    """Print a formatted header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}")
    print(f"{title}")
    print(f"{'='*70}{Colors.ENDC}\n")

def print_section(title: str) -> None:
    """Print a section header"""
    print(f"\n{Colors.INFO}{Colors.BOLD}{title}:{Colors.ENDC}")

def format_success(message: str) -> str:
    """Format a success message"""
    return f"{Colors.SUCCESS}{Emojis.SUCCESS} {message}{Colors.ENDC}"

def format_error(message: str) -> str:
    """Format an error message"""
    return f"{Colors.ALERT}{Emojis.ERROR} {message}{Colors.ENDC}"

def format_info(message: str) -> str:
    """Format an info message"""
    return f"{Colors.INFO}{Emojis.INFO} {message}{Colors.ENDC}"

def format_warning(message: str) -> str:
    """Format a warning message"""
    return f"{Colors.EMPHASIS}{Emojis.WARNING} {message}{Colors.ENDC}"

def print_menu_option(number: str, emoji: str, text: str) -> None:
    """Print a menu option with consistent formatting"""
    print(f"{Colors.EMPHASIS}{number}. {emoji} {text}{Colors.ENDC}")

def print_result(success: bool, message: str, details: str = None) -> None:
    """Print an operation result with appropriate styling"""
    if success:
        print(format_success(message))
    else:
        print(format_error(message))
    if details:
        print(f"{Colors.INFO}{details}{Colors.ENDC}")