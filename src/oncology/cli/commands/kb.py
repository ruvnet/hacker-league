"""
Knowledge Base Management commands.
Handles both CLI and interactive modes for KB operations.
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

class KBCommands:
    """Knowledge Base Management commands"""
    
    def __init__(self, scripts_dir: Path, data_dir: Path):
        self.scripts_dir = scripts_dir
        self.data_dir = data_dir
        self.kb_dir = data_dir / 'knowledge_base'
    
    def show_menu(self) -> None:
        """Show Knowledge Base Management menu"""
        while True:
            print_header("Knowledge Base Management")
            
            print_section("Available Actions")
            print_menu_option("1", Emojis.REPORT, "Process Medical Documents")
            print_menu_option("2", Emojis.GENE, "Query Knowledge Base")
            print_menu_option("3", Emojis.CHART, "View Statistics")
            print_menu_option("0", "⬅️", "Return to Main Menu")
            
            choice = input(f"\n{Colors.INFO}Enter your choice (0-3): {Colors.ENDC}")
            
            if choice == '0':
                break
            elif choice == '1':
                self.process_document_interactive()
            elif choice == '2':
                self.query_kb_interactive()
            elif choice == '3':
                self.show_stats()
    
    def process_document_interactive(self) -> None:
        """Handle interactive KB document processing"""
        print_header("Process Medical Documents")
        
        input_path = input(f"{Colors.INFO}Enter document path: {Colors.ENDC}")
        print("\nDocument types:")
        print("1. Drug Label")
        print("2. Clinical Guideline")
        print("3. Clinical Trial")
        doc_type = input(f"{Colors.INFO}Enter document type (1-3): {Colors.ENDC}")
        
        type_map = {
            "1": "drug_label",
            "2": "guideline",
            "3": "trial"
        }
        
        if doc_type in type_map:
            self.process_document(input_path, type_map[doc_type])
        else:
            print(format_error("Invalid document type selected"))
        
        input(f"\n{Colors.INFO}Press Enter to continue...{Colors.ENDC}")
    
    def query_kb_interactive(self) -> None:
        """Handle interactive KB querying"""
        print_header("Query Knowledge Base")
        
        entity = input(f"{Colors.INFO}Enter entity to query (e.g., drug name): {Colors.ENDC}")
        relation = input(f"{Colors.INFO}Enter relation type (e.g., treats): {Colors.ENDC}")
        
        self.query_kb(entity, relation)
        
        input(f"\n{Colors.INFO}Press Enter to continue...{Colors.ENDC}")
    
    def show_stats(self) -> None:
        """Show Knowledge Base statistics"""
        print_header("Knowledge Base Statistics")
        
        print_section("Document Statistics")
        print(f"{Colors.EMPHASIS}Total Documents: {Emojis.REPORT} 0")
        print(f"Processed Documents: {Emojis.SUCCESS} 0")
        print(f"Failed Documents: {Emojis.ERROR} 0{Colors.ENDC}")
        
        print_section("Entity Statistics")
        print(f"{Colors.EMPHASIS}Drugs: {Emojis.DRUG} 0")
        print(f"Diseases: {Emojis.WARNING} 0")
        print(f"Genes: {Emojis.DNA} 0{Colors.ENDC}")
        
        print_section("Processing Time")
        print(f"{Colors.EMPHASIS}Average Processing Time: {Emojis.CLOCK} 0s{Colors.ENDC}")
        
        input(f"\n{Colors.INFO}Press Enter to continue...{Colors.ENDC}")
    
    def process_document(self, input_path: str, doc_type: str) -> None:
        """Process a medical document"""
        try:
            module = load_script(str(self.scripts_dir / 'medical_knowledge_agent.py'))
            if module:
                agent = module.MedicalKnowledgeAgent(self.kb_dir)
                result = agent.process_document(input_path, doc_type)
                print(format_success("Processing complete:"))
                print(json.dumps(result, indent=2))
        except Exception as e:
            print(format_error(str(e)))
    
    def query_kb(self, entity: str, relation: str) -> None:
        """Query the knowledge base"""
        try:
            module = load_script(str(self.scripts_dir / 'medical_knowledge_agent.py'))
            if module:
                agent = module.MedicalKnowledgeAgent(self.kb_dir)
                result = agent.query_knowledge_base(entity, relation)
                print(format_success("Query results:"))
                print(json.dumps(result, indent=2))
        except Exception as e:
            print(format_error(str(e)))
    
    def handle_command(self, args: Any) -> None:
        """Handle KB commands from CLI arguments"""
        if args.kb_command == 'process':
            self.process_document(args.input, args.type)
        elif args.kb_command == 'query':
            self.query_kb(args.entity, args.relation)
        elif args.kb_command == 'stats':
            self.show_stats()