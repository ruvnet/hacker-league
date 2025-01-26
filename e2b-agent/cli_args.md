# RUV CLI Arguments Documentation

## Command Structure

The RUV CLI follows this general command structure:
```bash
ruv <command> <subcommand> [options]
```

## Available Commands

### 1. Authentication

#### Login
```bash
ruv auth login
```
- Authenticates with E2B using API key from environment
- Required env var: `E2B_API_KEY`

#### Logout
```bash
ruv auth logout
```
- Clears stored authentication credentials

### 2. Template Management

#### Initialize Template
```bash
ruv template init
```
- Creates a new template structure
- Creates: ruv.toml, Dockerfile

#### Build Template
```bash
ruv template build
```
- Builds template from current directory
- Options:
  - `--name`: Custom template name
  - `--cpu-count`: CPU cores (default: 2)
  - `--memory-mb`: Memory in MB (default: 4096)

#### List Templates
```bash
ruv template list
```
- Shows all available templates
- Displays: ID, Name, Status

### 3. Sandbox Management

#### List Sandboxes
```bash
ruv sandbox list
```
- Lists all active sandboxes
- Shows: ID, Status, Uptime, Resources

#### Kill Sandbox
```bash
ruv sandbox kill <sandbox-id>
```
- Terminates specified sandbox
- Required: sandbox-id parameter

### 4. Agent Operations

#### Code Agent
```bash
ruv agent code [query]
```
- Generates and executes code based on query
- Examples:
  ```bash
  ruv agent code "Calculate fibonacci sequence"
  ruv agent code "Create a web server"
  ```

#### Data Agent
```bash
ruv agent data <operation> [options]
```
- Performs data operations
- Operations:
  - `load`: Load data from file
  - `describe`: Analyze data
  - `plot`: Create visualizations
- Options:
  - `--file`: Input file path
  - `--columns`: Columns to process
- Examples:
  ```bash
  ruv agent data load --file=data.csv
  ruv agent data describe --file=data.csv --columns col1 col2
  ruv agent data plot --file=data.csv --columns col1 col2
  ```

#### Employee Agent
```bash
ruv agent employee <role> [options]
```
- Manages virtual employee agents
- Options:
  - `--start`: Start the agent
  - `--stop`: Stop the agent
  - `--status`: Check agent status
- Examples:
  ```bash
  ruv agent employee data_analyst --start
  ruv agent employee data_analyst --status
  ruv agent employee data_analyst --stop
  ```

#### Communications Agent
```bash
ruv agent comms <method> [options]
```
- Handles external communications
- Methods:
  - `slack`: Send Slack messages
  - `email`: Send emails
- Options:
  - `--message`: Message content
- Examples:
  ```bash
  ruv agent comms slack --message="Hello team"
  ruv agent comms email --message="Status update"
  ```

### 5. Interactive Menu
```bash
ruv menu
```
- Launches interactive CLI menu
- Provides guided interface for all commands

## Global Options

### Output Format
```bash
--format <format>
```
- Formats: json, yaml, table
- Default: table
- Example: `ruv sandbox list --format=json`

### Verbosity
```bash
--verbose, -v
```
- Increases output verbosity
- Can be stacked: -vvv for more detail

### Help
```bash
--help, -h
```
- Shows help for command
- Example: `ruv agent code --help`

## Environment Variables

### Required
- `E2B_API_KEY`: E2B authentication key (used internally)
- `OPENROUTER_API_KEY`: OpenRouter API key for LLM access

### Optional
- `SLACK_BOT_TOKEN`: Slack integration token
- `EMAIL_SMTP_SERVER`: SMTP server for email
- `EMAIL_SMTP_USER`: SMTP username
- `EMAIL_SMTP_PASS`: SMTP password

## Exit Codes

- 0: Success
- 1: General error
- 2: Invalid arguments
- 3: Authentication error
- 4: Resource error
- 5: Network error

## Examples

### Basic Workflow
```bash
# Login
ruv auth login

# Create and build template
ruv template init
ruv template build --name="custom-env"

# Run code
ruv agent code "print('Hello, World!')"

# Cleanup
ruv sandbox kill $(ruv sandbox list --format=json | jq -r '.[0].id')
```

### Data Analysis Workflow
```bash
# Load and analyze data
ruv agent data load --file=dataset.csv
ruv agent data describe --file=dataset.csv --columns price volume
ruv agent data plot --file=dataset.csv --columns price

# Share results
ruv agent comms slack --message="Analysis complete"
```

### Long-Running Task
```bash
# Start employee agent
ruv agent employee data_analyst --start

# Check status periodically
ruv agent employee data_analyst --status

# Stop when done
ruv agent employee data_analyst --stop
```

## Best Practices

1. **Resource Management**
   - Always clean up unused sandboxes
   - Monitor resource usage
   - Use appropriate resource limits

2. **Error Handling**
   - Check exit codes
   - Use verbose mode for debugging
   - Handle cleanup in scripts

3. **Security**
   - Use environment variables for secrets
   - Regularly rotate API keys
   - Validate input data

4. **Automation**
   - Use JSON output for scripting
   - Create aliases for common commands
   - Use shell functions for complex workflows

## Common Issues

1. **Authentication Failures**
   - Check environment variables
   - Verify API key validity
   - Ensure network connectivity

2. **Resource Limits**
   - Monitor sandbox usage
   - Clean up unused resources
   - Adjust resource allocations

3. **Integration Issues**
   - Verify service credentials
   - Check network connectivity
   - Review service logs

## Support

- Documentation: https://github.com/yourusername/ruv-cli
- Issues: https://github.com/yourusername/ruv-cli/issues
- Community: Join our Discord community