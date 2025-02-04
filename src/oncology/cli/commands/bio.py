"""
Bioinformatics Analysis commands.
Handles both CLI and interactive modes for bioinformatics operations.
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

class BioCommands:
    """Bioinformatics Analysis commands"""
    
    def __init__(self, scripts_dir: Path, data_dir: Path):
        self.scripts_dir = scripts_dir
        self.data_dir = data_dir
        self.bio_dir = data_dir / 'bio_analysis'
    
    def show_menu(self) -> None:
        """Show Bioinformatics Analysis menu"""
        while True:
            print_header("Bioinformatics Analysis")
            
            print_section("Available Analyses")
            print_menu_option("1", Emojis.PATHWAY, "Pathway Enrichment")
            print_menu_option("2", Emojis.GENE, "Differential Expression")
            print_menu_option("3", Emojis.LINK, "Gene Correlation")
            print_menu_option("0", "⬅️", "Return to Main Menu")
            
            choice = input(f"\n{Colors.INFO}Enter your choice (0-3): {Colors.ENDC}")
            
            if choice == '0':
                break
            elif choice == '1':
                self.pathway_analysis_interactive()
            elif choice == '2':
                self.expression_analysis_interactive()
            elif choice == '3':
                self.correlation_analysis_interactive()
    
    def pathway_analysis_interactive(self) -> None:
        """Handle interactive pathway analysis"""
        print_header("Pathway Enrichment Analysis")
        
        genes_file = input(f"{Colors.INFO}Enter gene list file path: {Colors.ENDC}")
        pathways_file = input(f"{Colors.INFO}Enter pathway database file path: {Colors.ENDC}")
        
        self.analyze_pathways(genes_file, pathways_file)
        
        input(f"\n{Colors.INFO}Press Enter to continue...{Colors.ENDC}")
    
    def expression_analysis_interactive(self) -> None:
        """Handle interactive expression analysis"""
        print_header("Expression Analysis")
        
        data_file = input(f"{Colors.INFO}Enter expression data file path: {Colors.ENDC}")
        groups_file = input(f"{Colors.INFO}Enter sample groups file path: {Colors.ENDC}")
        
        self.analyze_expression(data_file, groups_file)
        
        input(f"\n{Colors.INFO}Press Enter to continue...{Colors.ENDC}")
    
    def correlation_analysis_interactive(self) -> None:
        """Handle interactive correlation analysis"""
        print_header("Gene Correlation Analysis")
        
        data_file = input(f"{Colors.INFO}Enter expression data file path: {Colors.ENDC}")
        gene_pairs = input(f"{Colors.INFO}Enter gene pairs file path: {Colors.ENDC}")
        
        self.analyze_correlation(data_file, gene_pairs)
        
        input(f"\n{Colors.INFO}Press Enter to continue...{Colors.ENDC}")
    
    def analyze_pathways(self, genes_file: str, pathways_file: str) -> None:
        """Perform pathway enrichment analysis"""
        try:
            module = load_script(str(self.scripts_dir / 'bioinformatics_agent.py'))
            if module:
                agent = module.BioinformaticsAgent(self.bio_dir)
                with open(genes_file) as f:
                    genes = f.read().strip().split('\n')
                with open(pathways_file) as f:
                    pathways = json.load(f)
                result = agent.analyze_pathways(genes, pathways)
                print(format_success("Analysis complete:"))
                print(json.dumps(result, indent=2))
        except Exception as e:
            print(format_error(str(e)))
    
    def analyze_expression(self, data_file: str, groups_file: str) -> None:
        """Perform differential expression analysis"""
        try:
            module = load_script(str(self.scripts_dir / 'bio_analyzer.py'))
            if module:
                analyzer = module.BioAnalyzer(self.bio_dir)
                result = analyzer.analyze_expression(data_file, groups_file)
                print(format_success("Analysis complete:"))
                print(json.dumps(result, indent=2))
        except Exception as e:
            print(format_error(str(e)))
    
    def analyze_correlation(self, data_file: str, gene_pairs: str) -> None:
        """Perform gene correlation analysis"""
        try:
            module = load_script(str(self.scripts_dir / 'bio_analyzer.py'))
            if module:
                analyzer = module.BioAnalyzer(self.bio_dir)
                result = analyzer.analyze_correlations(data_file, gene_pairs)
                print(format_success("Analysis complete:"))
                print(json.dumps(result, indent=2))
        except Exception as e:
            print(format_error(str(e)))
    
    def handle_command(self, args: Any) -> None:
        """Handle bioinformatics commands from CLI arguments"""
        if args.bio_command == 'pathway':
            self.analyze_pathways(args.genes, args.pathways)
        elif args.bio_command == 'expression':
            self.analyze_expression(args.data, args.groups)
        elif args.bio_command == 'correlation':
            self.analyze_correlation(args.data, args.genes)