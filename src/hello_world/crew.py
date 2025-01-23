from crewai import Agent, Crew, Process, Task
from hello_world.tools.custom_tool import CustomTool
import yaml
from dotenv import load_dotenv
import os
import httpx
import json
import asyncio

load_dotenv()  # Load environment variables from .env file

async def stream_openrouter_response(messages, model):
    """Stream responses directly from OpenRouter"""
    async with httpx.AsyncClient() as client:
        async with client.stream(
            "POST",
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:3000",
                "X-Title": "CrewAI Console"
            },
            json={
                "model": model,
                "messages": messages,
                "stream": True,
                "temperature": 0.7
            },
            timeout=None
        ) as response:
            async for chunk in response.aiter_bytes():
                if chunk:
                    try:
                        chunk_str = chunk.decode()
                        if chunk_str.startswith('data: '):
                            chunk_data = json.loads(chunk_str[6:])
                            if chunk_data != '[DONE]':
                                if 'choices' in chunk_data and len(chunk_data['choices']) > 0:
                                    delta = chunk_data['choices'][0].get('delta', {})
                                    if 'content' in delta:
                                        content = delta['content']
                                        print(content, end='', flush=True)
                    except (json.JSONDecodeError, UnicodeDecodeError):
                        continue

class HelloWorldCrew:
    def __init__(self):
        with open('src/hello_world/config/agents.yaml', 'r') as f:
            self.agents_config = yaml.safe_load(f)
        with open('src/hello_world/config/tasks.yaml', 'r') as f:
            self.tasks_config = yaml.safe_load(f)
            
    async def run_with_streaming(self):
        """Run crew with streaming responses"""
        # Create tools
        tools = [CustomTool()]
        
        # Initial messages for researcher
        researcher_messages = [{
            "role": "system",
            "content": f"You are a {self.agents_config['researcher']['role']} with the goal: {self.agents_config['researcher']['goal']}. Use ReACT (Reasoning and Acting) methodology to break down complex tasks into actionable steps."
        }, {
            "role": "user",
            "content": self.tasks_config['research_task']['description']
        }]
        
        print("""
╔══════════════════════════════════════════════════════════════════╗
║  🤖 INITIALIZING RESEARCH ANALYST v2.0 - DEEPSEEK CORE LOADED   ║
╚══════════════════════════════════════════════════════════════════╝
        
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
🔄 ACTIVATING ReACT PROTOCOL...
📡 NEURAL INTERFACE ONLINE
🧠 COGNITIVE SYSTEMS ENGAGED
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

[SYS]: Initiating ReACT Methodology Analysis...
""")
        await stream_openrouter_response(researcher_messages, self.agents_config['researcher']['llm'])
        
        # Initial messages for executor
        executor_messages = [{
            "role": "system",
            "content": f"You are a {self.agents_config['executor']['role']} with the goal: {self.agents_config['executor']['goal']}. Focus on implementing the action plan efficiently."
        }, {
            "role": "user",
            "content": self.tasks_config['execution_task']['description']
        }]
        
        print("""

╔══════════════════════════════════════════════════════════════════╗
║  ⚡ ACTIVATING TASK EXECUTOR v1.5 - PHI CORE INITIALIZED        ║
╚══════════════════════════════════════════════════════════════════╝

▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
🎯 EXECUTION PROTOCOLS LOADED
⚙️ SYSTEM OPTIMIZATION: ENABLED
🔧 TOOL INTERFACE: ACTIVE
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

[SYS]: Beginning Implementation Sequence...
""")
        await stream_openrouter_response(executor_messages, self.agents_config['executor']['llm'])
        
    def run(self):
        """Run crew synchronously"""
        try:
            return asyncio.run(self.run_with_streaming())
        except KeyboardInterrupt:
            print("""
╔══════════════════════════════════════════════════════════════════╗
║  🛑 EMERGENCY SHUTDOWN SEQUENCE INITIATED                        ║
╚══════════════════════════════════════════════════════════════════╝
⚠️ Saving neural state...
💾 Preserving memory banks...
🔌 Powering down cores...
""")
            return None
        except Exception as e:
            print(f"""
╔══════════════════════════════════════════════════════════════════╗
║  ⚠️ SYSTEM MALFUNCTION DETECTED                                 ║
╚══════════════════════════════════════════════════════════════════╝
🔍 Error Analysis:
{str(e)}
🔧 Initiating recovery protocols...
""")
            return None
