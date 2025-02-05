#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
HELLO_WORLD_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"

# Oncology case: Medical image analysis with clinical correlation
echo "Running oncology imaging case..."
cd "$HELLO_WORLD_DIR" && python -m hello_world.main --prompt "Patient presents with suspicious mass on chest CT. 3cm lesion in right upper lobe with spiculated margins. Previous imaging from 6 months ago showed 1.5cm nodule. Recent weight loss and fatigue. Former smoker with 30 pack-year history. Family history of lung cancer in father." --task both
