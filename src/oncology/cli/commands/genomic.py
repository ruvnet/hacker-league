"""
Genomic Data Processing commands.
Handles both CLI and interactive modes for genomic data operations.
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

class GenomicCommands:
    """Genomic Data Processing commands"""
    
    def __init__(self, scripts_dir: Path, data_dir: Path):
        self.scripts_dir = scripts_dir
        self.data_dir = data_dir
        self.harmonized_dir = data_dir / 'harmonized'
        
        # Example annotation database - in production this would be loaded from a file
        self.annotation_db = {
            "chr17:41244435:G>A": {
                "gene": "BRCA1",
                "effect": "missense",
                "impact": "moderate"
            }
        }
    
    def show_menu(self) -> None:
        """Show Genomic Data Processing menu"""
        while True:
            print_header("Genomic Data Processing")
            
            print_section("Available Actions")
            print_menu_option("1", Emojis.DNA, "Process VCF Files")
            print_menu_option("2", Emojis.CHART, "Process Expression Data")
            print_menu_option("3", Emojis.LINK, "Harmonize Data")
            print_menu_option("0", "⬅️", "Return to Main Menu")
            
            choice = input(f"\n{Colors.INFO}Enter your choice (0-3): {Colors.ENDC}")
            
            if choice == '0':
                break
            elif choice == '1':
                self.process_vcf_interactive()
            elif choice == '2':
                self.process_expression_interactive()
            elif choice == '3':
                self.harmonize_data_interactive()
    
    def process_vcf_interactive(self) -> None:
        """Handle interactive VCF file processing"""
        print_header("Process VCF Files")
        
        vcf_path = input(f"{Colors.INFO}Enter VCF file path: {Colors.ENDC}")
        expression_path = input(f"{Colors.INFO}Enter expression data file path: {Colors.ENDC}")
        output_dir = input(f"{Colors.INFO}Enter output directory (or press Enter for default): {Colors.ENDC}")
        
        self.process_data(vcf_path, expression_path, output_dir)
        
        input(f"\n{Colors.INFO}Press Enter to continue...{Colors.ENDC}")
    
    def process_expression_interactive(self) -> None:
        """Handle interactive expression data processing"""
        print_header("Process Expression Data")
        
        expression_path = input(f"{Colors.INFO}Enter expression data file path: {Colors.ENDC}")
        vcf_path = input(f"{Colors.INFO}Enter VCF file path: {Colors.ENDC}")
        output_dir = input(f"{Colors.INFO}Enter output directory (or press Enter for default): {Colors.ENDC}")
        
        self.process_data(vcf_path, expression_path, output_dir)
        
        input(f"\n{Colors.INFO}Press Enter to continue...{Colors.ENDC}")
    
    def harmonize_data_interactive(self) -> None:
        """Handle interactive data harmonization"""
        print_header("Harmonize Genomic Data")
        
        input_dir = input(f"{Colors.INFO}Enter input directory: {Colors.ENDC}")
        output_dir = input(f"{Colors.INFO}Enter output directory (or press Enter for default): {Colors.ENDC}")
        
        self.harmonize_data(input_dir, output_dir)
        
        input(f"\n{Colors.INFO}Press Enter to continue...{Colors.ENDC}")
    
    def process_data(self, vcf_path: str, expression_path: str, output_dir: Optional[str] = None) -> None:
        """Process genomic data"""
        try:
            module = load_script(str(self.scripts_dir / 'genomic_harmonizer.py'))
            if module:
                harmonizer = module.GenomicHarmonizer(
                    Path(output_dir) if output_dir else self.harmonized_dir
                )
                # Load and process data
                harmonizer.load_vcf(Path(vcf_path))
                harmonizer.load_expression_data(Path(expression_path))
                harmonizer.export_harmonized_data()
                
                # Get stats for output
                stats = {
                    'total_variants': len(harmonizer.variants),
                    'total_genes': len(harmonizer.expression_data),
                    'linked_variants': len(harmonizer.create_variant_gene_links())
                }
                
                print(format_success("Processing complete:"))
                print(json.dumps(stats, indent=2))
        except Exception as e:
            print(format_error(str(e)))
    
    def harmonize_data(self, input_dir: str, output_dir: Optional[str] = None) -> None:
        """Harmonize genomic data"""
        try:
            module = load_script(str(self.scripts_dir / 'genomic_harmonizer.py'))
            if module:
                harmonizer = module.GenomicHarmonizer(
                    Path(output_dir) if output_dir else self.harmonized_dir
                )
                result = harmonizer.harmonize_directory(input_dir)
                print(format_success("Harmonization complete:"))
                print(json.dumps(result, indent=2))
        except Exception as e:
            print(format_error(str(e)))
    
    def analyze_data(self, input_dir: str, analysis_type: str) -> None:
        """Analyze genomic data"""
        try:
            module = load_script(str(self.scripts_dir / 'bioinformatics_agent.py'))
            if module:
                agent = module.BioinformaticsAgent(Path(input_dir))
                # Call appropriate analysis method based on analysis_type
                if analysis_type == 'enrichment':
                    result = agent.analyze_enrichment()
                elif analysis_type == 'correlation':
                    result = agent.analyze_correlation()
                elif analysis_type == 'de':
                    result = agent.analyze_differential_expression()
                else:
                    raise ValueError(f"Unknown analysis type: {analysis_type}")
                
                print(format_success("Analysis complete:"))
                print(json.dumps(result, indent=2))
        except Exception as e:
            print(format_error(str(e)))
    
    def handle_command(self, args: Any) -> None:
        """Handle genomic commands from CLI arguments"""
        if args.genomic_command == 'process':
            self.process_data(args.vcf, args.expression, args.output)
        elif args.genomic_command == 'analyze':
            self.analyze_data(args.input, args.analysis)
        elif args.genomic_command == 'harmonize':
            self.harmonize_data(args.input, args.output)