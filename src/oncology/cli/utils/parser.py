"""
Argument parser setup for the CLI interface.
Provides a consistent way to define and handle command-line arguments.
"""

import argparse
from pathlib import Path
from typing import Optional

def create_parser() -> argparse.ArgumentParser:
    """Create the main argument parser with all subcommands"""
    parser = argparse.ArgumentParser(
        description="Oncology System Command Line Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage="%(prog)s [-h] {kb,genomic,bio,doc} ...\n\n"
              "Oncology System CLI - Process and analyze medical data"
    )
    
    subparsers = parser.add_subparsers(
        dest='command',
        title='available commands',
        metavar='{kb,genomic,bio,doc}'
    )
    
    # Add subcommand parsers
    _add_kb_parser(subparsers)
    _add_genomic_parser(subparsers)
    _add_bio_parser(subparsers)
    _add_doc_parser(subparsers)
    
    return parser

def _add_kb_parser(subparsers) -> None:
    """Add Knowledge Base Management commands"""
    kb_parser = subparsers.add_parser('kb', help='Knowledge Base Management')
    kb_subparsers = kb_parser.add_subparsers(
        dest='kb_command',
        title='available kb commands',
        metavar='{process,query,stats}'
    )
    
    # KB - Process Documents
    kb_process = kb_subparsers.add_parser('process', help='Process medical documents')
    kb_process.add_argument('--input', required=True, help='Input document path')
    kb_process.add_argument('--type', choices=['drug_label', 'guideline', 'trial'],
                          required=True, help='Document type')
    
    # KB - Query
    kb_query = kb_subparsers.add_parser('query', help='Query knowledge base')
    kb_query.add_argument('--entity', help='Entity to query (e.g., drug name)')
    kb_query.add_argument('--relation', help='Relation type (e.g., treats)')
    
    # KB - Stats
    kb_stats = kb_subparsers.add_parser('stats', help='View knowledge base statistics')

def _add_genomic_parser(subparsers) -> None:
    """Add Genomic Data Processing commands"""
    genomic_parser = subparsers.add_parser('genomic', help='Genomic Data Processing')
    genomic_subparsers = genomic_parser.add_subparsers(
        dest='genomic_command',
        title='available genomic commands',
        metavar='{process,analyze,harmonize}'
    )
    
    # Genomic - Process Data
    genomic_process = genomic_subparsers.add_parser('process', help='Process genomic data')
    genomic_process.add_argument('--vcf', required=True, help='Input VCF file')
    genomic_process.add_argument('--expression', required=True, help='Expression data file')
    genomic_process.add_argument('--output', help='Output directory')
    
    # Genomic - Analyze
    genomic_analyze = genomic_subparsers.add_parser('analyze', help='Analyze genomic data')
    genomic_analyze.add_argument('--input', required=True, help='Input data directory')
    genomic_analyze.add_argument('--analysis',
                               choices=['enrichment', 'correlation', 'de'],
                               required=True, help='Analysis type')
    
    # Genomic - Harmonize
    genomic_harmonize = genomic_subparsers.add_parser('harmonize', help='Harmonize genomic data')
    genomic_harmonize.add_argument('--input', required=True, help='Input directory')
    genomic_harmonize.add_argument('--output', help='Output directory')

def _add_bio_parser(subparsers) -> None:
    """Add Bioinformatics Analysis commands"""
    bio_parser = subparsers.add_parser('bio', help='Bioinformatics Analysis')
    bio_subparsers = bio_parser.add_subparsers(
        dest='bio_command',
        title='available bio commands',
        metavar='{pathway,expression,correlation}'
    )
    
    # Bio - Pathway Analysis
    bio_pathway = bio_subparsers.add_parser('pathway', help='Pathway enrichment analysis')
    bio_pathway.add_argument('--genes', required=True, help='Gene list file')
    bio_pathway.add_argument('--pathways', required=True, help='Pathway database file')
    
    # Bio - Expression Analysis
    bio_expression = bio_subparsers.add_parser('expression', help='Expression analysis')
    bio_expression.add_argument('--data', required=True, help='Expression data file')
    bio_expression.add_argument('--groups', required=True, help='Sample groups file')
    
    # Bio - Correlation Analysis
    bio_correlation = bio_subparsers.add_parser('correlation', help='Gene correlation analysis')
    bio_correlation.add_argument('--data', required=True, help='Expression data file')
    bio_correlation.add_argument('--genes', required=True, help='Gene pairs file')

def _add_doc_parser(subparsers) -> None:
    """Add Medical Document Processing commands"""
    doc_parser = subparsers.add_parser('doc', help='Medical Document Processing')
    doc_subparsers = doc_parser.add_subparsers(
        dest='doc_command',
        title='available doc commands',
        metavar='{extract,refs,report}'
    )
    
    # Doc - Extract
    doc_extract = doc_subparsers.add_parser('extract', help='Extract information from documents')
    doc_extract.add_argument('--input', required=True, help='Input document')
    doc_extract.add_argument('--type',
                           choices=['report', 'label', 'publication'],
                           required=True, help='Document type')
    
    # Doc - Process References
    doc_refs = doc_subparsers.add_parser('refs', help='Process document references')
    doc_refs.add_argument('--input', required=True, help='Input document')
    
    # Doc - Generate Report
    doc_report = doc_subparsers.add_parser('report', help='Generate document report')
    doc_report.add_argument('--input', required=True, help='Input document')
    doc_report.add_argument('--output', help='Output path')

def parse_args(args: Optional[list] = None) -> argparse.Namespace:
    """Parse command line arguments"""
    parser = create_parser()
    return parser.parse_args(args)