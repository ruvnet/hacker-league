# Insider Trading Mirror System Makefile

.PHONY: all clean install test lint format check coverage docs run

# Python settings
PYTHON := python3
VENV := venv
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/pytest
BLACK := $(VENV)/bin/black
ISORT := $(VENV)/bin/isort
FLAKE8 := $(VENV)/bin/flake8
MYPY := $(VENV)/bin/mypy
PYLINT := $(VENV)/bin/pylint
SPHINX := $(VENV)/bin/sphinx-build

# Project settings
SRC_DIR := src/insider_mirror
TEST_DIR := tests
DOCS_DIR := docs
COVERAGE_DIR := htmlcov

# Default target
all: install test lint

# Create virtual environment
$(VENV)/bin/activate:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install -r requirements-dev.txt

# Install dependencies
install: $(VENV)/bin/activate

# Run tests
test: install
	$(PYTEST) $(TEST_DIR) -v

# Run tests with coverage
coverage: install
	$(PYTEST) $(TEST_DIR) -v --cov=$(SRC_DIR) --cov-report=html --cov-report=term-missing

# Run linting
lint: install
	$(BLACK) --check $(SRC_DIR) $(TEST_DIR)
	$(ISORT) --check-only $(SRC_DIR) $(TEST_DIR)
	$(FLAKE8) $(SRC_DIR) $(TEST_DIR)
	$(MYPY) $(SRC_DIR)
	$(PYLINT) $(SRC_DIR)

# Format code
format: install
	$(BLACK) $(SRC_DIR) $(TEST_DIR)
	$(ISORT) $(SRC_DIR) $(TEST_DIR)

# Type checking
typecheck: install
	$(MYPY) $(SRC_DIR)

# Build documentation
docs: install
	$(SPHINX) -b html $(DOCS_DIR)/source $(DOCS_DIR)/build/html

# Clean build artifacts
clean:
	rm -rf $(VENV)
	rm -rf $(COVERAGE_DIR)
	rm -rf $(DOCS_DIR)/build
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf .mypy_cache
	rm -rf **/__pycache__
	rm -rf **/*.pyc
	rm -rf **/*.pyo
	rm -rf **/*.pyd
	rm -rf .eggs
	rm -rf *.egg-info
	rm -rf dist
	rm -rf build

# Run the system
run: install
	$(PYTHON) -m insider_mirror.cli run

# Run specific commands
.PHONY: data analyze trade report

data: install
	$(PYTHON) -m insider_mirror.cli data fetch

analyze: install
	$(PYTHON) -m insider_mirror.cli analyze trades

trade: install
	$(PYTHON) -m insider_mirror.cli trade execute --mode paper

report: install
	$(PYTHON) -m insider_mirror.cli report generate --format html

# Development helpers
.PHONY: dev-setup dev-update

# Set up development environment
dev-setup: install
	$(PIP) install pre-commit
	pre-commit install

# Update dependencies
dev-update: install
	$(PIP) install --upgrade -r requirements.txt
	$(PIP) install --upgrade -r requirements-dev.txt

# Security checks
.PHONY: security

security: install
	$(VENV)/bin/bandit -r $(SRC_DIR)
	$(VENV)/bin/safety check

# Performance testing
.PHONY: benchmark

benchmark: install
	$(PYTEST) $(TEST_DIR) -v -m "slow" --durations=0

# Help target
help:
	@echo "Available targets:"
	@echo "  install     - Install project dependencies"
	@echo "  test        - Run tests"
	@echo "  coverage    - Run tests with coverage report"
	@echo "  lint        - Run all linting checks"
	@echo "  format      - Format code with black and isort"
	@echo "  typecheck   - Run type checking"
	@echo "  docs        - Build documentation"
	@echo "  clean       - Clean build artifacts"
	@echo "  run         - Run the system"
	@echo "  data        - Run data fetching"
	@echo "  analyze     - Run trade analysis"
	@echo "  trade       - Run trade execution"
	@echo "  report      - Generate reports"
	@echo "  dev-setup   - Set up development environment"
	@echo "  dev-update  - Update dependencies"
	@echo "  security    - Run security checks"
	@echo "  benchmark   - Run performance tests"