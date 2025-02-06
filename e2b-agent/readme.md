# RUV CLI

A powerful command-line interface that abstracts E2B's code interpreter functionality, providing a streamlined experience for managing AI agents, sandboxes, and automated workflows.

## Documentation

- [Implementation Details](implementation.md)
- [Test Plan](test_plan.md)
- [Development Roadmap](roadmap.md)
- [CLI Arguments](cli_args.md)
- [Project Summary](summary.md)

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ruv-cli
cd ruv-cli

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Setup

Create a `.env` file with your credentials:

```bash
# Required
E2B_API_KEY=your_e2b_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Optional
SLACK_BOT_TOKEN=your_slack_bot_token_here
EMAIL_SMTP_SERVER=smtp.example.com
EMAIL_SMTP_USER=your_email@example.com
EMAIL_SMTP_PASS=your_email_password_here
```

### Basic Usage

```bash
# Login
ruv auth login

# Create and build a template
ruv template init
ruv template build --name="custom-env"

# Run code
ruv agent code "print('Hello, World!')"

# Use data agent
ruv agent data load --file=data.csv
ruv agent data describe --file=data.csv --columns col1 col2

# Start an employee agent
ruv agent employee data_analyst --start
```

## Features

- **Code Generation & Execution**: Generate and run Python code in isolated sandboxes
- **Data Analysis**: Load, analyze, and visualize data with built-in tools
- **Virtual Employees**: Run long-running agent processes for specialized tasks
- **Communication**: Integrate with Slack, email, and other channels
- **Resource Management**: Efficiently manage templates and sandboxes

## Project Structure

```plaintext
ruv_cli/
├── ruv_agent/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── menu.py
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── template.py
│   │   ├── sandbox.py
│   │   ├── agent/
│   │   │   ├── __init__.py
│   │   │   ├── code_agent.py
│   │   │   ├── data_agent.py
│   │   │   ├── employee_agent.py
│   │   │   ├── comms_agent.py
│   │   │   └── base_agent.py
│   │   └── agent.py
│   └── utils/
│       └── ruv_helpers.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_agents/
├── requirements.txt
└── setup.py
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=ruv_agent

# Run specific test category
pytest tests/test_agents/
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## Security

- API keys and credentials are stored securely in environment variables
- Sandboxes are isolated with resource limits
- All communications are encrypted
- Regular security updates and patches

## Performance

- Fast command execution (<1s)
- Quick sandbox startup (<5s)
- Efficient resource usage
- Optimized for large datasets

## Support

- [GitHub Issues](https://github.com/yourusername/ruv-cli/issues)
- [Documentation](https://github.com/yourusername/ruv-cli/wiki)
- [Community Discord](https://discord.gg/your-server)

## License

MIT License - see [LICENSE](LICENSE) for details

## Acknowledgments

- Built on [E2B](https://e2b.dev) technology
- Uses [OpenRouter](https://openrouter.ai/) for LLM access
- Inspired by various CLI tools and agent frameworks
    sandbox_sub.add_parser("list", help="List active sandboxes")
    kill_parser = sandbox_sub.add_parser("kill", help="Kill a sandbox by ID")
    kill_parser.add_argument("id", help="Sandbox ID")

    # --------------------
    # Agent
    # --------------------
    agent_parser = subparsers.add_parser("agent", help="Run agentic flows")
    agent_sub = agent_parser.add_subparsers(dest="agent_cmd")

    # 1) Code-based agent
    code_parser = agent_sub.add_parser("code", help="Generate & run Python code in a sandbox")
    code_parser.add_argument("query", nargs="*", help="Prompt for code generation")

    # 2) Data science agent
    data_parser = agent_sub.add_parser("data", help="Data science tasks (analysis, plots, etc.)")
    data_parser.add_argument("operation", help="E.g., 'load', 'describe', 'plot'")
    data_parser.add_argument("--file", help="Path to local or remote data file", default="")
    data_parser.add_argument("--columns", nargs="*", help="Columns to analyze", default=[])

    # 3) Virtual employee agent
    emp_parser = agent_sub.add_parser("employee", help="Manage a persistent or specialized 'virtual employee' agent")
    emp_parser.add_argument("role", help="e.g. 'data_analyst', 'devops_engineer', 'chatbot', etc.")
    emp_parser.add_argument("--start", action="store_true", help="Start the employee agent")
    emp_parser.add_argument("--stop", action="store_true", help="Stop the employee agent")
    emp_parser.add_argument("--status", action="store_true", help="Check status")

    # 4) Communication agent
    comm_parser = agent_sub.add_parser("comms", help="Agent that handles Slack or email messages")
    comm_parser.add_argument("method", choices=["slack", "email"], help="Communication method")
    comm_parser.add_argument("--message", help="Message or content to send", default="")

    # --------------------
    # Menu (Optional)
    # --------------------
    menu_parser = subparsers.add_parser("menu", help="Start the interactive menu")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # Dispatch commands
    if args.command == "auth":
        if args.auth_cmd == "login":
            auth.login()
        elif args.auth_cmd == "logout":
            auth.logout()
        else:
            auth_parser.print_help()

    elif args.command == "template":
        if args.template_cmd == "init":
            template.init_template()
        elif args.template_cmd == "build":
            template.build_template()
        elif args.template_cmd == "list":
            template.list_templates()
        else:
            template_parser.print_help()

    elif args.command == "sandbox":
        if args.sandbox_cmd == "list":
            sandbox.list_sandboxes()
        elif args.sandbox_cmd == "kill":
            sandbox.kill_sandbox(args.id)
        else:
            sandbox_parser.print_help()

    elif args.command == "agent":
        agent.handle_agent_command(args)

    elif args.command == "menu":
        main_menu()

    else:
        parser.print_help()
```

