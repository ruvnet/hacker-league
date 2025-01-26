# E2B Agent Test Plan

## Test Execution Order

The tests should be executed in the following order to ensure proper dependency handling and resource management:

1. Auth Tests
2. Template Tests
3. Sandbox Tests
4. Agent Tests (in order)

## 1. Auth Tests

### Test Cases

```python
# test_auth.py

def test_login_with_valid_key():
    """
    Given: A valid E2B API key
    When: Logging in
    Then: Should successfully authenticate
    """
    args = ["auth", "login"]
    expected_output = "Successfully logged in to E2B"

def test_login_with_invalid_key():
    """
    Given: An invalid E2B API key
    When: Logging in
    Then: Should fail with appropriate error message
    """
    args = ["auth", "login"]
    expected_error = "Invalid API key"

def test_logout():
    """
    Given: An authenticated session
    When: Logging out
    Then: Should successfully clear credentials
    """
    args = ["auth", "logout"]
    expected_output = "Successfully logged out"
```

## 2. Template Tests

### Test Cases

```python
# test_template.py

def test_init_template():
    """
    Given: Valid template configuration
    When: Initializing a new template
    Then: Should create template structure
    """
    args = ["template", "init"]
    expected_files = ["e2b.toml", "Dockerfile"]

def test_build_template():
    """
    Given: Valid template files
    When: Building template
    Then: Should successfully build and register
    """
    args = ["template", "build"]
    expected_output = "Template built successfully"

def test_list_templates():
    """
    Given: Existing templates
    When: Listing templates
    Then: Should show all available templates
    """
    args = ["template", "list"]
    expected_output_contains = ["custom_template"]
```

## 3. Sandbox Tests

### Test Cases

```python
# test_sandbox.py

def test_list_empty_sandboxes():
    """
    Given: No running sandboxes
    When: Listing sandboxes
    Then: Should show empty list
    """
    args = ["sandbox", "list"]
    expected_output = "No active sandboxes"

def test_list_active_sandboxes():
    """
    Given: Running sandbox
    When: Listing sandboxes
    Then: Should show active sandbox details
    """
    args = ["sandbox", "list"]
    expected_output_contains = ["SANDBOX_ID", "STATUS", "UPTIME"]

def test_kill_sandbox():
    """
    Given: Running sandbox ID
    When: Killing sandbox
    Then: Should terminate successfully
    """
    args = ["sandbox", "kill", "test-id"]
    expected_output = "Sandbox terminated successfully"
```

## 4. Agent Tests

### 4.1 Code Agent Tests

```python
# test_agents/test_code_agent.py

def test_code_generation():
    """
    Given: Valid code generation prompt
    When: Generating code
    Then: Should return valid Python code
    """
    args = ["agent", "code", "Calculate fibonacci sequence"]
    expected_output_contains = ["def fibonacci"]

def test_code_execution():
    """
    Given: Valid Python code
    When: Executing in sandbox
    Then: Should return execution results
    """
    args = ["agent", "code", "print('Hello, World!')"]
    expected_output = "Hello, World!"

def test_code_execution_error():
    """
    Given: Invalid Python code
    When: Executing in sandbox
    Then: Should handle error gracefully
    """
    args = ["agent", "code", "invalid syntax!!!"]
    expected_error_contains = "SyntaxError"
```

### 4.2 Data Agent Tests

```python
# test_agents/test_data_agent.py

def test_load_csv():
    """
    Given: Valid CSV file
    When: Loading data
    Then: Should successfully load
    """
    args = ["agent", "data", "load", "--file=test.csv"]
    expected_output_contains = ["Loaded data with shape"]

def test_describe_data():
    """
    Given: Loaded dataset
    When: Describing data
    Then: Should show statistics
    """
    args = ["agent", "data", "describe", "--file=test.csv"]
    expected_output_contains = ["count", "mean", "std"]

def test_plot_data():
    """
    Given: Loaded dataset
    When: Creating plot
    Then: Should generate visualization
    """
    args = ["agent", "data", "plot", "--file=test.csv"]
    expected_output = "Plot saved to output_plot.png"
```

### 4.3 Employee Agent Tests

```python
# test_agents/test_employee_agent.py

def test_start_employee():
    """
    Given: Valid employee role
    When: Starting employee
    Then: Should start successfully
    """
    args = ["agent", "employee", "data_analyst", "--start"]
    expected_output = "Employee agent started"

def test_employee_status():
    """
    Given: Running employee agent
    When: Checking status
    Then: Should show running status
    """
    args = ["agent", "employee", "data_analyst", "--status"]
    expected_output_contains = ["running"]

def test_stop_employee():
    """
    Given: Running employee agent
    When: Stopping employee
    Then: Should stop successfully
    """
    args = ["agent", "employee", "data_analyst", "--stop"]
    expected_output = "Employee agent stopped"
```

### 4.4 Comms Agent Tests

```python
# test_agents/test_comms_agent.py

def test_slack_message():
    """
    Given: Valid Slack configuration
    When: Sending message
    Then: Should deliver successfully
    """
    args = ["agent", "comms", "slack", "--message=test"]
    expected_output = "Message posted to Slack"

def test_email_message():
    """
    Given: Valid email configuration
    When: Sending email
    Then: Should send successfully
    """
    args = ["agent", "comms", "email", "--message=test"]
    expected_output = "Email sent successfully"

def test_invalid_comms_method():
    """
    Given: Invalid communication method
    When: Attempting to send
    Then: Should fail with error
    """
    args = ["agent", "comms", "invalid", "--message=test"]
    expected_error = "Unknown communication method"
```

## Test Data Requirements

1. Sample CSV file for data agent tests
2. Mock E2B sandbox responses
3. Mock OpenRouter API responses
4. Mock Slack/Email configurations

## Test Environment Setup

```python
# conftest.py

@pytest.fixture
def mock_e2b():
    """Mock E2B sandbox environment"""
    pass

@pytest.fixture
def mock_openrouter():
    """Mock OpenRouter API"""
    pass

@pytest.fixture
def mock_slack():
    """Mock Slack API"""
    pass

@pytest.fixture
def mock_smtp():
    """Mock SMTP server"""
    pass

@pytest.fixture
def sample_data():
    """Create sample CSV data"""
    pass
```

## Test Execution Commands

```bash
# Run all tests
pytest

# Run specific test category
pytest tests/test_auth.py
pytest tests/test_template.py
pytest tests/test_sandbox.py
pytest tests/test_agents/

# Run with coverage
pytest --cov=e2b_agent

# Generate coverage report
pytest --cov=e2b_agent --cov-report=html
```

## CI/CD Integration

1. Run tests on every pull request
2. Require passing tests for merge
3. Generate and store test reports
4. Track coverage metrics

## Test Maintenance

1. Update tests when adding new features
2. Maintain mock data and fixtures
3. Review and update test cases regularly
4. Monitor test execution times

## Success Criteria

1. All tests pass
2. Code coverage > 90%
3. No flaky tests
4. Clear error messages
5. Fast execution time