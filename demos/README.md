# Oncology System CLI Demo Scripts

This directory contains example shell scripts demonstrating various features of the Oncology System CLI.

## Available Demos

### 1. Knowledge Base Management (`kb_demo.sh`)
Demonstrates:
- Processing drug label documents
- Querying the knowledge base
- Viewing knowledge base statistics

```bash
chmod +x kb_demo.sh
./kb_demo.sh
```

### 2. Genomic Data Processing (`genomic_demo.sh`)
Demonstrates:
- Processing genomic data files (VCF and expression data)
- Analyzing processed genomic data
- Harmonizing genomic data
- Running various bioinformatics analyses (pathway, expression, correlation)

```bash
chmod +x genomic_demo.sh
./genomic_demo.sh
```

### 3. Medical Document Processing (`doc_demo.sh`)
Demonstrates:
- Extracting information from clinical reports
- Processing document references
- Generating analysis reports
- Processing medical image data
- Creating comprehensive medical reports

```bash
chmod +x doc_demo.sh
./doc_demo.sh
```

## Prerequisites

1. Make sure you have the Oncology System installed and configured:
```bash
pip install -r requirements.txt
```

2. Required data files should be present in their respective directories:
- `data/knowledge_base/drug_labels/` - Drug label documents
- `data/bio_analysis/` - Genomic and expression data files
- `data/harmonized/variants/` - Variant data files
- `src/oncology/tests/sample_data/` - Sample medical documents

3. Make the scripts executable:
```bash
chmod +x demos/*.sh
```

## Usage Notes

- These scripts are designed to run from the project root directory
- Each script includes descriptive comments explaining the operations
- Scripts will create output directories as needed
- Check the console output for progress and any error messages

## Output Locations

- Knowledge base data: `data/knowledge_base/`
- Processed genomic data: `data/processed/`
- Harmonized genomic data: `data/harmonized_output/`
- Generated reports: `reports/`
