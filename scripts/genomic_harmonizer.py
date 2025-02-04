#!/usr/bin/env python3
"""
Genomic Data Harmonizer

This script demonstrates harmonization of genomic data from multiple sources:
- Clinical sequencing data (VCF files)
- Expression data (RNA-seq)
- Clinical annotations
- Variant databases (ClinVar, COSMIC, etc.)

It standardizes data formats and integrates annotations across sources.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class DataSource(Enum):
    """Supported genomic data sources"""
    VCF = "vcf"
    RNA_SEQ = "rna_seq"
    CLINVAR = "clinvar"
    COSMIC = "cosmic"
    CLINICAL = "clinical"

@dataclass
class GenomicVariant:
    """Represents a genomic variant"""
    chrom: str
    pos: int
    ref: str
    alt: str
    qual: float
    filter_status: str
    annotations: Dict[str, Any]
    
@dataclass
class ExpressionData:
    """Represents gene expression data"""
    gene_id: str
    gene_name: str
    expression_value: float
    sample_id: str
    metadata: Dict[str, Any]

class GenomicHarmonizer:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize data stores
        self.variants: Dict[str, GenomicVariant] = {}
        self.expression_data: Dict[str, List[ExpressionData]] = {}
        self.clinical_annotations: Dict[str, Dict[str, Any]] = {}
        
    def load_vcf(self, vcf_path: Path) -> None:
        """Load and parse VCF file"""
        print(f"Loading VCF: {vcf_path}")
        variants = []
        with open(vcf_path) as f:
            for line in f:
                if line.startswith('#'):
                    continue
                
                fields = line.strip().split('\t')
                if len(fields) < 8:
                    continue
                
                # Parse INFO field
                info_dict = {}
                for item in fields[7].split(';'):
                    if '=' in item:
                        key, value = item.split('=')
                        info_dict[key] = value
                
                variant = GenomicVariant(
                    chrom=fields[0],
                    pos=int(fields[1]),
                    ref=fields[3],
                    alt=fields[4],
                    qual=float(fields[5]),
                    filter_status=fields[6],
                    annotations={
                        'gene': info_dict.get('GENE'),
                        'impact': info_dict.get('IMPACT')
                    }
                )
                
                variant_id = f"{fields[0]}_{fields[1]}_{fields[3]}_{fields[4]}"
                self.variants[variant_id] = variant
        
    def load_expression_data(self, expression_path: Path) -> None:
        """Load RNA-seq expression data"""
        print(f"Loading expression data: {expression_path}")
        df = pd.read_csv(expression_path)
        
        # Assuming first column is gene_id and rest are samples
        gene_ids = df.iloc[:, 0]
        expression_values = df.iloc[:, 1:]
        
        for gene_id, row in zip(gene_ids, expression_values.values):
            expressions = []
            for sample_id, value in zip(expression_values.columns, row):
                expr = ExpressionData(
                    gene_id=gene_id,
                    gene_name=gene_id,  # Using gene_id as name for now
                    expression_value=value,
                    sample_id=sample_id,
                    metadata={}
                )
                expressions.append(expr)
            self.expression_data[gene_id] = expressions
        
    def load_clinvar(self) -> None:
        """Load ClinVar annotations"""
        print("Loading ClinVar annotations")
        # In real system: Use ClinVar API or downloaded database
        
    def load_cosmic(self) -> None:
        """Load COSMIC annotations"""
        print("Loading COSMIC annotations")
        # In real system: Query COSMIC database
        
    def load_clinical_data(self, clinical_path: Path) -> None:
        """Load clinical annotations"""
        print(f"Loading clinical data: {clinical_path}")
        # In real system: Parse clinical data files
        
    def harmonize_variant_annotations(self) -> pd.DataFrame:
        """Harmonize variant annotations across sources"""
        harmonized_variants = []
        
        for variant_id, variant in self.variants.items():
            # Collect annotations from different sources
            annotations = {
                'variant_id': variant_id,
                'chrom': variant.chrom,
                'pos': variant.pos,
                'ref': variant.ref,
                'alt': variant.alt,
                'qual': variant.qual,
                'filter_status': variant.filter_status,
                'gene': variant.annotations.get('gene'),
                'impact': variant.annotations.get('impact')
            }
            
            # Add ClinVar annotations if available
            clinvar_data = variant.annotations.get('clinvar', {})
            annotations.update({
                'clinvar_significance': clinvar_data.get('significance'),
                'clinvar_phenotypes': clinvar_data.get('phenotypes')
            })
            
            # Add COSMIC annotations if available
            cosmic_data = variant.annotations.get('cosmic', {})
            annotations.update({
                'cosmic_id': cosmic_data.get('cosmic_id'),
                'cosmic_primary_site': cosmic_data.get('primary_site')
            })
            
            harmonized_variants.append(annotations)
        
        df = pd.DataFrame(harmonized_variants)
        # Ensure consistent column order
        columns = [
            'variant_id', 'chrom', 'pos', 'ref', 'alt', 'qual', 
            'filter_status', 'gene', 'impact', 'clinvar_significance',
            'clinvar_phenotypes', 'cosmic_id', 'cosmic_primary_site'
        ]
        # Only include columns that exist
        columns = [c for c in columns if c in df.columns]
        return df[columns]
    
    def harmonize_expression_data(self) -> pd.DataFrame:
        """Harmonize expression data across samples"""
        expression_records = []
        
        for gene_id, expressions in self.expression_data.items():
            for expr in expressions:
                record = {
                    'gene_id': expr.gene_id,
                    'gene_name': expr.gene_name,
                    'expression_value': expr.expression_value,
                    'sample_id': expr.sample_id
                }
                record.update(expr.metadata)
                expression_records.append(record)
        
        df = pd.DataFrame(expression_records)
        # Ensure consistent column order
        columns = ['gene_id', 'gene_name', 'sample_id', 'expression_value']
        # Only include columns that exist
        columns = [c for c in columns if c in df.columns]
        return df[columns]

    def create_variant_gene_links(self) -> pd.DataFrame:
        """Create links between variants and gene expression"""
        links = []
        
        # Get variants with gene annotations
        variants_df = self.harmonize_variant_annotations()
        variants_with_genes = variants_df[variants_df['gene'].notna()]
        
        # Get expression data
        expression_df = self.harmonize_expression_data()
        
        # Create links where genes match
        for _, variant in variants_with_genes.iterrows():
            gene = variant['gene']
            if gene in self.expression_data:
                # Get mean expression for this gene
                gene_expr = expression_df[expression_df['gene_id'] == gene]
                mean_expr = gene_expr['expression_value'].mean()
                
                links.append({
                    'variant_id': variant['variant_id'],
                    'gene': gene,
                    'impact': variant['impact'],
                    'mean_expression': mean_expr,
                    'chrom': variant['chrom'],
                    'pos': variant['pos']
                })
        
        df = pd.DataFrame(links)
        if len(df) > 0:
            # Ensure consistent column order
            columns = ['variant_id', 'gene', 'impact', 'mean_expression', 'chrom', 'pos']
            df = df[columns]
        return df
    
    def export_harmonized_data(self) -> None:
        """Export harmonized genomic data"""
        # Export harmonized variants
        variants_df = self.harmonize_variant_annotations()
        variants_df.to_csv(self.output_dir / 'harmonized_variants.csv', index=False, sep='\t')
        
        # Export harmonized expression data
        expression_df = self.harmonize_expression_data()
        expression_df.to_csv(self.output_dir / 'harmonized_expression.csv', index=False, sep='\t')
        
        # Export variant-gene links
        links_df = self.create_variant_gene_links()
        if len(links_df) > 0:
            links_df.to_csv(self.output_dir / 'variant_gene_links.csv', index=False, sep='\t')
        
        # Export integration stats
        stats = {
            'total_variants': len(self.variants),
            'total_genes': len(self.expression_data),
            'linked_variants': len(links_df),
            'timestamp': pd.Timestamp.now().isoformat()
        }
        pd.Series(stats).to_json(self.output_dir / 'integration_stats.json')
        
        print(f"Exported harmonized data to {self.output_dir}")

def main():
    # Initialize harmonizer
    harmonizer = GenomicHarmonizer(Path('data/harmonized'))
    
    # Load data from different sources
    harmonizer.load_vcf(Path('data/variants/sample1.vcf'))
    harmonizer.load_expression_data(Path('data/expression/sample1.counts'))
    harmonizer.load_clinvar()
    harmonizer.load_cosmic()
    harmonizer.load_clinical_data(Path('data/clinical/annotations.csv'))
    
    # Export harmonized data
    harmonizer.export_harmonized_data()

if __name__ == '__main__':
    main()