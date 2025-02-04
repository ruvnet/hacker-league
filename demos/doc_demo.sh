#!/bin/bash

# Medical Document Processing Demo Script
# This script demonstrates document processing and analysis workflow

echo "Medical Document Processing Demo"
echo "=============================="

# Extract information from a medical document
echo "1. Extracting information from clinical report..."
python -m src.oncology.cli doc extract \
    --input src/oncology/tests/sample_data/report.txt \
    --type report

# Process document references
echo -e "\n2. Processing document references..."
python -m src.oncology.cli doc refs \
    --input src/oncology/tests/sample_data/report.txt

# Generate analysis report
echo -e "\n3. Generating analysis report..."
python -m src.oncology.cli doc report \
    --input src/oncology/tests/sample_data/report.txt \
    --output reports/analysis_report.pdf

# Process multiple document types
echo -e "\n4. Processing medical image data..."
python -m src.oncology.cli doc extract \
    --input src/oncology/tests/sample_data/image.txt \
    --type image

# Generate comprehensive report
echo -e "\n5. Generating comprehensive medical report..."
python -m src.oncology.cli doc report \
    --input src/oncology/tests/sample_data/report.txt \
    --output reports/comprehensive_report.pdf