### 3.3 Root Agent Dispatch: `agent.py`

We now have multiple specialized flows. This file **routes** the subcommands to the correct module in `commands/agent/`:

```python
# e2b_agent/commands/agent.py

from e2b_agent.commands.agent import code_agent, data_agent, employee_agent, comms_agent

def handle_agent_command(args):
    if args.agent_cmd == "code":
        query = " ".join(args.query) if args.query else ""
        code_agent.run_code(query)

    elif args.agent_cmd == "data":
        data_agent.run_data_operation(args.operation, file_path=args.file, columns=args.columns)

    elif args.agent_cmd == "employee":
        employee_agent.manage_employee_agent(
            role=args.role,
            start=args.start,
            stop=args.stop,
            status=args.status
        )

    elif args.agent_cmd == "comms":
        comms_agent.handle_communication(
            method=args.method,
            message=args.message
        )

    else:
        print("[ERROR] Unknown agent subcommand.")
```

### 3.4 Specialized Agent Modules

#### 3.4.1 `base_agent.py`

A simple base class or shared methods:

```python
# e2b_agent/commands/agent/base_agent.py

class BaseAgent:
    """
    Common methods or attributes for agentic flows.
    """
    def __init__(self, name="BaseAgent"):
        self.name = name

    def log(self, message):
        print(f"[{self.name}] {message}")

    def run(self, code):
        """
        Common code to execute code in E2B sandbox. 
        Derived classes can override or extend this.
        """
        from e2b_code_interpreter import CodeInterpreter
        with CodeInterpreter() as sandbox:
            execution = sandbox.notebook.exec_cell(code)
            return execution.text
```

#### 3.4.2 `code_agent.py`

A **general “code generation and execution”** agent:

```python
# e2b_agent/commands/agent/code_agent.py

import os
from openrouter import OpenRouter
from .base_agent import BaseAgent

def run_code(user_query: str):
    if not user_query:
        print("[ERROR] No query provided for code agent.")
        return

    # Generate code from LLM
    code = _generate_code(user_query)

    # Execute in E2B sandbox
    agent = BaseAgent(name="CodeAgent")
    result = agent.run(code)
    agent.log(f"Execution Result:\n{result}")


def _generate_code(prompt: str) -> str:
    """
    Use an LLM (via OpenRouter) to generate Python code from a textual prompt.
    """
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    if not openrouter_key:
        raise RuntimeError("OPENROUTER_API_KEY not set.")

    client = OpenRouter(api_key=openrouter_key)
    system_prompt = "You are a Python code interpreter. Generate concise, runnable code."

    response = client.chat.completions.create(
        model="deepseek/deepseek-coder-1.3b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    code_snippet = response.choices[0].message.content
    return code_snippet
```

#### 3.4.3 `data_agent.py`

