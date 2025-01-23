# CrewAI Multi-Model Demo

This project demonstrates how to use multiple AI models through OpenRouter in a CrewAI application.

## Features

- Multi-model usage (DeepSeek R-1 and GPT-3.5)
- Sequential process flow
- Basic tool integration
- YAML-based configuration

## Setup

1. Install dependencies:
```bash
pip install crewai
pip install 'crewai[tools]'
```

2. Set up environment variables in `.env`:
```
OPENAI_API_KEY=<your-openrouter-api-key>
OPENAI_API_BASE=https://openrouter.ai/api/v1
SERPER_API_KEY=<your-serper-api-key>
```

## Running the Project

Execute the project using:
```bash
cd hello_world
python -m src.hello_world.main
```

## Project Structure

The project uses two agents:
- Researcher (DeepSeek R-1): Handles complex reasoning and research tasks
- Executor (GPT-3.5): Implements findings and executes tasks

Tools included:
- SerperDevTool: For web searches
- WebsiteSearchTool: For website content analysis