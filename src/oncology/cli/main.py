"""
Main CLI module for the Oncology System.
Provides entry points for both interactive and command-line usage.
"""

import sys
from pathlib import Path
from typing import Optional, List

from .utils.formatting import Colors, Emojis, print_header, print_menu_option
from .utils.parser import parse_args
from .commands.kb import KBCommands
from .commands.genomic import GenomicCommands
from .commands.bio import BioCommands
from .commands.doc import DocCommands

class OncologyCLI:
    """Main CLI class that coordinates all commands"""
    
    def __init__(self):
        # Base paths
        self.scripts_dir = Path("scripts")
        self.data_dir = Path("data")
        
        # Initialize command handlers
        self.kb = KBCommands(self.scripts_dir, self.data_dir)
        self.genomic = GenomicCommands(self.scripts_dir, self.data_dir)
        self.bio = BioCommands(self.scripts_dir, self.data_dir)
        self.doc = DocCommands(self.scripts_dir, self.data_dir)
    
    def run(self, args: Optional[List[str]] = None) -> None:
        """Run the CLI with given args"""
        if args is None:
            args = sys.argv[1:]
        
        # If no arguments, show interactive menu
        if not args:
            self.show_menu()
            return
        
        # Parse and handle command-line arguments
        parsed_args = parse_args(args)
        
        # Process command
        if parsed_args.command == 'kb':
            self.kb.handle_command(parsed_args)
        elif parsed_args.command == 'genomic':
            self.genomic.handle_command(parsed_args)
        elif parsed_args.command == 'bio':
            self.bio.handle_command(parsed_args)
        elif parsed_args.command == 'doc':
            self.doc.handle_command(parsed_args)
        else:
            self.show_menu()
    
    def show_menu(self) -> None:
        """Show interactive menu"""
        while True:
            print_header("Oncology System")
            
            print("\nAvailable Commands:")
            print_menu_option("1", Emojis.DRUG, "Knowledge Base Management")
            print_menu_option("2", Emojis.DNA, "Genomic Data Processing")
            print_menu_option("3", Emojis.MICROSCOPE, "Bioinformatics Analysis")
            print_menu_option("4", Emojis.REPORT, "Medical Document Processing")
            print_menu_option("0", "🚪", "Exit")
            
            choice = input(f"\n{Colors.INFO}Enter your choice (0-4): {Colors.ENDC}")
            
            if choice == '0':
                print(f"\n{Colors.SUCCESS}Goodbye!{Colors.ENDC}")
                break
            elif choice == '1':
                self.kb.show_menu()
            elif choice == '2':
                self.genomic.show_menu()
            elif choice == '3':
                self.bio.show_menu()
            elif choice == '4':
                self.doc.show_menu()

def main():
    """Main entry point with graceful exit handling"""
    cli = OncologyCLI()
    try:
        cli.run()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.INFO}Exiting gracefully...{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.ALERT}{Emojis.ERROR} Error: {str(e)}{Colors.ENDC}")
        sys.exit(1)

if __name__ == '__main__':
    main()