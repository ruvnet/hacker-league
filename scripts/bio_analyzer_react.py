#!/usr/bin/env python3
"""
Bioinformatic Analysis Workflows using ReAct-style Tools

This script uses a ReAct-inspired architecture to orchestrate bioinformatics analyses:
- Gene-disease associations
- Drug-target interactions
- Pathway enrichment
- Expression correlation analysis
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests

class Tool:
    """Base class for analysis tools"""
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    def __call__(self, *args, **kwargs) -> str:
        raise NotImplementedError

class GeneAssociationTool(Tool):
    """Tool for gene-disease association analysis"""
    def __init__(self, variant_data: pd.DataFrame):
        super().__init__(
            name="gene_association",
            description="Analyze association between genes and disease"
        )
        self.variant_data = variant_data
    
    def __call__(self, genes: List[str], phenotype_data: Dict[str, int]) -> str:
        results = []
        phenotype = pd.Series(phenotype_data)
        
        for gene in genes:
            # Get variants in this gene
            gene_variants = self.variant_data[
                self.variant_data['gene_name'] == gene
            ]
            
            if len(gene_variants) == 0:
                continue
            
            # Calculate association statistics
            variant_samples = set(gene_variants['sample_id'])
            case_samples = set(phenotype[phenotype == 1].index)
            control_samples = set(phenotype[phenotype == 0].index)
            
            # Fisher's exact test
            table = [
                [len(variant_samples & case_samples),
                 len(variant_samples & control_samples)],
                [len(case_samples - variant_samples),
                 len(control_samples - variant_samples)]
            ]
            odds_ratio, pvalue = stats.fisher_exact(table)
            
            results.append({
                'gene': gene,
                'n_variants': len(gene_variants),
                'odds_ratio': odds_ratio,
                'pvalue': pvalue
            })
        
        if not results:
            return "No significant associations found"
            
        # Create results DataFrame
        results_df = pd.DataFrame(results)
        results_df['qvalue'] = multipletests(
            results_df['pvalue'], method='fdr_bh'
        )[1]
        
        return f"""
Gene-Disease Association Results:
{results_df.to_string()}
"""

class ExpressionCorrelationTool(Tool):
    """Tool for expression correlation analysis"""
    def __init__(self, expression_data: pd.DataFrame):
        super().__init__(
            name="expression_correlation",
            description="Analyze correlation between gene expression"
        )
        self.expression_data = expression_data
    
    def __call__(self, gene_x: str, gene_y: str) -> str:
        try:
            # Get expression values
            expr_x = self.expression_data.loc[gene_x]
            expr_y = self.expression_data.loc[gene_y]
            
            # Calculate correlation
            corr, pvalue = stats.pearsonr(expr_x, expr_y)
            
            return f"""
Expression Correlation Analysis:
- Correlation coefficient: {corr:.3f}
- P-value: {pvalue:.3f}
- Number of samples: {len(expr_x)}
"""
        except KeyError:
            return f"Error: One or both genes not found: {gene_x}, {gene_y}"

class PathwayEnrichmentTool(Tool):
    """Tool for pathway enrichment analysis"""
    def __init__(self, pathway_data: pd.DataFrame):
        super().__init__(
            name="pathway_enrichment",
            description="Analyze pathway enrichment"
        )
        self.pathway_data = pathway_data
    
    def __call__(self, genes: List[str], min_genes: int = 5) -> str:
        results = []
        query_genes = set(genes)
        
        for _, pathway in self.pathway_data.iterrows():
            pathway_genes = set(pathway['genes'].split(','))
            
            # Skip small pathways
            if len(pathway_genes) < min_genes:
                continue
            
            # Calculate overlap
            overlap_genes = query_genes & pathway_genes
            if len(overlap_genes) == 0:
                continue
            
            # Fisher's exact test
            table = [
                [len(overlap_genes),
                 len(query_genes - pathway_genes)],
                [len(pathway_genes - query_genes),
                 20000 - len(query_genes | pathway_genes)]
            ]
            odds_ratio, pvalue = stats.fisher_exact(table)
            
            results.append({
                'pathway_id': pathway['pathway_id'],
                'pathway_name': pathway['pathway_name'],
                'n_overlap': len(overlap_genes),
                'odds_ratio': odds_ratio,
                'pvalue': pvalue,
                'overlap_genes': ','.join(overlap_genes)
            })
        
        if not results:
            return "No significant pathway enrichment found"
            
        # Create results DataFrame
        results_df = pd.DataFrame(results)
        results_df['qvalue'] = multipletests(
            results_df['pvalue'], method='fdr_bh'
        )[1]
        
        return f"""