A **data science**-oriented agent. Here we show how you might parse an operation (e.g., “load CSV, describe it, plot columns, etc.”). This is only an example skeleton; you can expand with your own logic.

```python
# e2b_agent/commands/agent/data_agent.py

import os
import pandas as pd
from .base_agent import BaseAgent

def run_data_operation(operation: str, file_path: str = "", columns=None):
    if not operation:
        print("[ERROR] Must specify a data operation.")
        return

    agent = DataAgent(name="DataAgent")
    agent.log(f"Operation requested: {operation}, file: {file_path}, columns: {columns}")

    if operation == "load":
        agent.load_data(file_path)
    elif operation == "describe":
        agent.describe_data(file_path, columns)
    elif operation == "plot":
        agent.plot_data(file_path, columns)
    else:
        agent.log("Unknown operation. Supported: load, describe, plot")


class DataAgent(BaseAgent):
    def load_data(self, file_path: str):
        if not file_path:
            self.log("[ERROR] Missing file path.")
            return
        df = pd.read_csv(file_path)
        self.log(f"Loaded data with shape: {df.shape}")

    def describe_data(self, file_path: str, columns=None):
        if not file_path:
            self.log("[ERROR] Missing file path.")
            return
        df = pd.read_csv(file_path)
        if columns:
            df = df[columns]
        self.log(str(df.describe()))

    def plot_data(self, file_path: str, columns=None):
        import matplotlib.pyplot as plt
        import seaborn as sns

        if not file_path:
            self.log("[ERROR] Missing file path.")
            return

        df = pd.read_csv(file_path)
        if columns:
            df = df[columns]

        # Example: pairplot for quick visualization
        sns.pairplot(df)
        plt.savefig("output_plot.png")
        self.log("Plot saved to output_plot.png")
```

#### 3.4.4 `employee_agent.py`

A **“virtual employee”** agent that can be started, stopped, or monitored. This skeleton uses `apscheduler` for scheduling or continuous tasks. In practice, you might store state in a database or run in the background:

```python
# e2b_agent/commands/agent/employee_agent.py

import threading
import time
from apscheduler.schedulers.background import BackgroundScheduler
from .base_agent import BaseAgent

# Simple global store for running agents
AGENT_THREADS = {}
SCHEDULERS = {}

def manage_employee_agent(role: str, start: bool, stop: bool, status: bool):
    """
    - role: e.g. "data_analyst", "devops_engineer"
    - start: start this role if not running
    - stop: stop if running
    - status: print running status
    """
    if not role:
        print("[ERROR] No role specified for employee agent.")
        return

    agent_id = f"employee_{role}"

    if start:
        _start_employee_agent(agent_id, role)
    elif stop:
        _stop_employee_agent(agent_id)
    elif status:
        _status_employee_agent(agent_id)
    else:
        print("[INFO] Use --start/--stop/--status with the role for 'employee' subcommand.")


def _start_employee_agent(agent_id, role):
    if agent_id in AGENT_THREADS:
        print(f"[INFO] Employee agent '{agent_id}' already running.")
        return

    agent = EmployeeAgent(name=agent_id, role=role)
    t = threading.Thread(target=agent.run_loop, daemon=True)
    t.start()
    AGENT_THREADS[agent_id] = t

    # Example: schedule some recurring task using APScheduler
    sched = BackgroundScheduler()
    sched.add_job(agent.periodic_check, 'interval', seconds=30)
    sched.start()
    SCHEDULERS[agent_id] = sched

    print(f"[INFO] Employee agent '{agent_id}' started.")


def _stop_employee_agent(agent_id):
    if agent_id not in AGENT_THREADS:
        print(f"[INFO] Employee agent '{agent_id}' not running.")
        return

    # Stopping logic
    thread = AGENT_THREADS.pop(agent_id)
    if agent_id in SCHEDULERS:
        SCHEDULERS[agent_id].shutdown(wait=False)
        SCHEDULERS.pop(agent_id)

    print(f"[INFO] Employee agent '{agent_id}' stopped (thread can't be forcibly killed in Python).")


def _status_employee_agent(agent_id):
    running = agent_id in AGENT_THREADS
    print(f"[INFO] Employee agent '{agent_id}' is {'running' if running else 'not running'}.")


class EmployeeAgent(BaseAgent):
    def __init__(self, name, role):
        super().__init__(name=name)
        self.role = role
        self.active = True

    def run_loop(self):
        """
        The main loop for the “virtual employee.” In reality,
        you'd handle messages, tasks, or data from a queue or DB.
        """
        self.log(f"Starting virtual employee role: {self.role}")
        while self.active:
            # Example: do some "work"
            time.sleep(5)
            self.log("Working on tasks ...")

    def periodic_check(self):
        """
        Called by APScheduler every 30s. Good for housekeeping tasks.
        """
        self.log("Periodic check: heartbeat okay?")
```

