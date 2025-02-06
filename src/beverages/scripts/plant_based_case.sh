#!/bin/bash
cd "$(dirname "$0")/.." && python -m beverages.main --prompt "Analyze market potential for plant-based beverage alternatives. Focus on dairy alternatives, protein-enriched drinks, and innovative plant-based formulations. Consider sustainability, nutritional equivalence, and consumer acceptance factors." --task both
