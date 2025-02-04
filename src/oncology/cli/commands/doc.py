"""
Medical Document Processing commands.
Handles both CLI and interactive modes for document operations.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional

from ..utils.formatting import (
    Colors, Emojis, print_header, print_section,
    print_menu_option, print_result, format_success, format_error
)

def load_script(script_path: str) -> Optional[object]:
    """Dynamically load a Python script"""
    import importlib.util
    try:
        spec = importlib.util.spec_from_file_location("module", script_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        return None
    except Exception as e:
        print(format_error(f"Error loading script: {e}"))
        return None

class DocCommands:
    """Medical Document Processing commands"""
    
    def __init__(self, scripts_dir: Path, data_dir: Path):
        self.scripts_dir = scripts_dir
        self.data_dir = data_dir
        self.kb_dir = data_dir / 'knowledge_base'
        self.reports_dir = data_dir / 'reports'
    
    def show_menu(self) -> None:
        """Show Medical Document Processing menu"""
        while True:
            print_header("Medical Document Processing")
            
            print_section("Available Actions")
            print_menu_option("1", Emojis.REPORT, "Extract Information")
            print_menu_option("2", Emojis.LINK, "Process References")
            print_menu_option("3", Emojis.CHART, "Generate Report")
            print_menu_option("0", "⬅️", "Return to Main Menu")
            
            choice = input(f"\n{Colors.INFO}Enter your choice (0-3): {Colors.ENDC}")
            
            if choice == '0':
                break
            elif choice == '1':
                self.extract_info_interactive()
            elif choice == '2':
                self.process_refs_interactive()
            elif choice == '3':
                self.generate_report_interactive()
    
    def extract_info_interactive(self) -> None:
        """Handle interactive document information extraction"""
        print_header("Extract Document Information")
        
        input_path = input(f"{Colors.INFO}Enter document path: {Colors.ENDC}")
        print("\nDocument types:")
        print("1. Clinical Report")
        print("2. Drug Label")
        print("3. Publication")
        doc_type = input(f"{Colors.INFO}Enter document type (1-3): {Colors.ENDC}")
        
        type_map = {
            "1": "report",
            "2": "label",
            "3": "publication"
        }
        
        if doc_type in type_map:
            self.extract_info(input_path, type_map[doc_type])
        else:
            print(format_error("Invalid document type selected"))
        
        input(f"\n{Colors.INFO}Press Enter to continue...{Colors.ENDC}")
    
    def process_refs_interactive(self) -> None:
        """Handle interactive reference processing"""
        print_header("Process Document References")
        
        input_path = input(f"{Colors.INFO}Enter document path: {Colors.ENDC}")
        
        self.process_refs(input_path)
        
        input(f"\n{Colors.INFO}Press Enter to continue...{Colors.ENDC}")
    
    def generate_report_interactive(self) -> None:
        """Handle interactive report generation"""
        print_header("Generate Document Report")
        
        input_path = input(f"{Colors.INFO}Enter document path: {Colors.ENDC}")
        output_path = input(f"{Colors.INFO}Enter output path (or press Enter for default): {Colors.ENDC}")
        
        self.generate_report(input_path, output_path)
        
        input(f"\n{Colors.INFO}Press Enter to continue...{Colors.ENDC}")
    
    def extract_info(self, input_path: str, doc_type: str) -> None:
        """Extract information from a document"""
        try:
            module = load_script(str(self.scripts_dir / 'medical_knowledge_agent.py'))
            if module:
                agent = module.MedicalKnowledgeAgent(self.kb_dir)
                result = agent.extract_information(input_path, doc_type)
                print(format_success("Extraction complete:"))
                print(json.dumps(result, indent=2))
        except Exception as e:
            print(format_error(str(e)))
    
    def process_refs(self, input_path: str) -> None:
        """Process document references"""
        try:
            module = load_script(str(self.scripts_dir / 'medical_knowledge_agent.py'))
            if module:
                agent = module.MedicalKnowledgeAgent(self.kb_dir)
                result = agent.process_references(input_path)
                print(format_success("Reference processing complete:"))
                print(json.dumps(result, indent=2))
        except Exception as e:
            print(format_error(str(e)))
    
    def generate_report(self, input_path: str, output_path: Optional[str] = None) -> None:
        """Generate a document report"""
        try:
            module = load_script(str(self.scripts_dir / 'medical_knowledge_agent.py'))
            if module:
                agent = module.MedicalKnowledgeAgent(self.kb_dir)
                result = agent.generate_report(
                    input_path,
                    Path(output_path) if output_path else self.reports_dir
                )
                print(format_success("Report generation complete:"))
                print(json.dumps(result, indent=2))
        except Exception as e:
            print(format_error(str(e)))
    
    def handle_command(self, args: Any) -> None:
        """Handle document commands from CLI arguments"""
        if args.doc_command == 'extract':
            self.extract_info(args.input, args.type)
        elif args.doc_command == 'refs':
            self.process_refs(args.input)
        elif args.doc_command == 'report':
            self.generate_report(args.input, args.output)