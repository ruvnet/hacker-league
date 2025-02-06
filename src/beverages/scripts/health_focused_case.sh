#!/bin/bash
cd "$(dirname "$0")/.." && python -m beverages.main --prompt "Develop a health-focused beverage targeting wellness-conscious consumers. Focus on natural ingredients, functional benefits, and clean label formulation. Consider trends in immunity boosting, gut health, and mental wellness." --task both
