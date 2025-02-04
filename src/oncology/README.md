# Oncology System

A medical analysis system that uses Large Language Models (LLMs) and specialized tools for processing medical images, reports, and genomic data.

## Features

- Medical image analysis using state-of-the-art computer vision models
- Clinical report processing with advanced NLP
- Genomic data interpretation and variant analysis
- Knowledge base integration for evidence-based insights
- Multi-modal analysis combining various data sources
- Caching system for efficient processing
- Configurable model and task settings

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/oncology.git
cd oncology

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## Usage

Basic usage example:

```python
from oncology import OncologySystem

# Create system instance
system = OncologySystem()

# Analyze a case
result = system.analyze_case({
    'image_path': 'path/to/image.jpg',
    'report_text': 'Clinical report text...',
    'genomic_data': {
        'variants': ['BRCA1:c.181T>G']
    }
})

print(result)
```

## Configuration

The system can be configured through YAML files in the `config` directory:

- `models.yaml`: Configure LLM models and their roles
- `tasks.yaml`: Define analysis tasks and their requirements

## Development

### Running Tests

```bash
# Run all tests
./test.sh

# Skip slow tests
./test.sh --skip-slow

# Skip integration tests
./test.sh --skip-integration

# Custom report directory
./test.sh --report-dir /path/to/reports
```

### Code Style

This project uses:
- Black for code formatting
- isort for import sorting
- flake8 for linting
- mypy for type checking

```bash
# Install development dependencies
pip install -e ".[dev]"

# Format code
black .
isort .

# Run linting
flake8 .

# Run type checking
mypy .
```

## Documentation

```bash
# Install documentation dependencies
pip install -e ".[docs]"

# Build documentation
cd docs
make html
```

Documentation will be available in `docs/_build/html`.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Requirements

- Python 3.8+
- Dependencies listed in requirements.txt
- CUDA-capable GPU recommended for image analysis

## Project Structure

```
oncology/
├── config/             # Configuration files
├── docs/              # Documentation
├── tests/             # Test suite
├── tools/             # Analysis tools
│   ├── image_analyzer.py
│   ├── text_analyzer.py
│   └── knowledge_base.py
├── main.py            # Main entry point
├── crew.py           # Crew system implementation
├── cache.py          # Caching system
└── requirements.txt   # Dependencies
```

## Acknowledgments

- OpenRouter for LLM access
- Medical imaging libraries and models
- NLP and genomics tools