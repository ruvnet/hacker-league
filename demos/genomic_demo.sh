#!/bin/bash

# Genomic Data Processing Demo Script
# This script demonstrates genomic data processing and analysis workflow

echo "Genomic Data Processing Demo"
echo "=========================="

# Process genomic data files
echo "1. Processing genomic data..."
python -m src.oncology.cli genomic process \
    --vcf data/harmonized/variants/sample1.vcf \
    --expression data/bio_analysis/expression.csv \
    --output data/processed

# Analyze processed data
echo -e "\n2. Performing genomic analysis..."
python -m src.oncology.cli genomic analyze \
    --input data/processed \
    --analysis enrichment

# Harmonize genomic data
echo -e "\n3. Harmonizing genomic data..."
python -m src.oncology.cli genomic harmonize \
    --input data/harmonized/variants \
    --output data/harmonized_output

# Run bioinformatics analyses
echo -e "\n4. Running pathway analysis..."
python -m src.oncology.cli bio pathway \
    --genes data/bio_analysis/gene_pairs.csv \
    --pathways data/bio_analysis/pathways.csv

echo -e "\n5. Running expression analysis..."
python -m src.oncology.cli bio expression \
    --data data/bio_analysis/expression.csv \
    --groups data/bio_analysis/groups.csv

echo -e "\n6. Running correlation analysis..."
python -m src.oncology.cli bio correlation \
    --data data/bio_analysis/expression.csv \
    --genes data/bio_analysis/gene_pairs.csv
