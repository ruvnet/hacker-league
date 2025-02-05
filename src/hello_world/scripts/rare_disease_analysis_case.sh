#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
HELLO_WORLD_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"

# Advanced case: Rare disease diagnosis using multi-omic integration
echo "Running rare disease multi-omic analysis case..."
cd "$HELLO_WORLD_DIR" && python -m hello_world.main --prompt "Complex rare disease diagnostic case. 7-year-old patient with undiagnosed neurodevelopmental disorder. Whole genome sequencing reveals compound heterozygous variants in DOCK7 gene (c.2104C>T, p.Arg702* and c.3709G>A, p.Gly1237Arg), both ultra-rare (gnomAD AF < 0.0001%). RNA-seq from fibroblasts shows aberrant splicing affecting DOCK7. Proteomics confirms reduced DOCK7 protein levels and dysregulated Rac1 signaling. Metabolomics reveals altered sphingolipid metabolism. Phenotype analysis: Progressive microcephaly (-3.5 SD), cortical atrophy on brain MRI, seizures (focal onset), developmental delay, and distinctive facial features. Clinical history includes hypotonia, feeding difficulties in infancy. Family history: Consanguineous parents (first cousins), healthy siblings. Detailed phenotyping using HPO terms matches DOCK7-related epileptic encephalopathy. Single-cell RNA-seq from blood shows altered neural progenitor signatures. Cellular phenotyping demonstrates impaired neuronal migration in patient-derived cells. Phosphoproteomics indicates disrupted cytoskeletal regulation. Longitudinal brain imaging shows progressive white matter changes. Neurophysiology: Abnormal ERG responses. Plasma biomarkers suggest elevated neurofilament light chain." --task both