#### 3.4.5 `comms_agent.py`

A **communication** agent bridging Slack or Email. You can expand to handle more channels:

```python
# e2b_agent/commands/agent/comms_agent.py

import os
import requests
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from .base_agent import BaseAgent

def handle_communication(method: str, message: str):
    agent = CommunicationAgent(name="CommsAgent")

    if method == "slack":
        agent.send_slack_message(message)
    elif method == "email":
        agent.send_email(message)
    else:
        agent.log("[ERROR] Unknown communication method.")


class CommunicationAgent(BaseAgent):
    def send_slack_message(self, message: str):
        slack_token = os.getenv("SLACK_BOT_TOKEN")
        if not slack_token:
            self.log("[ERROR] SLACK_BOT_TOKEN not set.")
            return
        client = WebClient(token=slack_token)
        try:
            response = client.chat_postMessage(
                channel="#general",
                text=message
            )
            self.log(f"Message posted to Slack: {response['ts']}")
        except SlackApiError as e:
            self.log(f"[ERROR] Slack error: {e.response['error']}")

    def send_email(self, message: str):
        smtp_server = os.getenv("EMAIL_SMTP_SERVER")
        smtp_user = os.getenv("EMAIL_SMTP_USER")
        smtp_pass = os.getenv("EMAIL_SMTP_PASS")
        if not all([smtp_server, smtp_user, smtp_pass]):
            self.log("[ERROR] Email SMTP configuration missing.")
            return

        # Minimal example using Python's smtplib
        import smtplib
        from email.mime.text import MIMEText

        msg = MIMEText(message)
        msg["Subject"] = "Message from CommsAgent"
        msg["From"] = smtp_user
        msg["To"] = "recipient@example.com"

        with smtplib.SMTP(smtp_server, 587) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, ["recipient@example.com"], msg.as_string())
        self.log("Email sent successfully!")
```

---

## 4. Updated Optional Text Menu

You can **extend `main_menu()`** to present new agentic flows. E.g.:

```python
# e2b_agent/menu.py

from e2b_agent.commands import auth, sandbox, template, agent

def main_menu():
    while True:
        print("\n--- E2B Agent Menu ---")
        print("[1] Auth -> Login")
        print("[2] Auth -> Logout")
        print("[3] Template -> Init")
        print("[4] Template -> Build")
        print("[5] Template -> List")
        print("[6] Sandbox -> List")
        print("[7] Sandbox -> Kill")
        print("[8] Agent -> Code Generation")
        print("[9] Agent -> Data Science")
        print("[10] Agent -> Virtual Employee")
        print("[11] Agent -> Communications")
        print("[12] Quit")

        choice = input("Select an option: ").strip()
        if choice == "1":
            auth.login()
        elif choice == "2":
            auth.logout()
        elif choice == "3":
            template.init_template()
        elif choice == "4":
            template.build_template()
        elif choice == "5":
            template.list_templates()
        elif choice == "6":
            sandbox.list_sandboxes()
        elif choice == "7":
            sandbox_id = input("Enter Sandbox ID: ").strip()
            sandbox.kill_sandbox(sandbox_id)
        elif choice == "8":
            query_text = input("Enter code generation prompt: ").strip()
            args = type("Args", (), {"agent_cmd": "code", "query": [query_text]})
            agent.handle_agent_command(args)
        elif choice == "9":
            operation = input("Enter data operation (load/describe/plot): ").strip()
            file_path = input("Enter file path: ").strip()
            columns = input("Enter columns (space-separated), or leave blank: ").split()
            args = type("Args", (), {
                "agent_cmd": "data",
                "operation": operation,
                "file": file_path,
                "columns": columns
            })
            agent.handle_agent_command(args)
        elif choice == "10":
            role = input("Enter employee role: ").strip()
            start = input("Start employee? (y/n): ").lower() == "y"
            stop = input("Stop employee? (y/n): ").lower() == "y"
            status = input("Check status? (y/n): ").lower() == "y"
            args = type("Args", (), {
                "agent_cmd": "employee",
                "role": role,
                "start": start,
                "stop": stop,
                "status": status
            })
            agent.handle_agent_command(args)
        elif choice == "11":
            method = input("Enter communication method (slack/email): ").strip()
            message = input("Enter message: ").strip()
            args = type("Args", (), {"agent_cmd": "comms", "method": method, "message": message})
            agent.handle_agent_command(args)
        elif choice == "12":
            print("[INFO] Exiting menu.")
            break
        else:
            print("[ERROR] Invalid selection. Try again.")
```

