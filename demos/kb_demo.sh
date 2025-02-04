#!/bin/bash

# Knowledge Base Management Demo Script
# This script demonstrates common knowledge base operations

echo "Knowledge Base Management Demo"
echo "============================"

# Process a drug label document
echo "1. Processing drug label document..."
python -m src.oncology.cli kb process \
    --input data/knowledge_base/drug_labels/example_label.xml \
    --type drug_label

# Query the knowledge base for a drug
echo -e "\n2. Querying knowledge base for drug information..."
python -m src.oncology.cli kb query \
    --entity "Tamoxifen" \
    --relation "treats"

# View knowledge base statistics
echo -e "\n3. Displaying knowledge base statistics..."
python -m src.oncology.cli kb stats
