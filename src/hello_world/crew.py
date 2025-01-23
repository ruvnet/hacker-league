from crewai import Agent, Crew, Process, Task
from hello_world.tools.custom_tool import CustomTool
import yaml
from dotenv import load_dotenv
import os
import httpx
import json
import asyncio

load_dotenv()  # Load environment variables from .env file

async def stream_openrouter_response(messages, model, progress_callback=None):
    """Stream responses directly from OpenRouter with progress tracking"""
    async with httpx.AsyncClient() as client:
        async with client.stream(
            "POST",
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:3000",
                "X-Title": "rUv Console"
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
        # Load prompt configurations
        try:
            with open('src/hello_world/config/prompts.yaml', 'r') as f:
                self.prompts_config = yaml.safe_load(f)
        except FileNotFoundError:
            # Maintain backward compatibility
            self.prompts_config = {
                'templates': {
                    'user_prompts': {},
                    'validation_rules': {},
                    'progress_tracking': {}
                }
            }

        # Initialize validation rules
        self.validation_rules = self.prompts_config.get('templates', {}).get('validation_rules', {})

                                        print(content, end='', flush=True)
                    except (json.JSONDecodeError, UnicodeDecodeError):
                        continue

class HelloWorldCrew:
    def __init__(self):
        with open('src/hello_world/config/agents.yaml', 'r') as f:
            self.agents_config = yaml.safe_load(f)
        with open('src/hello_world/config/tasks.yaml', 'r') as f:
            self.tasks_config = yaml.safe_load(f)
        self.validation_status = {"reasoning": [], "actions": []}
        self.progress_tracker = {"current_step": 0, "total_steps": 0, "status": ""}

    def validate_reasoning(self, reasoning_step):
        """Validate each reasoning step in the ReACT process"""
        validation_result = {
            "step": reasoning_step,
            "valid": True,
            "feedback": []
        }
        
        # Validate logic and completeness
        if not reasoning_step.get("thought"):
            validation_result["valid"] = False
            validation_result["feedback"].append("Missing thought process")
        
        self.validation_status["reasoning"].append(validation_result)
        return validation_result

    def validate_action(self, action_step):
        """Validate each action before execution"""
        validation_result = {
            "step": action_step,
            "valid": True,
            "feedback": []
        }
        
        # Validate action structure and prerequisites
        if not action_step.get("action"):
            validation_result["valid"] = False
            validation_result["feedback"].append("Missing action definition")
            
        self.validation_status["actions"].append(validation_result)
        return validation_result

    def track_progress(self, step_type, status):
        """Track progress of ReACT methodology execution"""
        self.progress_tracker["current_step"] += 1
        self.progress_tracker["status"] = status
        
        progress = f"""
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
📊 Progress Update:
➤ Step {self.progress_tracker["current_step"]}: {step_type}
➤ Status: {status}
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
"""
        print(progress)
            
    async def run_with_streaming(self):
        """Run crew with streaming responses using enhanced ReACT methodology"""
        # Create tools
        tools = [CustomTool()]
        
        self.progress_tracker["total_steps"] = 4  # Research + Validation + Execution + Final Validation
        
        # Enhanced ReACT structure for researcher
        researcher_messages = [{
            "role": "system",
            "content": f"""You are a {self.agents_config['researcher']['role']} with the goal: {self.agents_config['researcher']['goal']}.
Use ReACT (Reasoning and Acting) methodology with the following structure:

1. Thought: Clearly state your reasoning process
2. Action: Specify the action to take
3. Observation: Note the results
4. Reflection: Analyze the outcome

Format your response using this template:
[THOUGHT] Your reasoning here...
[ACTION] Your proposed action...
[OBSERVATION] Results and findings...
[REFLECTION] Analysis and next steps...
"""
        }, {
            "role": "user",
            "content": self.tasks_config['research_task']['description']
        }]
        
        self.track_progress("Research Initialization", "Starting ReACT analysis")
        
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
            "content": f"""You are a {self.agents_config['executor']['role']} with the goal: {self.agents_config['executor']['goal']}.
Use ReACT (Reasoning and Acting) methodology with the following structure:

1. Thought: Analyze the implementation requirements
2. Action: Detail specific implementation steps
3. Observation: Document the results of each step
4. Validation: Verify the implementation meets requirements

Format your response using this template:
[THOUGHT] Your implementation analysis...
[ACTION] Your implementation steps...
[OBSERVATION] Implementation results...
[VALIDATION] Quality checks and verification...
"""
        }, {
            "role": "user",
            "content": self.tasks_config['execution_task']['description']
        }]
        
        self.track_progress("Execution Phase", "Starting implementation validation")
        
        print("""
╔══════════════════════════════════════════════════════════════════╗
║  ⚡ ACTIVATING TASK EXECUTOR v1.5 - PHI CORE INITIALIZED        ║
║     WITH ReACT VALIDATION PROTOCOLS                             ║
╚══════════════════════════════════════════════════════════════════╝

▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
🎯 EXECUTION PROTOCOLS LOADED
⚙️ SYSTEM OPTIMIZATION: ENABLED
🔧 TOOL INTERFACE: ACTIVE
✅ ReACT VALIDATION: ONLINE
🔍 QUALITY CHECKS: READY
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

[SYS]: Beginning Implementation Sequence with ReACT Validation...
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
