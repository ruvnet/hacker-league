from crewai import Agent, Crew, Process, Task
from beverages.tools.custom_tool import CustomTool
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
                "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
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
                                        print(content, end='', flush=True)
                    except (json.JSONDecodeError, UnicodeDecodeError):
                        continue

class BeverageCrew:
    def __init__(self):
        with open('config/agents.yaml', 'r') as f:
            self.agents_config = yaml.safe_load(f)
        with open('config/tasks.yaml', 'r') as f:
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
            
    async def run_with_streaming(self, prompt="Tell me about yourself", task_type="both"):
        """Run crew with streaming responses using advanced beverage development workflow"""
        tools = [CustomTool()]
        
        self.progress_tracker["total_steps"] = 6  # Market Research + Consumer Analysis + Product Development + Quality Assessment + Marketing Strategy + Review
        
        if task_type in ["research", "both"]:
            await self._run_market_research(prompt)
            await self._run_consumer_analysis(prompt)
            
        if task_type in ["execute", "both"]:
            await self._run_product_development(prompt)
            await self._run_quality_assessment(prompt)
            await self._run_marketing_strategy(prompt)
            
        if task_type in ["analyze", "both"]:
            await self._run_review_board(prompt)
            
        return True

    async def _run_market_research(self, prompt):
        """Run the market research specialist agent"""
        market_research_messages = [{
            "role": "system",
            "content": f"""You are a {self.agents_config['market_researcher']['role']} with the goal: {self.agents_config['market_researcher']['goal']}.
Use ReACT (Reasoning and Acting) methodology with the following structure:

1. Thought: Analyze market trends and opportunities
2. Action: Gather market data and competitor insights
3. Observation: Document key findings and patterns
4. Plan: Identify potential market gaps and opportunities

Format your response using this template:
[THOUGHT] Your market analysis...
[ACTION] Your research steps...
[OBSERVATION] Key findings...
[PLAN] Market opportunities...
"""
        }, {
            "role": "user",
            "content": f"{self.tasks_config['market_research_task']['description']}\n\nUser Prompt: {prompt}"
        }]
        
        self.track_progress("Market Research", "Starting market analysis")
        
        print("""
╔══════════════════════════════════════════════════════════════════╗
║  📊 INITIALIZING MARKET RESEARCH v2.0 - ANALYSIS CORE          ║
╚══════════════════════════════════════════════════════════════════╝
        
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
🔄 ACTIVATING RESEARCH PROTOCOLS...
📈 TREND ANALYSIS: ACTIVE
🔍 MARKET INSIGHTS: ONLINE
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

[SYS]: Beginning Market Research Analysis...
""")
        await stream_openrouter_response(market_research_messages, self.agents_config['market_researcher']['llm'])

    async def _run_consumer_analysis(self, prompt):
        """Run the consumer behavior analyst agent"""
        consumer_analysis_messages = [{
            "role": "system",
            "content": f"""You are a {self.agents_config['consumer_analyst']['role']} with the goal: {self.agents_config['consumer_analyst']['goal']}.
Use ReACT (Reasoning and Acting) methodology with the following structure:

1. Thought: Analyze consumer behavior patterns
2. Action: Evaluate demographic preferences
3. Observation: Document consumer insights
4. Plan: Identify target segments and preferences

Format your response using this template:
[THOUGHT] Your consumer analysis...
[ACTION] Your research steps...
[OBSERVATION] Consumer insights...
[PLAN] Target segments...
"""
        }, {
            "role": "user",
            "content": f"{self.tasks_config['consumer_analysis_task']['description']}\n\nUser Prompt: {prompt}"
        }]
        
        self.track_progress("Consumer Analysis", "Analyzing consumer behavior")
        
        print("""
╔══════════════════════════════════════════════════════════════════╗
║  👥 INITIALIZING CONSUMER ANALYSIS v2.0 - BEHAVIOR CORE        ║
╚══════════════════════════════════════════════════════════════════╝
        
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
🔄 ACTIVATING ANALYSIS PROTOCOLS...
📊 DEMOGRAPHIC ANALYSIS: ACTIVE
🎯 PREFERENCE MAPPING: ONLINE
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

[SYS]: Beginning Consumer Behavior Analysis...
""")
        await stream_openrouter_response(consumer_analysis_messages, self.agents_config['consumer_analyst']['llm'])

    async def _run_product_development(self, prompt):
        """Run the product developer agent"""
        product_development_messages = [{
            "role": "system",
            "content": f"""You are a {self.agents_config['product_developer']['role']} with the goal: {self.agents_config['product_developer']['goal']}.
Use ReACT (Reasoning and Acting) methodology with the following structure:

1. Thought: Analyze product requirements
2. Action: Design product formulation
3. Observation: Document development process
4. Plan: Create product specifications

Format your response using this template:
[THOUGHT] Your product analysis...
[ACTION] Your development steps...
[OBSERVATION] Product details...
[PLAN] Specifications...
"""
        }, {
            "role": "user",
            "content": f"{self.tasks_config['product_development_task']['description']}\n\nUser Prompt: {prompt}"
        }]
        
        self.track_progress("Product Development", "Designing product formulation")
        
        print("""
╔══════════════════════════════════════════════════════════════════╗
║  🧪 INITIALIZING PRODUCT DEVELOPMENT v2.0 - FORMULATION CORE   ║
╚══════════════════════════════════════════════════════════════════╝
        
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
🔄 ACTIVATING DEVELOPMENT PROTOCOLS...
🧬 FORMULATION ENGINE: ACTIVE
📋 SPECIFICATION SYSTEM: ONLINE
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

[SYS]: Beginning Product Development Process...
""")
        await stream_openrouter_response(product_development_messages, self.agents_config['product_developer']['llm'])

    async def _run_quality_assessment(self, prompt):
        """Run the quality analyst agent"""
        quality_assessment_messages = [{
            "role": "system",
            "content": f"""You are a {self.agents_config['quality_analyst']['role']} with the goal: {self.agents_config['quality_analyst']['goal']}.
Use ReACT (Reasoning and Acting) methodology with the following structure:

1. Thought: Review quality requirements
2. Action: Conduct quality tests
3. Observation: Document test results
4. Plan: Define quality standards

Format your response using this template:
[THOUGHT] Your quality analysis...
[ACTION] Your testing steps...
[OBSERVATION] Quality findings...
[PLAN] Quality standards...
"""
        }, {
            "role": "user",
            "content": f"{self.tasks_config['quality_assessment_task']['description']}\n\nUser Prompt: {prompt}"
        }]
        
        self.track_progress("Quality Assessment", "Evaluating product quality")
        
        print("""
╔══════════════════════════════════════════════════════════════════╗
║  🔍 INITIALIZING QUALITY ASSESSMENT v2.0 - TESTING CORE        ║
╚══════════════════════════════════════════════════════════════════╝
        
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
🔄 ACTIVATING QUALITY PROTOCOLS...
🧪 TEST SUITE: ACTIVE
📊 QUALITY METRICS: ONLINE
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

[SYS]: Beginning Quality Assessment Process...
""")
        await stream_openrouter_response(quality_assessment_messages, self.agents_config['quality_analyst']['llm'])

    async def _run_marketing_strategy(self, prompt):
        """Run the marketing strategist agent"""
        marketing_strategy_messages = [{
            "role": "system",
            "content": f"""You are a {self.agents_config['marketing_strategist']['role']} with the goal: {self.agents_config['marketing_strategist']['goal']}.
Use ReACT (Reasoning and Acting) methodology with the following structure:

1. Thought: Analyze market positioning
2. Action: Develop marketing strategy
3. Observation: Document strategy components
4. Plan: Create implementation roadmap

Format your response using this template:
[THOUGHT] Your strategy analysis...
[ACTION] Your planning steps...
[OBSERVATION] Strategy details...
[PLAN] Implementation roadmap...
"""
        }, {
            "role": "user",
            "content": f"{self.tasks_config['marketing_strategy_task']['description']}\n\nUser Prompt: {prompt}"
        }]
        
        self.track_progress("Marketing Strategy", "Developing marketing plan")
        
        print("""
╔══════════════════════════════════════════════════════════════════╗
║  📢 INITIALIZING MARKETING STRATEGY v2.0 - PLANNING CORE       ║
╚══════════════════════════════════════════════════════════════════╝
        
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
🔄 ACTIVATING STRATEGY PROTOCOLS...
🎯 POSITIONING ENGINE: ACTIVE
📋 PLANNING SYSTEM: ONLINE
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

[SYS]: Beginning Marketing Strategy Development...
""")
        await stream_openrouter_response(marketing_strategy_messages, self.agents_config['marketing_strategist']['llm'])

    async def _run_review_board(self, prompt):
        """Run the product review board agent"""
        with open('config/analysis.yaml', 'r') as f:
            analysis_config = yaml.safe_load(f)
            
        review_board_messages = [{
            "role": "system",
            "content": f"""You are a {self.agents_config['review_board']['role']} with the goal: {self.agents_config['review_board']['goal']}.
Use ReACT (Reasoning and Acting) methodology with the following structure:

1. Thought: Review all development components
2. Action: Validate product strategy
3. Analysis: Consider market viability
4. Discussion: Document board conclusions
5. Recommendation: Provide launch guidance
6. Quality: Assess development standards

Format your response using this template:
[THOUGHT] Your review process...
[ACTION] Your validation steps...
[ANALYSIS] Viability assessment...
[DISCUSSION] Board conclusions...
[RECOMMENDATION] Launch guidance...
[QUALITY] Standards assessment...

Analysis Configuration:
{yaml.dump(analysis_config, default_flow_style=False)}
"""
        }, {
            "role": "user",
            "content": f"{self.tasks_config['review_task']['description']}\n\nUser Prompt: {prompt}"
        }]
        
        self.track_progress("Product Review Board", "Conducting final review")
        
        print("""
╔══════════════════════════════════════════════════════════════════╗
║  ⭐ INITIALIZING PRODUCT REVIEW BOARD v2.0 - EVALUATION CORE   ║
╚══════════════════════════════════════════════════════════════════╝
        
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
🔄 LOADING REVIEW PROTOCOLS...
📊 EVALUATION ENGINE: ACTIVE
✅ VALIDATION SYSTEM: ONLINE
📋 DOCUMENTATION: READY
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

[SYS]: Beginning Product Review Process...
""")
        await stream_openrouter_response(review_board_messages, self.agents_config['review_board']['llm'])
        
    def run(self, prompt="Tell me about yourself", task_type="both"):
        """Run crew synchronously"""
        try:
            return asyncio.run(self.run_with_streaming(prompt=prompt, task_type=task_type))
        except KeyboardInterrupt:
            print("""
╔══════════════════════════════════════════════════════════════════╗
║  🛑 EMERGENCY SHUTDOWN SEQUENCE INITIATED                        ║
╚══════════════════════════════════════════════════════════════════╝
⚠️ Saving analysis state...
💾 Preserving market data...
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
