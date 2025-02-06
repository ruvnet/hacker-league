#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Running all beverage analysis cases..."
echo "========================================"

echo -e "\n1. Health-Focused Beverage Development"
"$SCRIPT_DIR/health_focused_case.sh"

echo -e "\n2. Plant-Based Alternative Analysis"
"$SCRIPT_DIR/plant_based_case.sh"

echo -e "\n3. Functional Beverage Innovation"
"$SCRIPT_DIR/functional_beverage_case.sh"

echo -e "\n4. Sustainable Packaging Design"
"$SCRIPT_DIR/sustainable_packaging_case.sh"

echo -e "\nAll cases completed."
