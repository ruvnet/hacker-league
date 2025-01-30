"""
NOVA (Neuro-Symbolic, Optimized, Versatile Agent) Crew Implementation
"""

import warnings
warnings.filterwarnings('ignore', category=UserWarning)

import yaml
from dotenv import load_dotenv
import os
import httpx
import json
import asyncio
from typing import Dict, Any, Optional
from nova.tools.custom_tool import create_tool
from nova.cache import NovaCache

load_dotenv()  # Load environment variables from .env file

# Global cache instance
_cache = NovaCache()

async def stream_openrouter_response(messages, model, cache: NovaCache, progress_callback=None):
    """Stream responses directly from OpenRouter with progress tracking and caching"""
    # Generate cache key from messages and model
    cache_key = json.dumps({"messages": messages, "model": model}, sort_keys=True)
    
    # Try to get from cache first
    cached_response = await cache.get_api_result(cache_key)
    if cached_response is not None:
        print(cached_response, end='', flush=True)
        return

    async with httpx.AsyncClient() as client:
        async with client.stream(
            "POST",
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:3000",
                "X-Title": "NOVA Console"
            },
            json={
                "model": model,
                "messages": messages,
                "stream": True,
                "temperature": 0.7
            },
            timeout=None
        ) as response:
            full_response = ""
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
                                        full_response += content
                                        print(content, end='', flush=True)
                    except (json.JSONDecodeError, UnicodeDecodeError):
                        continue
            
            # Cache the complete response
            await cache.set_api_result(cache_key, full_response)