---

## 5. Installation & Usage

1. **Clone** or place into your project directory.
2. **Set up** Python 3.12 environment:

   ```bash
   python3.12 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure** environment variables:

   ```bash
   export E2B_API_KEY="..."
   export OPENROUTER_API_KEY="..."
   export SLACK_BOT_TOKEN="..."
   ...
   ```

4. **Run** the CLI:

   ```bash
   python -m e2b_agent
   ```

### Example Commands

- **Authenticate**:
  ```bash
  python -m e2b_agent auth login
  python -m e2b_agent auth logout
  ```

- **Templates**:
  ```bash
  python -m e2b_agent template init
  python -m e2b_agent template build
  python -m e2b_agent template list
  ```

- **Sandboxes**:
  ```bash
  python -m e2b_agent sandbox list
  python -m e2b_agent sandbox kill <id>
  ```

- **Agents**:
  1. **Code** Generation & Execution:
     ```bash
     python -m e2b_agent agent code "Compute Fibonacci(10) in Python"
     ```
  2. **Data**:
     ```bash
     python -m e2b_agent agent data load --file="data.csv"
     python -m e2b_agent agent data describe --file="data.csv" --columns col1 col2
     python -m e2b_agent agent data plot --file="data.csv" --columns col1 col2
     ```
  3. **Virtual Employee**:
     ```bash
     python -m e2b_agent agent employee data_analyst --start
     python -m e2b_agent agent employee data_analyst --status
     python -m e2b_agent agent employee data_analyst --stop
     ```
  4. **Communications**:
     ```bash
     python -m e2b_agent agent comms slack --message="Hello Slack!"
     python -m e2b_agent agent comms email --message="Automated email body"
     ```

- **Interactive Menu**:
  ```bash
  python -m e2b_agent menu
  ```

---

## 6. Reference Documentation

1. **E2B Official Docs**  
   - [https://e2b.dev/docs](https://e2b.dev/docs)  
   - [https://e2b.dev/docs/cli](https://e2b.dev/docs/cli)
   - [https://github.com/e2b-dev/code-interpreter/](https://github.com/e2b-dev/code-interpreter/)

2. **OpenRouter**  
   - [https://github.com/openrouter/openrouter-py](https://github.com/openrouter/openrouter-py)

3. **Slack SDK**  
   - [https://slack.dev/python-slack-sdk/](https://slack.dev/python-slack-sdk/)

4. **apscheduler** for “virtual employee” scheduling  
   - [https://apscheduler.readthedocs.io/](https://apscheduler.readthedocs.io/)

5. **Data Science** references (pandas, matplotlib, seaborn)  
   - [https://pandas.pydata.org/](https://pandas.pydata.org/)  
   - [https://matplotlib.org/](https://matplotlib.org/)  
   - [https://seaborn.pydata.org/](https://seaborn.pydata.org/)

---

## 7. Security & Best Practices

1. **Sensitive Keys**:  
   - Store environment variables in `.env` or a secrets manager, not in code.

2. **Resource Limits**:  
   - When instantiating `CodeInterpreter(template="custom", cpu_count=2, memory_mb=4096, ...)`, ensure resource constraints.

3. **Virtual Employee Agents**:  
   - Typically run them in a controlled environment or container. Add robust error handling or logging to track their status.

4. **Communication**:
   - For Slack, limit channels or user access tokens.  
   - For email, do not store SMTP credentials in plain text.

5. **Data**:
   - Sanitizing data input or columns if user-submitted.  
   - Carefully handle large files (pandas can use a lot of memory).

---

## 8. Conclusion & “PhD-level” Considerations

This expanded specification demonstrates how to:

1. **Manage** E2B code execution for general coding tasks and data science.  
2. **Simulate** “virtual employee” roles that run in the background, performing periodic tasks or reacting to events.  
3. **Integrate** with external communication channels, e.g., Slack or email.  
4. **Extend** the CLI with new subcommands and unify them behind a single interface.

For **PhD-level thoroughness**:

- You could incorporate **neuro-symbolic** reasoning, storing agent states in knowledge graphs or symbolic rule sets.  
- Use **abstract algebra** or advanced math for non-trivial transformations (e.g., group theory for transformation invariants in data).  
- Add concurrency or distributed systems patterns (e.g., using message queues like RabbitMQ for tasks).  
- Implement advanced security checks, role-based access control, or auditing for each command.  
- Include a thorough test suite (Pytest) with **integration tests** that spin up ephemeral E2B sandboxes to verify end-to-end behavior.

With this structure, your E2B-based CLI can handle **multiple AI/agentic flows** within the same management tool—powerful for real-world enterprise or research contexts.  

**End of extended specification**.

## References
## Base Structure

```dockerfile
FROM e2bdev/code-interpreter:latest