Pathway Enrichment Results:
{results_df.to_string()}
"""

class DrugTargetTool(Tool):
    """Tool for drug target analysis"""
    def __init__(self, drug_data: pd.DataFrame):
        super().__init__(
            name="drug_targets",
            description="Find drug targets for genes"
        )
        self.drug_data = drug_data
    
    def __call__(self, genes: List[str]) -> str:
        # Filter for specified genes
        target_info = self.drug_data[
            self.drug_data['target_gene'].isin(genes)
        ]
        
        if len(target_info) == 0:
            return "No drug targets found for specified genes"
            
        return f"""
Drug Target Analysis Results:
{target_info.to_string()}
"""

class BioAnalyzer:
    """ReAct-style orchestrator for bioinformatics analysis"""
    
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        
        # Load data
        print("Loading reference data...")
        self.load_data()
        
        # Initialize tools
        self.tools = {
            'gene_association': GeneAssociationTool(self.variant_data),
            'expression_correlation': ExpressionCorrelationTool(self.expression_data),
            'pathway_enrichment': PathwayEnrichmentTool(self.pathway_data),
            'drug_targets': DrugTargetTool(self.drug_data)
        }
    
    def load_data(self):
        """Load all reference data"""
        # Load expression data
        expr_file = self.data_dir / 'expression.csv'
        self.expression_data = pd.read_csv(expr_file, index_col='gene_id')
        
        # Load variant data
        var_file = self.data_dir / 'variants.csv'
        self.variant_data = pd.read_csv(var_file)
        
        # Load pathway data
        path_file = self.data_dir / 'pathways.csv'
        self.pathway_data = pd.read_csv(path_file)
        
        # Load drug data
        drug_file = self.data_dir / 'drug_targets.csv'
        self.drug_data = pd.read_csv(drug_file)
    
    def analyze_gene_disease(self, genes: List[str], phenotype: Dict[str, int]) -> str:
        """Run gene-disease association analysis"""
        return self.tools['gene_association'](genes, phenotype)
    
    def analyze_expression(self, gene_x: str, gene_y: str) -> str:
        """Run expression correlation analysis"""
        return self.tools['expression_correlation'](gene_x, gene_y)
    
    def analyze_pathways(self, genes: List[str], min_genes: int = 5) -> str:
        """Run pathway enrichment analysis"""
        return self.tools['pathway_enrichment'](genes, min_genes)
    
    def analyze_drugs(self, genes: List[str]) -> str:
        """Run drug target analysis"""
        return self.tools['drug_targets'](genes)

def main():
    # Initialize analyzer
    analyzer = BioAnalyzer(Path('data/bio_analysis'))
    
    # Example analyses
    genes = ['BRCA1', 'BRCA2', 'TP53']
    phenotype = {
        'SAMPLE1': 1,
        'SAMPLE2': 0,
        'SAMPLE3': 1
    }
    
    print("\nGene-Disease Associations:")
    print(analyzer.analyze_gene_disease(genes, phenotype))
    
    print("\nExpression Correlation:")
    print(analyzer.analyze_expression('BRCA1', 'BRCA2'))
    
    print("\nPathway Enrichment:")
    print(analyzer.analyze_pathways(genes))
    
    print("\nDrug Targets:")
    print(analyzer.analyze_drugs(genes))

if __name__ == '__main__':
    main()