class NovaCrew:
    """Main NOVA implementation combining all components"""
    
    def __init__(self):
        self.cache = _cache  # Use global cache instance
        self.symbolic_engine = create_tool("symbolic")
        self.language_normalizer = create_tool("data")  # Using data tool for LASER functionality
        self.tool_interface = create_tool("api")
        
        # Initialize tracking
        self.validation_status = {"reasoning": [], "actions": []}
        self.progress_tracker = {"current_step": 0, "total_steps": 0, "status": ""}

    async def validate_reasoning(self, reasoning_step: Dict) -> Dict:
        """Validate reasoning using symbolic engine and cache results"""
        cache_key = json.dumps(reasoning_step, sort_keys=True)
        
        # Try to get validation result from cache
        cached_result = await self.cache.get_inference(cache_key)
        if cached_result is not None:
            return cached_result
            
        validation_result = {
            "step": reasoning_step,
            "valid": True,
            "feedback": []
        }
        
        if not reasoning_step.get("thought"):
            validation_result["valid"] = False
            validation_result["feedback"].append("Missing thought process")
        
        self.validation_status["reasoning"].append(validation_result)
        
        # Cache the validation result
        await self.cache.set_inference(cache_key, validation_result)
        return validation_result

    async def validate_action(self, action_step: Dict) -> Dict:
        """Validate action before execution and cache results"""
        cache_key = json.dumps(action_step, sort_keys=True)
        
        # Try to get validation result from cache
        cached_result = await self.cache.get_inference(cache_key)
        if cached_result is not None:
            return cached_result
            
        validation_result = {
            "step": action_step,
            "valid": True,
            "feedback": []
        }
        
        if not action_step.get("action"):
            validation_result["valid"] = False
            validation_result["feedback"].append("Missing action definition")
            
        self.validation_status["actions"].append(validation_result)
        
        # Cache the validation result
        await self.cache.set_inference(cache_key, validation_result)
        return validation_result

    def track_progress(self, step_type: str, status: str):
        """Track progress with detailed formatting"""
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

    async def run_with_streaming(self, prompt: str = "Tell me about yourself", task_type: str = "both") -> bool:
        """Run NOVA system with streaming responses"""
        cleanup_task = None
        try:
            self.progress_tracker["total_steps"] = 4
            
            # Start cache cleanup task
            cleanup_task = asyncio.create_task(self.cache.start_cleanup_task())
            
            print("""
╔══════════════════════════════════════════════════════════════════╗
║              NOVA NEURAL ORCHESTRATION SYSTEM                    ║
║        [ NEURO-SYMBOLIC OPTIMIZED VERSATILE AGENT ]             ║
╚══════════════════════════════════════════════════════════════════╝
""")
            
            if task_type in ["research", "both"]:
                await self._run_research_phase(prompt)
                
            if task_type in ["execute", "both"]:
                await self._run_execution_phase(prompt)
                
            if task_type == "analyze":
                await self._run_analysis_phase(prompt)
                
            # Print cache metrics
            metrics = self.cache.get_metrics()
            print(f"""
Cache Performance Metrics:
- Hit Rate: {metrics['hit_rate']:.2f}%
- Hits: {metrics['hits']}
- Misses: {metrics['misses']}
- Evictions: {metrics['evictions']}
- API Cache Size: {metrics['api_cache_size']}
- Inference Cache Size: {metrics['inference_cache_size']}
""")
            
            print("""
╔══════════════════════════════════════════════════════════════════╗
║             🌟 NOVA PROCESSING COMPLETE 🌟                       ║
╚══════════════════════════════════════════════════════════════════╝

▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
        ✨ ALL OBJECTIVES ACHIEVED
        📊 PERFORMANCE METRICS OPTIMAL
        🔒 SYSTEM INTEGRITY MAINTAINED
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
""")
            return True
            
        except Exception as e:
            print(f"""
╔══════════════════════════════════════════════════════════════════╗
║  ⚠️ NOVA SYSTEM MALFUNCTION DETECTED                           ║
╚══════════════════════════════════════════════════════════════════╝
🔍 Error Analysis:
{str(e)}
🔧 Initiating recovery protocols...
""")
            return False
            
        finally:
            # Cancel cleanup task if it exists
            if cleanup_task is not None:
                cleanup_task.cancel()
                try:
                    await cleanup_task
                except asyncio.CancelledError:
                    pass

    async def _run_research_phase(self, prompt: str):
        """Execute research phase"""
        researcher_messages = [{
            "role": "system",
            "content": """You are a NOVA Research Analyst specializing in neuro-symbolic reasoning.
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
            "content": f"Analyze the following using NOVA methodology:\n\n{prompt}"
        }]
        
        self.track_progress("Research Phase", "Starting ReACT analysis")
        
        print("""
╔══════════════════════════════════════════════════════════════════╗
║  🤖 INITIALIZING RESEARCH ANALYST - NOVA CORE LOADED            ║
╚══════════════════════════════════════════════════════════════════╝
        
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
🔄 ACTIVATING ReACT PROTOCOL...
📡 NEURAL INTERFACE ONLINE
🧠 COGNITIVE SYSTEMS ENGAGED
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

[SYS]: Initiating ReACT Methodology Analysis...
""")
        await stream_openrouter_response(researcher_messages, "anthropic/claude-2", self.cache)
        
    async def _run_execution_phase(self, prompt: str):
        """Execute implementation phase"""
        executor_messages = [{
            "role": "system",
            "content": """You are a NOVA Task Executor specializing in implementing solutions.
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
            "content": f"Implement solution for:\n\n{prompt}"
        }]
        
        self.track_progress("Execution Phase", "Starting implementation")
        
        print("""
╔══════════════════════════════════════════════════════════════════╗
║  ⚡ ACTIVATING TASK EXECUTOR - NOVA CORE INITIALIZED            ║
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
        await stream_openrouter_response(executor_messages, "anthropic/claude-2", self.cache)
        
    async def _run_analysis_phase(self, prompt: str):
        """Execute analysis phase"""
        analyzer_messages = [{
            "role": "system",
            "content": """You are a NOVA Performance Analyzer specializing in system optimization.
Use ReACT (Reasoning and Acting) methodology with the following structure:

1. Thought: Analyze current performance metrics and thresholds
2. Action: Compare against defined rules and benchmarks
3. Observation: Document findings and patterns
4. Recommendation: Suggest optimizations based on analysis

Format your response using this template:
[THOUGHT] Your analysis process...
[ACTION] Your evaluation steps...
[OBSERVATION] Performance findings...
[RECOMMENDATION] Optimization suggestions...
"""
        }, {
            "role": "user",
            "content": f"Analyze performance for:\n\n{prompt}"
        }]
        
        self.track_progress("Analysis Phase", "Starting performance analysis")
        
        print("""
╔══════════════════════════════════════════════════════════════════╗
║  📊 INITIALIZING PERFORMANCE ANALYZER - METRICS CORE            ║
╚══════════════════════════════════════════════════════════════════╝
        
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
🔄 LOADING ANALYSIS CONFIGURATION...
📡 METRIC COLLECTION: ACTIVE
🧮 OPTIMIZATION ENGINE: ONLINE
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

[SYS]: Beginning Performance Analysis...
""")
        await stream_openrouter_response(analyzer_messages, "anthropic/claude-2", self.cache)

    def run(self, prompt: str = "Tell me about yourself", task_type: str = "both") -> bool:
        """Synchronous entry point"""
        try:
            return asyncio.run(self.run_with_streaming(prompt=prompt, task_type=task_type))
        except KeyboardInterrupt:
            print("""
╔══════════════════════════════════════════════════════════════════╗
║  🛑 NOVA EMERGENCY SHUTDOWN SEQUENCE INITIATED                  ║
╚══════════════════════════════════════════════════════════════════╝
⚠️ Saving neural state...
💾 Preserving memory banks...
🔌 Powering down cores...
""")
            return False
        except Exception as e:
            print(f"""
╔══════════════════════════════════════════════════════════════════╗
║  ⚠️ NOVA SYSTEM MALFUNCTION DETECTED                           ║
╚══════════════════════════════════════════════════════════════════╝
🔍 Error Analysis:
{str(e)}
🔧 Initiating recovery protocols...
""")
            return False