# System packages
RUN apt-get update && apt-get install -y \
    package1 \
    package2

# Python packages
RUN pip install package1 package2

# Node.js packages
RUN npm install package1 package2[1]
```

## Storage Integration Components

### GCS Configuration
```dockerfile
FROM ubuntu:latest
RUN apt-get update && apt-get install -y gnupg lsb-release wget
RUN lsb_release -c -s > /tmp/lsb_release
RUN GCSFUSE_REPO=$(cat /tmp/lsb_release); \
    echo "deb https://packages.cloud.google.com/apt gcsfuse-$GCSFUSE_REPO main" | \
    tee /etc/apt/sources.list.d/gcsfuse.list
RUN wget -O - https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
RUN apt-get update && apt-get install -y gcsfuse[1]
```

### S3 Configuration
```dockerfile
FROM ubuntu:latest
RUN apt-get update && apt-get install s3fs[1]
```

## Environment Configuration

**Template Configuration File (e2b.toml)**
```toml
template_id = "your_template_id"
dockerfile = "e2b.Dockerfile"
template_name = "custom_name"
start_cmd = "your_start_command"[8]
```

## Build Parameters

- **CPU Configuration**: `--cpu-count=<value>`
- **Memory Configuration**: `--memory-mb=<value>`
- **Start Command**: `-c "<command>"` [3]

## Filesystem Structure

- Root directory: `/`
- Home directory: `/home/user`
- Jupyter startup: `/root/.jupyter/start-up.sh`[2]

## Best Practices

### Package Installation
```dockerfile
# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Python packages with version pinning
RUN pip install \
    pandas==2.0.0 \
    numpy==1.24.0

# Node.js packages with version pinning
RUN npm install -g \
    typescript@4.9.5 \
    ts-node@10.9.1[2][4]
```

### Process Management
```dockerfile
# Add startup scripts
COPY startup.sh /root/
RUN chmod +x /root/startup.sh

# Set environment variables
ENV PYTHONPATH=/usr/local/lib/python3.8/site-packages
ENV NODE_PATH=/usr/local/lib/node_modules[2]
```

## Security Considerations

- Use specific package versions
- Minimize image layers
- Remove unnecessary build dependencies
- Set appropriate file permissions
- Clean up package manager caches[1][2]

## Build Configuration

### Dockerignore
```plaintext
.git
.env
node_modules
__pycache__
*.pyc
*.pyo
*.pyd[7]
```

### Build Command Structure
```bash
e2b template build \
    -c "/root/.jupyter/start-up.sh" \
    --name "custom-sandbox" \
    --cpu-count=2 \
    --memory-mb=4096[3][4]
