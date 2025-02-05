#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
HELLO_WORLD_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"

# Complex case: Multi-system trauma with complications
echo "Running complex trauma case..."
cd "$HELLO_WORLD_DIR" && python -m hello_world.main --prompt "22-year-old trauma patient from MVA. Multiple injuries including closed head trauma (GCS 12), chest wall contusion, suspected internal bleeding. BP 90/60, HR 130, RR 28, O2 sat 88%. Positive seat belt sign, complaining of severe abdominal pain. Multiple lacerations and right femur deformity noted." --task both
