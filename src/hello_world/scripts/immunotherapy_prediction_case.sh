#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
HELLO_WORLD_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"

# Advanced case: Immunotherapy response prediction using multi-modal data
echo "Running immunotherapy response prediction analysis..."
cd "$HELLO_WORLD_DIR" && python -m hello_world.main --prompt "Complex immunotherapy response analysis case. Patient with metastatic NSCLC being evaluated for immunotherapy. Spatial transcriptomics of tumor microenvironment shows distinct immune-hot and immune-cold regions. Single-cell immune profiling reveals: exhausted CD8+ T cells (high PD-1, TIM3, LAG3), active NK cell populations, and immunosuppressive Tregs. Bulk TCR sequencing shows restricted T cell clonality (Shannon diversity index: 3.2). Multiplex immunofluorescence imaging demonstrates tertiary lymphoid structure formation. Gut microbiome analysis shows high Akkermansia muciniphila abundance. Cytokine panel reveals elevated IL-6, IL-8, and TGF-beta. Immune cell deconvolution from RNA-seq suggests high M2 macrophage infiltration. HLA typing: A*02:01 positive with high neoantigen burden. Radiomics features from CT indicate heterogeneous immune infiltration patterns. Previous autoimmune history: mild psoriasis. Recent steroid use for radiation-induced pneumonitis." --task both