```

Citations:
[1] https://e2b.dev/docs/legacy/guide/connect-bucket
[2] https://e2b.dev/docs/sandbox-template
[3] https://e2b.dev/docs/legacy/guide/custom-sandbox
[4] https://e2b.dev/docs/quickstart/install-custom-packages
[5] https://www.npmjs.com/package/@e2b/cli/v/0.4.4
[6] https://e2b.dev/docs/legacy/sandbox/templates/overview
[7] https://github.com/e2b-dev/E2B/issues/255
[8] https://e2b.dev/docs/legacy/sandbox/templates/start-cmd
[9] https://www.restack.io/p/ai-generated-code-answer-ai-tools-comparison-cat-ai

## Core SDK Features

### Sandbox Management
```python
from e2b_code_interpreter import CodeInterpreter

sandbox = CodeInterpreter(
    template="custom_template",
    cpu_count=2,
    memory_mb=4096,
    timeout=300,
    env_vars={"API_KEY": "secret"}
)[1]
```

### Code Execution
```python
# Basic execution
sandbox.notebook.exec_cell("x = 1")

# Multi-line execution with context
sandbox.notebook.exec_cell("""
def process_data(x):
    return x * 2
result = process_data(10)
print(result)
""")[1][4]
```

## File System Operations

### File Management
```python
# Write files
sandbox.filesystem.write('/data.csv', 'content')

# Read files
content = sandbox.filesystem.read('/data.csv')

# Upload local files
with open('local.txt', 'rb') as f:
    sandbox.filesystem.write('/remote.txt', f.read())[1][4]
```

## Process Management

### Command Execution
```python
# Synchronous execution
result = sandbox.commands.run('ls -la')

# Async execution with streaming
def on_stdout(data): print(f"Output: {data}")
def on_stderr(data): print(f"Error: {data}")

sandbox.commands.run('python script.py',
    on_stdout=on_stdout,
    on_stderr=on_stderr
)[1]
```

## Package Management

### Dependency Installation
```python
# System packages
sandbox.commands.run('apt-get install -y ffmpeg')

# Python packages
sandbox.commands.run('pip install pandas numpy')

# Node.js packages
sandbox.commands.run('npm install express')[2]
```

## Data Analysis Capabilities

### Visualization
```python
sandbox.notebook.exec_cell("""
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
plt.plot(x, np.sin(x))
plt.show()
""")[4]
```

## Network Features

### Web Access
```python
sandbox.notebook.exec_cell("""
import requests
response = requests.get('https://api.example.com')
print(response.json())
""")[2]
```

## Git Integration
```python
# Clone repository
sandbox.commands.run('git clone https://github.com/user/repo.git')

# Git operations
sandbox.commands.run('''
cd repo
git checkout -b feature
git add .
git commit -m "Update"
''')[2]
```

## Resource Management

### Cleanup
```python
# Automatic cleanup
with CodeInterpreter() as sandbox:
    sandbox.notebook.exec_cell("print('Working...')")

# Manual cleanup
sandbox = CodeInterpreter()
try:
    sandbox.notebook.exec_cell("code")
finally:
    sandbox.close()[1]
```

## Security Features

- Isolated VM environments
- Resource usage limits
- Network isolation
- File system isolation
- Process isolation[1][5]

## Advanced Features

### Custom Templates
```dockerfile
FROM e2bdev/code-interpreter:latest
RUN apt update && apt install -y ffmpeg
RUN pip install pandas numpy matplotlib[1]
```

### Environment Configuration
```python
sandbox = CodeInterpreter(
    env_vars={
        "DATABASE_URL": "postgresql://user:pass@host/db",
        "API_KEY": "secret",
        "DEBUG": "true"
    }
)[2]
```

Citations:
[1] https://e2b.dev/docs
[2] https://www.npmjs.com/package/@e2b/sdk/v/0.7.1
[3] https://www.abdulazizahwan.com/2024/08/e2b-code-interpreting-for-ai-apps-a-comprehensive-guide.html
[4] https://e2b.dev/docs/code-interpreting/analyze-data-with-ai
[5] https://github.com/e2b-dev/e2b
[6] https://www.npmjs.com/package/@e2b/sdk
[7] https://e2b.dev/docs/sdk-reference
[8] https://e2b.dev
[9] https://pypi.org/project/e2b/
[10] https://console.groq.com/docs/e2b
[11] https://github.com/e2b-dev/fragments
[12] https://e2b.dev/docs/quickstart/connect-llms
[13] https://github.com/e2b-dev/code-interpreter/
[14] https://www.youtube.com/watch?v=I6G5g5FHTdU