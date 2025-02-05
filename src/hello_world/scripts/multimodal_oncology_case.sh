#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
HELLO_WORLD_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"

# Oncology case: Multi-modal analysis combining imaging, pathology, and genomics
echo "Running multi-modal oncology analysis case..."
cd "$HELLO_WORLD_DIR" && python -m hello_world.main --prompt "Patient undergoing comprehensive cancer workup. PET-CT shows hypermetabolic lesions in liver (SUV 8.5) and multiple bone metastases. Liver biopsy reveals poorly differentiated adenocarcinoma, CK7+/CK20-, TTF1+. NGS panel shows EGFR exon 19 deletion and TP53 mutation. Previous chest CT from 3 months ago showed 4.2cm right lower lobe mass. 58-year-old Asian female, never-smoker, with progressive fatigue and 15-pound weight loss over 2 months." --task both
