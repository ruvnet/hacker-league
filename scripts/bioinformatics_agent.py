#!/usr/bin/env python3
"""
Bioinformatics Analysis Agent using ReAct Architecture

This agent performs bioinformatics analyses using a ReAct approach:
1. Observation: Load and validate biological data
2. Thought: Plan analysis strategy
3. Action: Execute analysis and interpret results
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from scipy import stats
from statsmodels.stats.multitest import multipletests

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
    PATHWAY = "🔄"          # Pathway/Process
    GENE = "🔍"             # Gene/Search

@dataclass
class AnalysisState:
    """State of the bioinformatics analysis"""
    expression_loaded: bool = False
    enrichment_done: bool = False
    correlation_done: bool = False
    de_done: bool = False
    expression_data: Optional[pd.DataFrame] = None
    error_log: List[str] = None

class BioinformaticsAgent:
    """ReAct-style agent for bioinformatics analysis"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.state = AnalysisState(error_log=[])
    
    def analyze_data(self,
                    expression_path: str,
                    pathway_db: Dict[str, List[str]],
                    gene_pairs: List[tuple],
                    group1_samples: List[str],
                    group2_samples: List[str]) -> str:
        """Run bioinformatics analyses"""
        
        # Load expression data
        print(f"\n{Colors.INFO}{Emojis.DNA} Loading expression data...{Colors.ENDC}")
        try:
            self.state.expression_data = pd.read_csv(expression_path, index_col=0)
            self.state.expression_loaded = True
            print(f"{Colors.SUCCESS}Loaded {self.state.expression_data.shape[0]} genes, "
                  f"{self.state.expression_data.shape[1]} samples{Colors.ENDC}")
        except Exception as e:
            self.state.error_log.append(f"Expression loading error: {str(e)}")
            return self._format_error_report()
        
        # Pathway enrichment
        print(f"\n{Colors.INFO}{Emojis.PATHWAY} Analyzing pathway enrichment...{Colors.ENDC}")
        enrichment_results = self._analyze_enrichment(
            gene_list=self.state.expression_data.index.tolist(),
            pathway_db=pathway_db
        )
        if enrichment_results is None:
            return self._format_error_report()
        self.state.enrichment_done = True
        
        # Gene correlations
        print(f"\n{Colors.INFO}{Emojis.LINK} Analyzing gene correlations...{Colors.ENDC}")
        correlation_results = self._analyze_correlations(gene_pairs)
        if correlation_results is None:
            return self._format_error_report()
        self.state.correlation_done = True
        
        # Differential expression
        print(f"\n{Colors.INFO}{Emojis.GENE} Performing differential expression...{Colors.ENDC}")
        de_results = self._analyze_differential_expression(
            group1_samples, group2_samples
        )
        if de_results is None:
            return self._format_error_report()
        self.state.de_done = True
        
        # Export results
        self._export_results(
            enrichment=enrichment_results,
            correlation=correlation_results,
            de=de_results
        )
        
        return self._format_success_report(
            enrichment=enrichment_results,
            correlation=correlation_results,
            de=de_results
        )
    
    def _analyze_enrichment(self, 
                          gene_list: List[str],
                          pathway_db: Dict[str, List[str]],
                          min_genes: int = 5) -> Optional[Dict[str, Any]]:
        """Perform pathway enrichment analysis"""
        try:
            results = []
            query_genes = set(gene_list)
            
            for pathway_id, pathway_genes in pathway_db.items():
                pathway_genes = set(pathway_genes)
                if len(pathway_genes) < min_genes:
                    continue
                
                overlap = query_genes & pathway_genes
                if not overlap:
                    continue
                
                # Fisher's exact test
                table = [
                    [len(overlap),
                     len(query_genes - pathway_genes)],
                    [len(pathway_genes - query_genes),
                     20000 - len(query_genes | pathway_genes)]
                ]
                odds_ratio, pvalue = stats.fisher_exact(table)
                
                results.append({
                    'pathway_id': pathway_id,
                    'overlap_size': len(overlap),
                    'pathway_size': len(pathway_genes),
                    'odds_ratio': odds_ratio,
                    'pvalue': pvalue,
                    'genes': list(overlap)
                })
            
            if results:
                # Multiple testing correction
                pvalues = [r['pvalue'] for r in results]
                qvalues = multipletests(pvalues, method='fdr_bh')[1]
                for res, qval in zip(results, qvalues):
                    res['qvalue'] = qval
            
            return {
                'enrichment': results,
                'total_pathways': len(pathway_db),
                'significant': sum(r['qvalue'] < 0.05 for r in results)
            }
            
        except Exception as e:
            self.state.error_log.append(f"Enrichment error: {str(e)}")
            return None
    
    def _analyze_correlations(self, 
                            gene_pairs: List[tuple]) -> Optional[Dict[str, Any]]:
        """Analyze gene expression correlations"""
        try:
            results = []
            for gene1, gene2 in gene_pairs:
                if gene1 not in self.state.expression_data.index or \
                   gene2 not in self.state.expression_data.index:
                    continue
                
                expr1 = self.state.expression_data.loc[gene1]
                expr2 = self.state.expression_data.loc[gene2]
                
                corr, pvalue = stats.pearsonr(expr1, expr2)
                
                results.append({
                    'gene1': gene1,
                    'gene2': gene2,
                    'correlation': corr,
                    'pvalue': pvalue
                })
            
            if results:
                # Multiple testing correction
                pvalues = [r['pvalue'] for r in results]
                qvalues = multipletests(pvalues, method='fdr_bh')[1]
                for res, qval in zip(results, qvalues):
                    res['qvalue'] = qval
            
            return {
                'correlations': results,
                'total_pairs': len(gene_pairs),
                'significant': sum(r['qvalue'] < 0.05 for r in results)
            }
            
        except Exception as e:
            self.state.error_log.append(f"Correlation error: {str(e)}")
            return None
    
    def _analyze_differential_expression(self,
                                      group1_samples: List[str],
                                      group2_samples: List[str]) -> Optional[Dict[str, Any]]:
        """Perform differential expression analysis"""
        try:
            results = []
            for gene in self.state.expression_data.index:
                expr1 = self.state.expression_data.loc[gene, group1_samples]
                expr2 = self.state.expression_data.loc[gene, group2_samples]
                
                tstat, pvalue = stats.ttest_ind(expr1, expr2)
                
                mean1 = np.mean(expr1)
                mean2 = np.mean(expr2)
                log2fc = np.log2(mean2 / mean1) if mean1 > 0 else np.nan
                
                results.append({
                    'gene': gene,
                    'log2fc': log2fc,
                    'pvalue': pvalue,
                    'mean1': mean1,
                    'mean2': mean2
                })
            
            # Convert to DataFrame for easier handling
            results_df = pd.DataFrame(results)
            
            # Multiple testing correction
            results_df['qvalue'] = multipletests(
                results_df['pvalue'].fillna(1), 
                method='fdr_bh'
            )[1]
            
            return {
                'de_results': results_df,
                'total_genes': len(results_df),
                'significant': sum(results_df['qvalue'] < 0.05)
            }
            
        except Exception as e:
            self.state.error_log.append(f"DE error: {str(e)}")
            return None
    
    def _export_results(self,
                       enrichment: Dict[str, Any],
                       correlation: Dict[str, Any],
                       de: Dict[str, Any]) -> None:
        """Export analysis results"""
        # Save enrichment results
        if enrichment['enrichment']:
            pd.DataFrame(enrichment['enrichment']).to_csv(
                self.output_dir / 'pathway_enrichment.csv'
            )
        
        # Save correlation results
        if correlation['correlations']:
            pd.DataFrame(correlation['correlations']).to_csv(
                self.output_dir / 'gene_correlations.csv'
            )
        
        # Save DE results
        de['de_results'].to_csv(self.output_dir / 'differential_expression.csv')
    
    def _format_success_report(self,
                             enrichment: Dict[str, Any],
                             correlation: Dict[str, Any],
                             de: Dict[str, Any]) -> str:
        """Format successful analysis report"""
        header = f"""
{Colors.HEADER}{Colors.BOLD}╔══════════════════════════════════════════════════════════════════╗
║                    BIOINFORMATICS ANALYSIS                       ║
╚══════════════════════════════════════════════════════════════════╝{Colors.ENDC}
"""
        sections = []

        # Analysis Status
        sections.append(f"""
{Colors.INFO}{Colors.BOLD}ANALYSIS STATUS:{Colors.ENDC}
{self._format_status_line('Expression Data', self.state.expression_loaded)}
{self._format_status_line('Pathway Enrichment', self.state.enrichment_done)}
{self._format_status_line('Gene Correlations', self.state.correlation_done)}
{self._format_status_line('Differential Expression', self.state.de_done)}
""")

        # Results Summary
        sections.append(f"""
{Colors.INFO}{Colors.BOLD}RESULTS SUMMARY:{Colors.ENDC}
{Emojis.PATHWAY} Pathway Enrichment:
  • Analyzed {enrichment['total_pathways']} pathways
  • Found {enrichment['significant']} significant (q<0.05)

{Emojis.LINK} Gene Correlations:
  • Analyzed {correlation['total_pairs']} gene pairs
  • Found {correlation['significant']} significant (q<0.05)

{Emojis.GENE} Differential Expression:
  • Analyzed {de['total_genes']} genes
  • Found {de['significant']} differentially expressed (q<0.05)
""")

        # Output Files
        sections.append(f"""
{Colors.SUCCESS}{Colors.BOLD}OUTPUT FILES:{Colors.ENDC}
{Emojis.REPORT} Pathway Results: {self.output_dir / 'pathway_enrichment.csv'}
{Emojis.CHART} Correlation Results: {self.output_dir / 'gene_correlations.csv'}
{Emojis.DNA} DE Results: {self.output_dir / 'differential_expression.csv'}
""")

        footer = f"""
{Colors.HEADER}▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀{Colors.ENDC}
"""

        return header + "\n".join(sections) + footer
    
    def _format_error_report(self) -> str:
        """Format error report"""
        return f"""
{Colors.HEADER}{Colors.BOLD}╔══════════════════════════════════════════════════════════════════╗
║                    ANALYSIS ERROR                               ║
╚══════════════════════════════════════════════════════════════════╝{Colors.ENDC}

{Colors.ALERT}{Emojis.WARNING} Analysis Status:{Colors.ENDC}
{self._format_status_line('Expression Data', self.state.expression_loaded)}
{self._format_status_line('Pathway Enrichment', self.state.enrichment_done)}
{self._format_status_line('Gene Correlations', self.state.correlation_done)}
{self._format_status_line('Differential Expression', self.state.de_done)}

{Colors.ALERT}{Colors.BOLD}ERROR LOG:{Colors.ENDC}
""" + "\n".join(f"{Colors.ALERT}{Emojis.ERROR} {err}{Colors.ENDC}" 
                for err in self.state.error_log) + f"""

{Colors.INFO}{Emojis.INFO} Please review errors and resubmit analysis.{Colors.ENDC}

{Colors.HEADER}▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀{Colors.ENDC}
"""

    def _format_status_line(self, label: str, status: bool) -> str:
        """Format a status line with appropriate emoji and color"""
        emoji = Emojis.SUCCESS if status else Emojis.ERROR
        color = Colors.SUCCESS if status else Colors.ALERT
        return f"{color}{emoji} {label}: {'Completed' if status else 'Failed'}{Colors.ENDC}"

def main():
    # Initialize agent
    agent = BioinformaticsAgent(Path('data/bio_analysis'))
    
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}")
    print(f"Bioinformatics Analysis System")
    print(f"{'='*70}{Colors.ENDC}")
    
    # Example pathway database
    pathway_db = {
        "DNA_REPAIR": ["BRCA1", "BRCA2", "TP53", "PTEN"],
        "CELL_CYCLE": ["TP53", "CCND1", "CDK4", "RB1"]
    }
    
    # Example gene pairs to correlate
    gene_pairs = [
        ("BRCA1", "BRCA2"),
        ("EGFR", "MET")
    ]
    
    # Example sample groups
    group1 = ["SAMPLE1", "SAMPLE2"]  # e.g., control
    group2 = ["SAMPLE3"]             # e.g., treatment
    
    # Run analysis
    result = agent.analyze_data(
        expression_path='data/bio_analysis/expression.csv',
        pathway_db=pathway_db,
        gene_pairs=gene_pairs,
        group1_samples=group1,
        group2_samples=group2
    )
    
    print(result)

if __name__ == '__main__':
    main()