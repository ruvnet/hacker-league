#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
HELLO_WORLD_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"

# Simple case: Basic headache assessment
echo "Running simple headache assessment case..."
cd "$HELLO_WORLD_DIR" && python -m hello_world.main --prompt "Patient presents with moderate headache for 2 days, no other symptoms. No history of migraines." --task both
