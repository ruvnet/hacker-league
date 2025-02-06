# Test Execution Guide

## Test Script Structure

The following script structure should be implemented to run tests in the correct order:

```python
# test_runner.py

import pytest
import os
import sys
from typing import List, Tuple
import subprocess

class TestRunner:
    """Manages test execution order and environment setup"""
    
    def __init__(self):
        self.test_groups = [
            ("Authentication", "tests/test_auth.py"),
            ("Template Management", "tests/test_template.py"),
            ("Sandbox Operations", "tests/test_sandbox.py"),
            ("Code Agent", "tests/test_agents/test_code_agent.py"),
            ("Data Agent", "tests/test_agents/test_data_agent.py"),
            ("Employee Agent", "tests/test_agents/test_employee_agent.py"),
            ("Communications Agent", "tests/test_agents/test_comms_agent.py")
        ]

    def setup_environment(self) -> bool:
        """Setup test environment and dependencies"""
        required_vars = [
            "E2B_API_KEY",
            "OPENROUTER_API_KEY"
        ]
        
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            print(f"Missing required environment variables: {', '.join(missing_vars)}")
            return False
            
        return True

    def run_test_group(self, test_path: str) -> Tuple[int, str]:
        """Run a specific test group and return results"""
        result = pytest.main([
            test_path,
            "-v",
            "--tb=short",
            "--cov=ruv_agent",
            "--cov-report=term-missing"
        ])
        
        return result

    def run_all_tests(self) -> bool:
        """Run all test groups in order"""
        if not self.setup_environment():
            return False

        failed_groups = []
        
        for group_name, test_path in self.test_groups:
            print(f"\nRunning {group_name} tests...")
            result = self.run_test_group(test_path)
            
            if result != 0:
                failed_groups.append(group_name)

        if failed_groups:
            print(f"\nTest groups failed: {', '.join(failed_groups)}")
            return False
            
        print("\nAll test groups passed successfully!")
        return True

    def generate_coverage_report(self):
        """Generate detailed coverage report"""
        subprocess.run([
            "pytest",
            "--cov=ruv_agent",
            "--cov-report=html",
            "--cov-report=term-missing"
        ])

if __name__ == "__main__":
    runner = TestRunner()
    success = runner.run_all_tests()
    
    if success:
        runner.generate_coverage_report()
    
    sys.exit(0 if success else 1)
```

## Test Execution Order

1. **Authentication Tests**
   - Verify API key handling
   - Test login/logout flows
   - Check error handling

2. **Template Tests**
   - Test template creation
   - Verify build process
   - Check template listing

3. **Sandbox Tests**
   - Test sandbox creation
   - Verify resource management
   - Check cleanup procedures

4. **Agent Tests**
   - Code Agent tests
   - Data Agent tests
   - Employee Agent tests
   - Communications Agent tests

## Running Tests

### Basic Execution
```bash
# Run all tests in order
python test_runner.py

# Run specific test group
pytest tests/test_auth.py -v
```

### Coverage Reports
```bash
# Generate HTML coverage report
pytest --cov=ruv_agent --cov-report=html

# Show terminal coverage report
pytest --cov=ruv_agent --cov-report=term-missing
```

## Test Environment Setup

### Required Environment Variables
```bash
# Core functionality
export E2B_API_KEY=your_e2b_api_key
export OPENROUTER_API_KEY=your_openrouter_api_key

# Optional integrations
export SLACK_BOT_TOKEN=your_slack_token
export EMAIL_SMTP_SERVER=smtp.example.com
export EMAIL_SMTP_USER=your_email
export EMAIL_SMTP_PASS=your_password
```

### Virtual Environment
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install test dependencies
pip install -r requirements-dev.txt
```

## Test Data

### Sample Files
- `tests/data/sample.csv`: Sample data for data agent tests
- `tests/data/test_code.py`: Sample code for code agent tests
- `tests/data/test_config.yaml`: Sample configuration for testing

### Mock Data
- `tests/mocks/e2b_responses.py`: Mock E2B API responses
- `tests/mocks/openrouter_responses.py`: Mock OpenRouter responses
- `tests/mocks/slack_responses.py`: Mock Slack API responses

## Continuous Integration

### GitHub Actions Workflow
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements-dev.txt
      - name: Run tests
        env:
          E2B_API_KEY: ${{ secrets.E2B_API_KEY }}
          OPENROUTER_API_KEY: ${{ secrets.OPENROUTER_API_KEY }}
        run: python test_runner.py
```

## Test Maintenance

### Regular Updates
1. Update test data monthly
2. Review and update mocks
3. Check for deprecated APIs
4. Update test dependencies

### Performance Monitoring
1. Track test execution time
2. Monitor coverage metrics
3. Check for flaky tests
4. Review resource usage

## Troubleshooting

### Common Issues
1. **Missing Environment Variables**
   - Check .env file
   - Verify variable names
   - Confirm values are correct

2. **Failed API Mocks**
   - Update mock responses
   - Check API versions
   - Verify endpoint URLs

3. **Resource Issues**
   - Clean up test sandboxes
   - Reset test environment
   - Check system resources

### Debug Mode
```bash
# Run tests with debug logging
pytest -v --log-cli-level=DEBUG

# Run specific test with debug
pytest tests/test_auth.py -v --log-cli-level=DEBUG
```

## Success Criteria

1. All tests pass
2. Coverage > 90%
3. No flaky tests
4. Clean test environment
5. Clear error messages