#!/bin/bash
cd "$(dirname "$0")/.." && python -m beverages.main --prompt "Design a functional beverage with targeted health benefits. Focus on cognitive enhancement, energy management, or sports recovery. Consider ingredient synergies, bioavailability, and scientific evidence supporting functional claims." --task both
