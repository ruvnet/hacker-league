#!/usr/bin/env python3
"""
Genomic Data Processing Agent using ReAct Architecture

This agent processes genomic data and harmonizes across sources:
1. Observation: Load and validate genomic data
2. Thought: Analyze data quality and compatibility
3. Action: Transform and harmonize data formats
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# ANSI color codes for clinical formatting
class Colors:
    HEADER = '\033[95m'      # Purple for headers
    ALERT = '\033[91m'       # Red for alerts/warnings
    SUCCESS = '\033[92m'     # Green for success
    INFO = '\033[94m'        # Blue for info
    EMPHASIS = '\033[93m'    # Yellow for emphasis
    ENDC = '\033[0m'         # End color
    BOLD = '\033[1m'         # Bold text
    UNDERLINE = '\033[4m'    # Underlined text

# Clinical emojis
class Emojis:
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

@dataclass
class GenomicVariant:
    """Standardized representation of a genomic variant"""
    chrom: str
    pos: int
    ref: str
    alt: str
    qual: float
    filter_status: str
    info: Dict[str, Any]
    annotations: Dict[str, Any]

class Tool:
    """Base class for genomic data tools"""
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    def __call__(self, *args, **kwargs) -> Dict[str, Any]:
        raise NotImplementedError

class VCFTool(Tool):
    """Process VCF files with variant data"""
    def __init__(self):
        super().__init__(
            name="vcf_processor",
            description="Load and validate VCF files"
        )
    
    def __call__(self, vcf_path: str) -> Dict[str, Any]:
        try:
            variants = []
            with open(vcf_path) as f:
                for line in f:
                    if line.startswith('#'):
                        continue
                    # Parse VCF fields
                    fields = line.strip().split('\t')
                    if len(fields) < 8:
                        continue
                    
                    # Extract basic fields
                    variant = GenomicVariant(
                        chrom=fields[0],
                        pos=int(fields[1]),
                        ref=fields[3],
                        alt=fields[4],
                        qual=float(fields[5]) if fields[5] != '.' else None,
                        filter_status=fields[6],
                        info=self._parse_info(fields[7]),
                        annotations={}
                    )
                    variants.append(variant)
            
            return {
                'success': True,
                'data': {
                    'variants': variants,
                    'count': len(variants)
                },
                'error': None
            }
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'error': str(e)
            }
    
    def _parse_info(self, info_str: str) -> Dict[str, Any]:
        """Parse VCF INFO field"""
        info = {}
        for item in info_str.split(';'):
            if '=' in item:
                key, value = item.split('=', 1)
                info[key] = value
            else:
                info[item] = True
        return info

class ExpressionTool(Tool):
    """Process gene expression data"""
    def __init__(self):
        super().__init__(
            name="expression_processor",
            description="Load and normalize expression data"
        )
    
    def __call__(self, expr_path: str) -> Dict[str, Any]:
        try:
            # Read expression matrix
            expr_df = pd.read_csv(expr_path)
            expr_df.set_index('gene_id', inplace=True)
            
            # Basic QC
            missing = expr_df.isnull().sum().sum()
            zero_genes = (expr_df == 0).all(axis=1).sum()
            
            # Log2 transform if needed
            if expr_df.select_dtypes(include=[np.number]).min().min() >= 0:
                expr_df = np.log2(expr_df.astype(float) + 1)
            
            # Basic normalization
            expr_df = (expr_df - expr_df.mean()) / expr_df.std()
            
            return {
                'success': True,
                'data': {
                    'expression': expr_df,
                    'qc': {
                        'missing_values': missing,
                        'zero_genes': zero_genes,
                        'samples': expr_df.shape[1],
                        'genes': expr_df.shape[0]
                    }
                },
                'error': None
            }
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'error': str(e)
            }

class AnnotationTool(Tool):
    """Add annotations to genomic data"""
    def __init__(self):
        super().__init__(
            name="annotator",
            description="Annotate variants with functional information"
        )
    
    def __call__(self, 
                 variants: List[GenomicVariant],
                 annotation_db: Dict[str, Any]) -> Dict[str, Any]:
        try:
            annotated = []
            for variant in variants:
                # Create variant key
                key = f"{variant.chrom}:{variant.pos}:{variant.ref}>{variant.alt}"
                
                # Get annotations
                annotations = annotation_db.get(key, {})
                
                # Add annotations to variant
                variant.annotations.update(annotations)
                annotated.append(variant)
            
            return {
                'success': True,
                'data': {
                    'variants': annotated,
                    'annotated_count': len(annotated)
                },
                'error': None
            }
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'error': str(e)
            }

class HarmonizationTool(Tool):
    """Harmonize data across different sources"""
    def __init__(self):
        super().__init__(
            name="harmonizer",
            description="Standardize data formats and merge sources"
        )
    
    def __call__(self, 
                 variants: List[GenomicVariant],
                 expression_data: pd.DataFrame) -> Dict[str, Any]:
        try:
            # Create standardized variant DataFrame
            var_records = []
            for var in variants:
                record = {
                    'chrom': var.chrom,
                    'pos': var.pos,
                    'ref': var.ref,
                    'alt': var.alt,
                    'qual': var.qual,
                    'filter': var.filter_status
                }
                # Add INFO fields
                record.update(var.info)
                # Add annotations
                record.update(var.annotations)
                var_records.append(record)
            
            var_df = pd.DataFrame(var_records)
            
            # Attempt to link variants to expression
            # For example, find genes affected by variants
            affected_genes = set()
            for var in variants:
                if 'gene' in var.annotations:
                    gene = var.annotations['gene']
                    if gene in expression_data.index:
                        affected_genes.add(gene)
            
            return {
                'success': True,
                'data': {
                    'harmonized_variants': var_df,
                    'expression_data': expression_data,
                    'affected_genes': list(affected_genes),
                    'integration_stats': {
                        'total_variants': len(variants),
                        'total_genes': len(expression_data),
                        'linked_genes': len(affected_genes)
                    }
                },
                'error': None
            }
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'error': str(e)
            }

@dataclass
class AgentState:
    """State of the genomic data agent"""
    vcf_processed: bool = False
    expression_processed: bool = False
    annotations_added: bool = False
    data_harmonized: bool = False
    current_variants: Optional[List[GenomicVariant]] = None
    current_expression: Optional[pd.DataFrame] = None
    error_log: List[str] = None

class GenomicDataAgent:
    """ReAct-style agent for genomic data processing"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize tools
        self.tools = {
            'vcf': VCFTool(),
            'expression': ExpressionTool(),
            'annotator': AnnotationTool(),
            'harmonizer': HarmonizationTool()
        }
        
        # Initialize state
        self.state = AgentState(error_log=[])
    
    def process_data(self, 
                    vcf_path: str,
                    expression_path: str,
                    annotation_db: Dict[str, Any]) -> str:
        """Process and harmonize genomic data"""
        
        # Step 1: Process VCF
        print(f"\n{Colors.INFO}{Emojis.DNA} Processing VCF file...{Colors.ENDC}")
        vcf_result = self.tools['vcf'](vcf_path)
        if not vcf_result['success']:
            self.state.error_log.append(f"VCF error: {vcf_result['error']}")
            return self._format_error_report()
        
        self.state.vcf_processed = True
        self.state.current_variants = vcf_result['data']['variants']
        print(f"{Colors.SUCCESS}Found {len(self.state.current_variants)} variants{Colors.ENDC}")
        
        # Step 2: Process Expression Data
        print(f"\n{Colors.INFO}{Emojis.MICROSCOPE} Processing expression data...{Colors.ENDC}")
        expr_result = self.tools['expression'](expression_path)
        if not expr_result['success']:
            self.state.error_log.append(f"Expression error: {expr_result['error']}")
            return self._format_error_report()
        
        self.state.expression_processed = True
        self.state.current_expression = expr_result['data']['expression']
        print(f"{Colors.SUCCESS}Expression data processed successfully{Colors.ENDC}")
        print(f"{Colors.INFO}QC stats: {expr_result['data']['qc']}{Colors.ENDC}")
        
        # Step 3: Add Annotations
        print(f"\n{Colors.INFO}{Emojis.LINK} Adding annotations...{Colors.ENDC}")
        annot_result = self.tools['annotator'](
            self.state.current_variants,
            annotation_db
        )
        if not annot_result['success']:
            self.state.error_log.append(f"Annotation error: {annot_result['error']}")
            return self._format_error_report()
        
        self.state.annotations_added = True
        self.state.current_variants = annot_result['data']['variants']
        print(f"{Colors.SUCCESS}Added annotations to {annot_result['data']['annotated_count']} variants{Colors.ENDC}")
        
        # Step 4: Harmonize Data
        print(f"\n{Colors.INFO}{Emojis.CHART} Harmonizing data...{Colors.ENDC}")
        harm_result = self.tools['harmonizer'](
            self.state.current_variants,
            self.state.current_expression
        )
        if not harm_result['success']:
            self.state.error_log.append(f"Harmonization error: {harm_result['error']}")
            return self._format_error_report()
        
        self.state.data_harmonized = True
        
        # Export harmonized data
        self._export_results(harm_result['data'])
        
        return self._format_success_report(harm_result['data'])
    
    def _export_results(self, harmonized_data: Dict[str, Any]) -> None:
        """Export harmonized data to files"""
        # Save variant data
        variants_file = self.output_dir / 'harmonized_variants.csv'
        harmonized_data['harmonized_variants'].to_csv(variants_file)
        
        # Save expression data
        expression_file = self.output_dir / 'harmonized_expression.csv'
        harmonized_data['expression_data'].to_csv(expression_file)
        
        # Save integration stats
        stats_file = self.output_dir / 'integration_stats.json'
        with stats_file.open('w') as f:
            json.dump(harmonized_data['integration_stats'], f, indent=2)
    
    def _format_success_report(self, data: Dict[str, Any]) -> str:
        """Format successful processing report with clinical styling"""
        header = f"""
{Colors.HEADER}{Colors.BOLD}╔══════════════════════════════════════════════════════════════════╗
║                    GENOMIC DATA INTEGRATION                       ║
╚══════════════════════════════════════════════════════════════════╝{Colors.ENDC}
"""
        sections = []

        # Processing Status
        sections.append(f"""
{Colors.INFO}{Colors.BOLD}PROCESSING STATUS:{Colors.ENDC}
{self._format_status_line('VCF Analysis', self.state.vcf_processed)}
{self._format_status_line('Expression Analysis', self.state.expression_processed)}
{self._format_status_line('Variant Annotation', self.state.annotations_added)}
{self._format_status_line('Data Harmonization', self.state.data_harmonized)}
""")

        # Integration Statistics
        stats = data['integration_stats']
        sections.append(f"""
{Colors.INFO}{Colors.BOLD}INTEGRATION METRICS:{Colors.ENDC}
{Emojis.DNA} Variants Processed: {Colors.EMPHASIS}{stats['total_variants']}{Colors.ENDC}
{Emojis.MICROSCOPE} Genes Analyzed: {Colors.EMPHASIS}{stats['total_genes']}{Colors.ENDC}
{Emojis.LINK} Variant-Gene Links: {Colors.EMPHASIS}{stats['linked_genes']}{Colors.ENDC}
""")

        # Output Files
        sections.append(f"""
{Colors.SUCCESS}{Colors.BOLD}OUTPUT FILES:{Colors.ENDC}
{Emojis.REPORT} Harmonized Variants: {self.output_dir / 'harmonized_variants.csv'}
{Emojis.CHART} Expression Matrix: {self.output_dir / 'harmonized_expression.csv'}
{Emojis.INFO} Integration Stats: {self.output_dir / 'integration_stats.json'}
""")

        footer = f"""
{Colors.HEADER}▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀{Colors.ENDC}
"""

        return header + "\n".join(sections) + footer
    
    def _format_error_report(self) -> str:
        """Format error report with clinical styling"""
        return f"""
{Colors.HEADER}{Colors.BOLD}╔══════════════════════════════════════════════════════════════════╗
║                    GENOMIC PROCESSING ERROR                      ║
╚══════════════════════════════════════════════════════════════════╝{Colors.ENDC}

{Colors.ALERT}{Emojis.WARNING} Processing Status:{Colors.ENDC}
{self._format_status_line('VCF Analysis', self.state.vcf_processed)}
{self._format_status_line('Expression Analysis', self.state.expression_processed)}
{self._format_status_line('Variant Annotation', self.state.annotations_added)}
{self._format_status_line('Data Harmonization', self.state.data_harmonized)}

{Colors.ALERT}{Colors.BOLD}ERROR LOG:{Colors.ENDC}
""" + "\n".join(f"{Colors.ALERT}{Emojis.ERROR} {err}{Colors.ENDC}" 
                for err in self.state.error_log) + f"""

{Colors.INFO}{Emojis.INFO} Please review errors and resubmit data for processing.{Colors.ENDC}

{Colors.HEADER}▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀{Colors.ENDC}
"""

    def _format_status_line(self, label: str, status: bool) -> str:
        """Format a status line with appropriate emoji and color"""
        emoji = Emojis.SUCCESS if status else Emojis.ERROR
        color = Colors.SUCCESS if status else Colors.ALERT
        return f"{color}{emoji} {label}: {'Completed' if status else 'Failed'}{Colors.ENDC}"

def main():
    # Initialize agent
    agent = GenomicDataAgent(Path('data/harmonized'))
    
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}")
    print(f"Genomic Data Processing System")
    print(f"{'='*70}{Colors.ENDC}")
    
    # Example annotation database
    annotation_db = {
        "chr17:41244435:G>A": {
            "gene": "BRCA1",
            "effect": "missense",
            "impact": "moderate"
        }
    }
    
    # Process example data
    result = agent.process_data(
        vcf_path='data/harmonized/variants/sample1.vcf',
        expression_path='data/bio_analysis/expression.csv',
        annotation_db=annotation_db
    )
    
    print(result)

if __name__ == '__main__':
    main()