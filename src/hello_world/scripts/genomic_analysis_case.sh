#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
HELLO_WORLD_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"

# Oncology case: Genomic analysis with clinical correlation
echo "Running genomic analysis case..."
cd "$HELLO_WORLD_DIR" && python -m hello_world.main --prompt "Patient with newly diagnosed breast cancer. Tumor sequencing reveals BRCA1 mutation (c.181T>G), PIK3CA mutation, and elevated HER2 expression. 45-year-old female, premenopausal, no previous cancer history. Mother and sister with history of ovarian cancer. Tumor size 2.5cm, grade 3, triple-negative on IHC." --task both
