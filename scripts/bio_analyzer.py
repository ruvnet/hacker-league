#!/usr/bin/env python3
"""
Bioinformatic Analysis Workflows

This script demonstrates analysis workflows for investigating biological relationships:
- Gene-disease associations
- Drug-target interactions
- Pathway enrichment
- Expression correlation analysis
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass
from scipy import stats
from statsmodels.stats.multitest import multipletests

@dataclass
class GeneSet:
    """Represents a set of genes (e.g., pathway, GO term)"""
    id: str
    name: str
    genes: Set[str]
    source: str
    description: Optional[str] = None

class BioAnalyzer:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        
        # Load reference data
        self.pathways: Dict[str, GeneSet] = {}
        self.expression_data: Optional[pd.DataFrame] = None
        self.variant_data: Optional[pd.DataFrame] = None
        self.drug_target_data: Optional[pd.DataFrame] = None
        
        self.load_data()
    
    def load_data(self) -> None:
        """Load all necessary data for analysis"""
        print("Loading reference data...")
        
        # Load pathway definitions
        pathway_file = self.data_dir / 'pathways.csv'
        if pathway_file.exists():
            df = pd.read_csv(pathway_file)
            for _, row in df.iterrows():
                genes = set(row['genes'].split(','))
                self.pathways[row['pathway_id']] = GeneSet(
                    id=row['pathway_id'],
                    name=row['pathway_name'],
                    genes=genes,
                    source=row['source'],
                    description=row['description']
                )
        
        # Load expression data
        expr_file = self.data_dir / 'expression.csv'
        if expr_file.exists():
            self.expression_data = pd.read_csv(expr_file)
            self.expression_data.set_index('gene_id', inplace=True)
        
        # Load variant data
        var_file = self.data_dir / 'variants.csv'
        if var_file.exists():
            self.variant_data = pd.read_csv(var_file)
        
        # Load drug-target data
        drug_file = self.data_dir / 'drug_targets.csv'
        if drug_file.exists():
            self.drug_target_data = pd.read_csv(drug_file)
    
    def analyze_gene_disease_association(self, 
                                      gene_list: List[str],
                                      phenotype_data: pd.Series) -> pd.DataFrame:
        """
        Analyze association between gene variants and disease phenotype
        
        Args:
            gene_list: List of genes to analyze
            phenotype_data: Series of phenotype values for samples
            
        Returns:
            DataFrame with association statistics
        """
        results = []
        
        if self.variant_data is None:
            return pd.DataFrame()
        
        for gene in gene_list:
            # Get variants in this gene
            gene_variants = self.variant_data[
                self.variant_data['gene_name'] == gene
            ]
            
            if len(gene_variants) == 0:
                continue
            
            # Calculate association statistics
            variant_samples = set(gene_variants['sample_id'])
            case_samples = set(phenotype_data[phenotype_data == 1].index)
            control_samples = set(phenotype_data[phenotype_data == 0].index)
            
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
        
        # Create results DataFrame
        results_df = pd.DataFrame(results)
        if len(results_df) > 0:
            # Multiple testing correction
            results_df['qvalue'] = multipletests(
                results_df['pvalue'], method='fdr_bh'
            )[1]
            return results_df.sort_values('pvalue')
        
        return pd.DataFrame()
    
    def analyze_expression_correlation(self,
                                    gene_x: str,
                                    gene_y: str) -> Dict[str, float]:
        """
        Analyze correlation between expression of two genes
        
        Args:
            gene_x: First gene name
            gene_y: Second gene name
            
        Returns:
            Dictionary with correlation statistics
        """
        if self.expression_data is None:
            return {'error': 'No expression data loaded'}
            
        try:
            # Get expression values
            expr_x = self.expression_data.loc[gene_x]
            expr_y = self.expression_data.loc[gene_y]
            
            # Calculate correlation
            corr, pvalue = stats.pearsonr(expr_x, expr_y)
            
            return {
                'correlation': corr,
                'pvalue': pvalue,
                'n_samples': len(expr_x)
            }
        except KeyError:
            return {
                'error': f'One or both genes not found in expression data: {gene_x}, {gene_y}'
            }
    
    def analyze_pathway_enrichment(self,
                                 gene_list: List[str],
                                 min_genes: int = 5) -> pd.DataFrame:
        """
        Perform pathway enrichment analysis
        
        Args:
            gene_list: List of genes to analyze
            min_genes: Minimum number of genes for pathway
            
        Returns:
            DataFrame with enrichment results
        """
        results = []
        query_genes = set(gene_list)
        
        for pathway_id, pathway in self.pathways.items():
            # Skip small pathways
            if len(pathway.genes) < min_genes:
                continue
            
            # Calculate overlap
            overlap_genes = query_genes & pathway.genes
            if len(overlap_genes) == 0:
                continue
            
            # Fisher's exact test
            table = [
                [len(overlap_genes),
                 len(query_genes - pathway.genes)],
                [len(pathway.genes - query_genes),
                 20000 - len(query_genes | pathway.genes)]  # Approximate background
            ]
            odds_ratio, pvalue = stats.fisher_exact(table)
            
            results.append({
                'pathway_id': pathway_id,
                'pathway_name': pathway.name,
                'n_overlap': len(overlap_genes),
                'odds_ratio': odds_ratio,
                'pvalue': pvalue,
                'overlap_genes': ','.join(overlap_genes)
            })
        
        # Create results DataFrame
        results_df = pd.DataFrame(results)
        if len(results_df) > 0:
            # Multiple testing correction
            results_df['qvalue'] = multipletests(
                results_df['pvalue'], method='fdr_bh'
            )[1]
            return results_df.sort_values('pvalue')
            
        return pd.DataFrame(columns=[
            'pathway_id', 'pathway_name', 'n_overlap', 
            'odds_ratio', 'pvalue', 'qvalue', 'overlap_genes'
        ])
    
    def analyze_differential_expression(self,
                                     data_file: str,
                                     groups_file: str) -> Dict[str, Any]:
        """
        Perform differential expression analysis between groups
        
        Args:
            data_file: Path to expression data CSV
            groups_file: Path to sample groups CSV
            
        Returns:
            Dictionary with analysis results
        """
        try:
            # Load expression data
            expr_data = pd.read_csv(data_file, index_col=0)
            
            # Load group definitions
            groups_data = pd.read_csv(groups_file)
            group1_samples = groups_data[groups_data['group'] == 1]['sample'].tolist()
            group2_samples = groups_data[groups_data['group'] == 2]['sample'].tolist()
            
            results = []
            for gene in expr_data.index:
                # Get expression values for each group
                expr1 = expr_data.loc[gene, group1_samples]
                expr2 = expr_data.loc[gene, group2_samples]
                
                # Calculate statistics
                tstat, pvalue = stats.ttest_ind(expr1, expr2)
                
                # Calculate fold change
                mean1 = np.mean(expr1)
                mean2 = np.mean(expr2)
                log2fc = np.log2(mean2 / mean1) if mean1 > 0 else np.nan
                
                results.append({
                    'gene': gene,
                    'log2fc': log2fc,
                    'pvalue': pvalue,
                    'mean_group1': mean1,
                    'mean_group2': mean2
                })
            
            # Create results DataFrame
            results_df = pd.DataFrame(results)
            
            # Multiple testing correction
            results_df['qvalue'] = multipletests(
                results_df['pvalue'].fillna(1),
                method='fdr_bh'
            )[1]
            
            # Sort by significance
            results_df = results_df.sort_values('pvalue')
            
            # Save results
            output_file = self.data_dir / 'differential_expression.csv'
            results_df.to_csv(output_file)
            
            return {
                'success': True,
                'n_genes': len(results_df),
                'significant': sum(results_df['qvalue'] < 0.05),
                'results_file': str(output_file),
                'data': results_df.to_dict('records')
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def find_drug_targets(self, gene_list: List[str]) -> pd.DataFrame:
        """
        Find drugs targeting specified genes
        
        Args:
            gene_list: List of genes to analyze
            
        Returns:
            DataFrame with drug-target information
        """
        if self.drug_target_data is None:
            return pd.DataFrame()
            
        # Filter for specified genes
        target_info = self.drug_target_data[
            self.drug_target_data['target_gene'].isin(gene_list)
        ]
        
        return target_info.sort_values(['target_gene', 'drug_name'])

    def analyze_correlations(self,
                           data_file: str,
                           gene_pairs_file: str) -> Dict[str, Any]:
        """
        Analyze correlations for multiple gene pairs
        
        Args:
            data_file: Path to expression data CSV
            gene_pairs_file: Path to gene pairs CSV (columns: gene1, gene2)
            
        Returns:
            Dictionary with correlation results
        """
        try:
            # Load expression data
            expr_data = pd.read_csv(data_file, index_col=0)
            
            # Load gene pairs
            pairs_data = pd.read_csv(gene_pairs_file)
            
            results = []
            for _, row in pairs_data.iterrows():
                gene1, gene2 = row['gene1'], row['gene2']
                
                # Get expression values
                try:
                    expr1 = expr_data.loc[gene1]
                    expr2 = expr_data.loc[gene2]
                    
                    # Calculate correlation
                    corr, pvalue = stats.pearsonr(expr1, expr2)
                    
                    results.append({
                        'gene1': gene1,
                        'gene2': gene2,
                        'correlation': corr,
                        'pvalue': pvalue
                    })
                except KeyError:
                    print(f"Warning: Genes not found: {gene1}, {gene2}")
                    continue
            
            # Create results DataFrame
            results_df = pd.DataFrame(results)
            
            if len(results_df) > 0:
                # Multiple testing correction
                results_df['qvalue'] = multipletests(
                    results_df['pvalue'].fillna(1),
                    method='fdr_bh'
                )[1]
                
                # Sort by significance
                results_df = results_df.sort_values('pvalue')
                
                # Save results
                output_file = self.data_dir / 'gene_correlations.csv'
                results_df.to_csv(output_file)
                
                return {
                    'success': True,
                    'n_pairs': len(results_df),
                    'significant': sum(results_df['qvalue'] < 0.05),
                    'results_file': str(output_file),
                    'data': results_df.to_dict('records')
                }
            
            return {
                'success': True,
                'n_pairs': 0,
                'significant': 0,
                'results_file': None,
                'data': []
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

def main():
    # Initialize analyzer
    analyzer = BioAnalyzer(Path('data/bio_analysis'))
    
    # Example: Gene-disease association
    phenotype = pd.Series({
        'SAMPLE1': 1,
        'SAMPLE2': 0,
        'SAMPLE3': 1
    })
    genes = ['BRCA1', 'BRCA2', 'TP53']
    
    print("\nGene-Disease Associations:")
    results = analyzer.analyze_gene_disease_association(genes, phenotype)
    print(results)
    
    # Example: Expression correlation
    print("\nExpression Correlation:")
    corr = analyzer.analyze_expression_correlation('BRCA1', 'BRCA2')
    print(corr)
    
    # Example: Pathway enrichment
    print("\nPathway Enrichment:")
    enrichment = analyzer.analyze_pathway_enrichment(genes)
    print(enrichment)
    
    # Example: Drug targets
    print("\nDrug Targets:")
    drugs = analyzer.find_drug_targets(genes)
    print(drugs)

if __name__ == '__main__':
    main()