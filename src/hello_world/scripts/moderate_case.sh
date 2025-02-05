#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
HELLO_WORLD_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"

# Moderate case: Diabetic patient with multiple symptoms
echo "Running moderate complexity diabetic case..."
cd "$HELLO_WORLD_DIR" && python -m hello_world.main --prompt "65-year-old diabetic patient presents with fatigue, polyuria, polydipsia for 1 week. Blood glucose reading at home was 385 mg/dL. History of hypertension and peripheral neuropathy." --task both
