```
    _    ___   _    _            _             _                           
   / \  |_ _| | |  | | __ _  ___| | _____ _ __| |    ___  __ _  __ _  _   _  ___ 
  / _ \  | |  | |__| |/ _` |/ __| |/ / _ \ '__| |   / _ \/ _` |/ _` || | | |/ _ \
 / ___ \ | |  |  __  | (_| | (__|   <  __/ |  | |__|  __/ (_| | (_| || |_| |  __/
/_/   \_\___| |_|  |_|\__,_|\___|_|\_\___|_|  |_____\___|\__,_|\__, | \__,_|\___|
                                                                |___/            
```

*Created during AI Hacker League live coding session - Every Thursday at 12pm ET*

# Welcome to AI Hacker League! 🚀

AI Hacker League is a vibrant community of developers, researchers, and enthusiasts who come together to explore and push the boundaries of AI technology. Our weekly live coding sessions are more than just tutorials - they're collaborative experiments in cutting-edge AI development.

## What is AI Hacker League?

- **Live Coding Sessions**: Every Thursday at 12pm ET, we dive into hands-on AI development, building real systems in real-time
- **Community Learning**: Join fellow AI enthusiasts in exploring new technologies and techniques
- **Practical Experience**: Learn by doing, with real-world applications and use cases
- **Expert Guidance**: Sessions led by experienced AI developers and researchers

## Why Join AI Hacker League?

- 🔧 Get hands-on experience with cutting-edge AI tools and frameworks
- 🤝 Network with other AI developers and enthusiasts
- 💡 Learn practical implementation techniques not taught in courses
- 🚀 Stay ahead of the curve in AI development
- 🛠️ Build your portfolio with real AI projects
- 🎓 Learn best practices from experienced developers

## About This Project

This repository showcases a project created during one of our live sessions, demonstrating the power of AI agents using CrewAI, LangChain/LangGraph, and Aider. It's a perfect example of the practical, hands-on learning you'll experience in AI Hacker League.

---

# AI Agent Development Tutorial
A comprehensive guide to building and customizing AI agents using CrewAI, LangChain/LangGraph, and Aider.

## Table of Contents
1. [Introduction](#introduction)
2. [Project Overview](#project-overview)
3. [Getting Started](#getting-started)
4. [Understanding the Components](#understanding-the-components)
5. [Customization Guide](#customization-guide)
6. [Advanced Topics](#advanced-topics)

## Introduction
This repository contains a demonstration of AI agent development created during the AI Hacker League live coding session. It showcases how to build AI agents that can perform research, execute tasks, and work together as a coordinated system.

## Project Overview
The project implements a modular AI agent system with the following key features:
- ReACT (Reasoning and Acting) methodology for structured problem-solving
- Multi-agent coordination using CrewAI
- Task configuration and agent role definition
- Interactive command-line interface with cyberpunk styling

## Getting Started

### Prerequisites
```bash
# Clone the repository
git clone https://github.com/ruvnet/hacker-league-jan23
cd hacker-league-jan23

# Install dependencies
poetry install
```

### Environment Setup
1. Copy the sample environment file:
```bash
cp env.sample .env
```

2. Configure your environment variables in `.env`:
```
OPENAI_API_KEY=your_api_key_here
```

### Running the Agent
```bash
# Using the interactive menu
./start.sh

# Direct execution with custom prompt
poetry run python src/hello_world/main.py --prompt "Your prompt here" --task research
```

## Understanding the Components

### 1. Agent Configuration (src/hello_world/config/agents.yaml)
Defines agent roles and capabilities:
```yaml
research_analyst:
  name: Research Analyst
  model: deepseek
  temperature: 0.7
  description: |
    Expert in analyzing information and providing insights using ReACT methodology.
```

### 2. Task Configuration (src/hello_world/config/tasks.yaml)
Defines tasks and their requirements:
```yaml
research:
  description: Conduct research and analysis
  tools:
    - web_search
    - document_analysis
```

### 3. Main Agent Logic (src/hello_world/main.py)
Orchestrates the agent system:
```python
def run():
    args = parse_args()
    crew = HelloWorldCrew()
    result = crew.run(prompt=args.prompt, task_type=args.task)
```

### 4. Crew Management (src/hello_world/crew.py)
Handles agent coordination and task execution:
```python
class HelloWorldCrew:
    def __init__(self):
        self.crew = Crew(
            agents=[self.research_analyst],
            tasks=[self.research_task]
        )
```

## Customization Guide

### 1. Adding New Agents
To create a new agent type:

1. Add agent configuration in `agents.yaml`:
```yaml
code_expert:
  name: Code Expert
  model: gpt-4
  temperature: 0.3
  description: |
    Specialized in code analysis and generation.
```

2. Create agent implementation in `crew.py`:
```python
def create_code_expert(self):
    return Agent(
        role="Code Expert",
        goal="Generate and analyze code efficiently",
        backstory="Expert software developer with broad language expertise",
        tools=[self.code_analysis_tool]
    )
```

### 2. Adding New Tasks
To implement new task types:

1. Define task in `tasks.yaml`:
```yaml
code_review:
  description: Perform code analysis and review
  tools:
    - code_analysis
    - best_practices_check
```

2. Implement task handler in `crew.py`:
```python
def code_review_task(self):
    return Task(
        description="Analyze code for quality and improvements",
        tools=self.get_code_tools()
    )
```

### 3. Adding Custom Tools
To create new tools for agents:

1. Create tool in `tools/custom_tool.py`:
```python
class CodeAnalysisTool:
    def analyze_code(self, code: str) -> dict:
        # Implementation
        return {
            "complexity": calculate_complexity(code),
            "suggestions": generate_suggestions(code)
        }
```

2. Register tool with agents in `crew.py`:
```python
def get_code_tools(self):
    return [
        Tool(
            name="code_analysis",
            func=self.code_analysis_tool.analyze_code,
            description="Analyzes code quality and structure"
        )
    ]
```

## Advanced Topics

### 1. Implementing Custom Workflows
You can create specialized workflows by combining agents and tasks:

```python
class CustomWorkflow:
    def __init__(self):
        self.research_agent = ResearchAnalyst()
        self.code_agent = CodeExpert()
        
    def execute(self, prompt):
        research_results = self.research_agent.analyze(prompt)
        code_implementation = self.code_agent.implement(research_results)
        return code_implementation
```

### 2. Integration with External Services
Add API integrations to enhance agent capabilities:

```python
class ExternalServiceTool:
    def __init__(self, api_key):
        self.client = ExternalAPI(api_key)
    
    def fetch_data(self, query):
        return self.client.search(query)
```

### 3. Custom Output Formatting
Implement custom formatters for agent outputs:

```python
class OutputFormatter:
    def format_research(self, results):
        return f"""
╔══════════════════════════════════════════════════════════════════╗
║                    RESEARCH FINDINGS                             ║
╚══════════════════════════════════════════════════════════════════╝

{results}
"""
```

## Contributing
Feel free to contribute to this project by:
1. Forking the repository
2. Creating a feature branch
3. Submitting a pull request

## Join AI Hacker League
Join us every Thursday at 12pm ET for live coding sessions where we build and explore AI systems. Follow [@rUv](https://github.com/ruvnet) for updates and announcements.

## License
This project is open source and available under the MIT License.

Created by rUv, cause he could. 🚀
