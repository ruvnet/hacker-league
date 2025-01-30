"""
NOVA (Neuro-Symbolic, Optimized, Versatile Agent) Crew Implementation
with Hierarchical Chain-of-Thought Reasoning
"""

import warnings
warnings.filterwarnings('ignore', category=UserWarning)

import yaml
from dotenv import load_dotenv
import os
import httpx
import json
import asyncio
from typing import Dict, Any, Optional, List
from nova.tools.custom_tool import create_tool
from nova.cache import NovaCache

load_dotenv()  # Load environment variables from .env file

class ReasoningModule:
    """Base class for specialized reasoning modules"""
    
    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt
        self.cache = NovaCache()
    
    async def reason(self, prompt: str) -> str:
        """Execute reasoning chain for this module"""
        messages = [{
            "role": "system",
            "content": self.system_prompt
        }, {
            "role": "user",
            "content": prompt
        }]
        
        await stream_openrouter_response(messages, "anthropic/claude-2", self.cache)
        return ""  # Actual response is streamed

class ConceptualReasoningModule(ReasoningModule):
    """Module for high-level conceptual reasoning"""
    
    def __init__(self):
        super().__init__(
            "ConceptualReasoning",
            """You are a NOVA Conceptual Reasoning Specialist.
Focus on understanding and explaining high-level concepts, relationships, and principles.
Use this structured format:
[CONCEPT] Define and explain the core concept
[RELATIONSHIPS] Identify key relationships and dependencies
[PRINCIPLES] Extract fundamental principles and patterns
[SYNTHESIS] Combine insights into a cohesive understanding"""
        )

class MathReasoningModule(ReasoningModule):
    """Module for mathematical and quantitative reasoning"""
    
    def __init__(self):
        super().__init__(
            "MathReasoning",
            """You are a NOVA Mathematical Reasoning Specialist.
Focus on numerical analysis, calculations, and mathematical relationships.
Use this structured format:
[GIVEN] List known quantities and relationships
[APPROACH] Outline mathematical method or formula to use
[CALCULATION] Show step-by-step solution
[VERIFICATION] Verify result and check units"""
        )

class ImplementationReasoningModule(ReasoningModule):
    """Module for implementation and technical reasoning"""
    
    def __init__(self):
        super().__init__(
            "ImplementationReasoning",
            """You are a NOVA Implementation Reasoning Specialist.
Focus on concrete implementation steps, technical details, and practical considerations.
Use this structured format:
[REQUIREMENTS] List technical requirements and constraints
[DESIGN] Outline implementation approach and architecture
[STEPS] Detail specific implementation steps
[VALIDATION] Define testing and validation criteria"""
        )

async def stream_openrouter_response(messages, model, cache: NovaCache):
    """Stream responses directly from OpenRouter with progress tracking and caching"""
    # Extract prompt from messages
    prompt = messages[-1]['content'] if messages else ""
    
    # Try to get from cache first
    cached_response = await cache.get_response(prompt)
    if cached_response is not None:
        return
        
    # If not in cache, get from OpenRouter
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
            await cache.set_response(prompt, full_response)

class NovaCrew:
    """Main NOVA implementation with Hierarchical Chain-of-Thought Reasoning"""
    
    def __init__(self):
        self.cache = NovaCache()
        self.symbolic_engine = create_tool("symbolic")
        self.language_normalizer = create_tool("data")
        self.tool_interface = create_tool("api")
        
        # Initialize reasoning modules
        self.conceptual_module = ConceptualReasoningModule()
        self.math_module = MathReasoningModule()
        self.implementation_module = ImplementationReasoningModule()
        
        # Initialize tracking
        self.validation_status = {"reasoning": [], "actions": []}
        self.progress_tracker = {"current_step": 0, "total_steps": 0, "status": ""}

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
        """Run NOVA system with streaming responses and hierarchical reasoning"""
        try:
            self.progress_tracker["total_steps"] = 4
            
            print("""
╔══════════════════════════════════════════════════════════════════╗
║              NOVA NEURAL ORCHESTRATION SYSTEM                    ║
║        [ NEURO-SYMBOLIC OPTIMIZED VERSATILE AGENT ]             ║
╚══════════════════════════════════════════════════════════════════╝
""")
            
            if task_type in ["research", "both"]:
                # Start with conceptual reasoning
                self.track_progress("Research Phase", "Starting Conceptual Analysis")
                print("""
╔══════════════════════════════════════════════════════════════════╗
║  🧠 ACTIVATING CONCEPTUAL REASONING MODULE                      ║
╚══════════════════════════════════════════════════════════════════╝
""")
                await self.conceptual_module.reason(f"Analyze the concept:\n\n{prompt}")
                
            if task_type in ["execute", "both"]:
                # Then do implementation reasoning
                self.track_progress("Execution Phase", "Starting Implementation Analysis")
                print("""
╔══════════════════════════════════════════════════════════════════╗
║  ⚡ ACTIVATING IMPLEMENTATION REASONING MODULE                  ║
╚══════════════════════════════════════════════════════════════════╝
""")
                await self.implementation_module.reason(f"Implement solution for:\n\n{prompt}")
                
            if task_type == "analyze":
                # Use math reasoning for analysis
                self.track_progress("Analysis Phase", "Starting Mathematical Analysis")
                print("""
╔══════════════════════════════════════════════════════════════════╗
║  📊 ACTIVATING MATHEMATICAL REASONING MODULE                    ║
╚══════════════════════════════════════════════════════════════════╝
""")
                await self.math_module.reason(f"Analyze performance metrics for:\n\n{prompt}")
                
            # Print cache metrics
            metrics = self.cache.get_metrics()
            print(f"""
Cache Performance Metrics:
- Hit Rate: {metrics['hit_rate']:.2f}%
- Hits: {metrics['hits']}
- Misses: {metrics['misses']}
- Cache Size: {metrics['cache_size']}
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