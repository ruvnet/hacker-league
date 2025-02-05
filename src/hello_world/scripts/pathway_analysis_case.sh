#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
HELLO_WORLD_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"

# Advanced case: Multi-omic pathway analysis with drug response prediction
echo "Running pathway analysis case with drug response prediction..."
cd "$HELLO_WORLD_DIR" && python -m hello_world.main --prompt "Integrative analysis of treatment-resistant metastatic melanoma. RNA-seq shows upregulated MAPK and PI3K pathways. Proteomics reveals elevated PD-L1 expression and altered metabolic signatures. Phosphoproteomics indicates hyperactive AKT signaling. Previous treatment history: Failed response to BRAF inhibitor (dabrafenib) and anti-PD1 therapy (pembrolizumab). Tumor mutation burden: high (45 mut/Mb). Key mutations: BRAF V600E, PTEN loss, NF1 truncation. Metabolomics shows elevated lactate and glutamine utilization. Bulk RNA-seq from three tumor sites shows heterogeneous MITF program activation. Single-cell RNA-seq reveals distinct resistant subpopulations with stem-like features. Circulating tumor DNA analysis detects emerging NRAS Q61K mutation in 15% of reads. Patient experiencing rapid progression with new brain metastases." --task both
