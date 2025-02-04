# Oncology System CLI Usage Guide

The Oncology System provides a comprehensive command-line interface (CLI) for managing and analyzing medical data. The CLI can be used in both interactive and command-line modes.

## Installation

The CLI is part of the Oncology System package. Make sure you have all dependencies installed:

```bash
pip install -r requirements.txt
```

## Running the CLI

### Interactive Mode

To start the interactive menu:

```bash
python -m src.oncology.cli
```

This will display a menu with the following options:
1. Knowledge Base Management
2. Genomic Data Processing
3. Bioinformatics Analysis
4. Medical Document Processing

### Command-Line Mode

The CLI supports direct command execution using the following format:

```bash
python -m src.oncology.cli <command> <subcommand> [options]
```

## Available Commands

### Knowledge Base Management (kb)

Manage and query the medical knowledge base.

#### Process Documents
```bash
python -m src.oncology.cli kb process --input <path> --type <type>

# Options:
--input     Path to the input document
--type      Document type: drug_label, guideline, or trial

# Example:
python -m src.oncology.cli kb process --input docs/drug_label.pdf --type drug_label
```

#### Query Knowledge Base
```bash
python -m src.oncology.cli kb query --entity <name> --relation <type>

# Options:
--entity    Entity to query (e.g., drug name)
--relation  Relation type (e.g., treats)

# Example:
python -m src.oncology.cli kb query --entity "Tamoxifen" --relation "treats"
```

#### View Statistics
```bash
python -m src.oncology.cli kb stats
```

### Genomic Data Processing (genomic)

Process and analyze genomic data files.

#### Process Data
```bash
python -m src.oncology.cli genomic process --vcf <file> --expression <file> [--output <dir>]

# Options:
--vcf         Input VCF file
--expression  Expression data file
--output      Output directory (optional)

# Example:
python -m src.oncology.cli genomic process \
    --vcf data/variants.vcf \
    --expression data/expression.csv
```

#### Analyze Data
```bash
python -m src.oncology.cli genomic analyze --input <dir> --analysis <type>

# Options:
--input     Input data directory
--analysis  Analysis type: enrichment, correlation, or de

# Example:
python -m src.oncology.cli genomic analyze \
    --input data/processed \
    --analysis enrichment
```

#### Harmonize Data
```bash
python -m src.oncology.cli genomic harmonize --input <dir> [--output <dir>]

# Options:
--input   Input directory
--output  Output directory (optional)

# Example:
python -m src.oncology.cli genomic harmonize --input data/raw
```

### Bioinformatics Analysis (bio)

Perform various bioinformatics analyses.

#### Pathway Analysis
```bash
python -m src.oncology.cli bio pathway --genes <file> --pathways <file>

# Options:
--genes     Gene list file
--pathways  Pathway database file

# Example:
python -m src.oncology.cli bio pathway \
    --genes data/gene_list.txt \
    --pathways data/pathway_db.json
```

#### Expression Analysis
```bash
python -m src.oncology.cli bio expression --data <file> --groups <file>

# Options:
--data    Expression data file
--groups  Sample groups file

# Example:
python -m src.oncology.cli bio expression \
    --data data/expression.csv \
    --groups data/groups.txt
```

#### Correlation Analysis
```bash
python -m src.oncology.cli bio correlation --data <file> --genes <file>

# Options:
--data   Expression data file
--genes  Gene pairs file

# Example:
python -m src.oncology.cli bio correlation \
    --data data/expression.csv \
    --genes data/gene_pairs.txt
```

### Medical Document Processing (doc)

Process and analyze medical documents.

#### Extract Information
```bash
python -m src.oncology.cli doc extract --input <file> --type <type>

# Options:
--input  Input document
--type   Document type: report, label, or publication

# Example:
python -m src.oncology.cli doc extract \
    --input reports/clinical.txt \
    --type report
```

#### Process References
```bash
python -m src.oncology.cli doc refs --input <file>

# Options:
--input  Input document

# Example:
python -m src.oncology.cli doc refs --input papers/study.pdf
```

#### Generate Report
```bash
python -m src.oncology.cli doc report --input <file> [--output <path>]

# Options:
--input   Input document
--output  Output path (optional)

# Example:
python -m src.oncology.cli doc report \
    --input data/patient_data.json \
    --output reports/summary.pdf
```

## File Formats

### Input Files

- **VCF Files**: Standard VCF format (v4.2+)
- **Expression Data**: CSV files with genes as rows and samples as columns
- **Gene Lists**: Text files with one gene per line
- **Pathway Files**: JSON format with pathway definitions
- **Sample Groups**: Tab-delimited files defining sample groupings
- **Medical Documents**: PDF, TXT, or structured formats (JSON/XML)

### Output Files

- **Harmonized Data**: CSV files with standardized formats
- **Analysis Results**: JSON files with detailed results
- **Reports**: PDF or HTML formats with visualizations
- **Statistics**: JSON files with summary statistics

## Environment Variables

The CLI respects the following environment variables:
- `ONCOLOGY_DATA_DIR`: Base directory for data files
- `ONCOLOGY_CONFIG_DIR`: Directory for configuration files
- `ONCOLOGY_OUTPUT_DIR`: Default output directory

## Error Handling

The CLI provides clear error messages with:
- Input validation errors
- File format errors
- Processing errors
- System errors

Error messages include:
- Error type and description
- Suggested resolution
- Relevant file or parameter information

## Best Practices

1. **Data Organization**
   - Keep input files in appropriate subdirectories
   - Use consistent file naming conventions
   - Maintain separate directories for raw and processed data

2. **Command Usage**
   - Use full paths for input/output files
   - Quote file paths containing spaces
   - Use the --help option for command-specific guidance

3. **Error Recovery**
   - Check input file formats before processing
   - Use the --output option to specify safe locations
   - Keep backups of important data files

## Support

For issues and feature requests:
- File an issue in the project repository
- Include command output and error messages
- Provide sample data (if possible)