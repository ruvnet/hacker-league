#!/bin/bash

# Master script to run all medical cases with different complexity levels
echo "Running all medical cases..."

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
HELLO_WORLD_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"

# Ensure all scripts are executable
chmod +x "$SCRIPT_DIR"/*.sh

echo -e "\n=== Running General Medical Cases ==="

# Simple case
echo -e "\n-> Running Simple Case"
echo "Basic headache assessment"
cd "$HELLO_WORLD_DIR" && python -m hello_world.main --prompt "Patient presents with moderate headache for 2 days, no other symptoms. No history of migraines." --task both

# Moderate case
echo -e "\n-> Running Moderate Case"
echo "Diabetic patient with complications"
cd "$HELLO_WORLD_DIR" && python -m hello_world.main --prompt "65-year-old diabetic patient presents with fatigue, polyuria, polydipsia for 1 week. Blood glucose reading at home was 385 mg/dL. History of hypertension and peripheral neuropathy." --task both

# Complex case
echo -e "\n-> Running Complex Case"
echo "Multi-system trauma"
cd "$HELLO_WORLD_DIR" && python -m hello_world.main --prompt "22-year-old trauma patient from MVA. Multiple injuries including closed head trauma (GCS 12), chest wall contusion, suspected internal bleeding. BP 90/60, HR 130, RR 28, O2 sat 88%. Positive seat belt sign, complaining of severe abdominal pain. Multiple lacerations and right femur deformity noted." --task both

echo -e "\n=== Running Oncology Cases ==="

# Oncology imaging case
echo -e "\n-> Running Oncology Imaging Case"
echo "Suspicious lung mass analysis"
cd "$HELLO_WORLD_DIR" && python -m hello_world.main --prompt "Patient presents with suspicious mass on chest CT. 3cm lesion in right upper lobe with spiculated margins. Previous imaging from 6 months ago showed 1.5cm nodule. Recent weight loss and fatigue. Former smoker with 30 pack-year history. Family history of lung cancer in father." --task both

# Genomic analysis case
echo -e "\n-> Running Genomic Analysis Case"
echo "Breast cancer molecular profiling"
cd "$HELLO_WORLD_DIR" && python -m hello_world.main --prompt "Patient with newly diagnosed breast cancer. Tumor sequencing reveals BRCA1 mutation (c.181T>G), PIK3CA mutation, and elevated HER2 expression. 45-year-old female, premenopausal, no previous cancer history. Mother and sister with history of ovarian cancer. Tumor size 2.5cm, grade 3, triple-negative on IHC." --task both

# Multi-modal oncology case
echo -e "\n-> Running Multi-modal Oncology Case"
echo "Comprehensive cancer workup"
cd "$HELLO_WORLD_DIR" && python -m hello_world.main --prompt "Patient undergoing comprehensive cancer workup. PET-CT shows hypermetabolic lesions in liver (SUV 8.5) and multiple bone metastases. Liver biopsy reveals poorly differentiated adenocarcinoma, CK7+/CK20-, TTF1+. NGS panel shows EGFR exon 19 deletion and TP53 mutation. Previous chest CT from 3 months ago showed 4.2cm right lower lobe mass. 58-year-old Asian female, never-smoker, with progressive fatigue and 15-pound weight loss over 2 months." --task both

echo -e "\n=== Running Advanced Analysis Cases ==="

# Pathway analysis case
echo -e "\n-> Running Pathway Analysis Case"
echo "Multi-omic pathway analysis with drug response prediction"
"$SCRIPT_DIR/pathway_analysis_case.sh"

# Immunotherapy prediction case
echo -e "\n-> Running Immunotherapy Prediction Case"
echo "Complex immunotherapy response analysis"
"$SCRIPT_DIR/immunotherapy_prediction_case.sh"

# Neurodegenerative analysis case
echo -e "\n-> Running Neurodegenerative Analysis Case"
echo "Advanced neurodegenerative disease analysis"
"$SCRIPT_DIR/neuro_analysis_case.sh"

# Rare disease analysis case
echo -e "\n-> Running Rare Disease Analysis Case"
echo "Complex rare disease diagnostic analysis"
"$SCRIPT_DIR/rare_disease_analysis_case.sh"

echo -e "\n=== All cases completed ==="
