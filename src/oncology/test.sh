#!/bin/bash
# Test runner script for oncology system

# Set environment variables
export PYTHONPATH="$(pwd)/..:$PYTHONPATH"  # Add parent directory to Python path
export OPENROUTER_API_KEY=${OPENROUTER_API_KEY:-"test_key"}
export TEST_MODE="true"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color
INFO="🔵"
SUCCESS="✅"
ERROR="❌"
WARNING="⚠️"

# Print header
echo -e "\n${YELLOW}======================================="
echo "Oncology System Test Runner"
echo -e "=======================================\n${NC}"

# Parse arguments
SKIP_SLOW=0
SKIP_INTEGRATION=0
CUSTOM_REPORT_DIR=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-slow)
            SKIP_SLOW=1
            shift
            ;;
        --skip-integration)
            SKIP_INTEGRATION=1
            shift
            ;;
        --report-dir)
            CUSTOM_REPORT_DIR="$2"
            shift
            shift
            ;;
        *)
            echo -e "${RED}${ERROR} Unknown argument: $1${NC}"
            exit 1
            ;;
    esac
done

# Check Python environment
echo -e "${INFO} Checking Python environment..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}${ERROR} Python 3 is not installed${NC}"
    exit 1
fi

# Create necessary directories
mkdir -p tests/sample_data
mkdir -p reports/coverage
mkdir -p reports/junit
mkdir -p reports/logs

# Prepare test command
TEST_CMD="python3 -m pytest"
if [ $SKIP_SLOW -eq 1 ]; then
    TEST_CMD="$TEST_CMD -m 'not slow'"
fi
if [ $SKIP_INTEGRATION -eq 1 ]; then
    TEST_CMD="$TEST_CMD -m 'not integration'"
fi
if [ ! -z "$CUSTOM_REPORT_DIR" ]; then
    TEST_CMD="$TEST_CMD --report-dir $CUSTOM_REPORT_DIR"
fi

# Add coverage and output formatting
TEST_CMD="$TEST_CMD --cov=. --cov-report=html:reports/coverage --cov-report=term-missing --junitxml=reports/junit/junit.xml -v"

# Run tests
echo -e "\n${INFO} Running tests..."
if eval $TEST_CMD; then
    echo -e "\n${GREEN}${SUCCESS} All tests passed!${NC}"
    exit 0
else
    echo -e "\n${RED}${ERROR} Some tests failed${NC}"
    exit 1
fi