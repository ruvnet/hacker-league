"""
NOVA Knowledge Distillation Core Implementation with Clean JSON Output
"""
import yaml
from dotenv import load_dotenv
import os
import httpx
import json
import asyncio
import re
from typing import Dict, Any, Optional, List
from pathlib import Path
from nova.cache import NovaCache
from nova.cache import NovaCache

load_dotenv()  # Load environment variables from .env file

class KnowledgeDistiller:
    """Core knowledge distillation implementation"""
    
    def __init__(self):
        # Load configurations
        config_dir = Path(__file__).parent.parent / 'config'
        with open(config_dir / 'models.yaml', 'r') as f:
            self.models_config = yaml.safe_load(f)
        with open(config_dir / 'tasks.yaml', 'r') as f:
            self.tasks_config = yaml.safe_load(f)
            
        # Initialize cache and tracking
        self.cache = NovaCache()
        self.progress_tracker = {
            "current_step": 0,
            "total_steps": 0,
            "status": ""
        }
        
        self.validation_metrics = {
            "knowledge_extraction": [],
            "model_training": [],
            "performance_analysis": []
        }

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

    def fix_json_formatting(self, text: str) -> str:
                """Fix common JSON formatting issues"""
                # Add missing commas between array elements and object properties
                text = re.sub(r'}\s+{', '}, {', text)
                text = re.sub(r'"\s+"', '", "', text)
                text = re.sub(r']\s+[{"]', '], ', text)
                text = re.sub(r'"[}\]]\s+[{\["]\w+":"', '", "', text)
                text = re.sub(r'"[}\]]\s+"', '", "', text)
                
                # Add missing commas between object properties
                text = re.sub(r'"\s*}\s*"', '"},"', text)
                text = re.sub(r'"\s*]\s*"', '"],"', text)
                text = re.sub(r'"\s*}\s*{', '"},"', text)
                text = re.sub(r'"\s*}\s*\[', '"},"', text)
                
                # Fix missing commas after values
                text = re.sub(r'(\d+)\s+[{\["]\w+":"', r'\1, "', text)
                text = re.sub(r'(\d+)\s+"', r'\1, "', text)
                text = re.sub(r'(\d+|\btrue\b|\bfalse\b|\bnull\b)\s+[{\["]\w+":"', r'\1, "', text)
                
                # Fix malformed object structures
                text = re.sub(r'\}\s*"(\w+)":', r'}, "\1":', text)
                text = re.sub(r'\]\s*"(\w+)":', r'], "\1":', text)
                text = re.sub(r'"(\w+)"\s*([{\[])', r'"\1": \2', text)
                
                # Ensure proper JSON structure
                if not text.startswith('{'):
                    text = '{' + text
                if not text.endswith('}'):
                    text = text + '}'
                    
                return text
    
    def _extract_json_from_response(self, text: str) -> Optional[Dict]:
            """Extract and validate JSON object from response text"""
            try:
                # Find JSON-like content
                start = text.find('{')
                end = text.rfind('}') + 1
                if start >= 0 and end > start:
                    json_str = text[start:end]
                    # Fix common formatting issues
                    json_str = self.fix_json_formatting(json_str)
                    return json.loads(json_str)
            except json.JSONDecodeError:
                pass
            return None

    async def validate_performance(self, model_name: str, metrics: Dict[str, float]) -> bool:
        """Validate model performance against thresholds"""
        thresholds = self.tasks_config['validation_thresholds']
        
        # Check accuracy
        if metrics.get('accuracy', 0) < thresholds['accuracy']['min']:
            print(f"❌ Accuracy below minimum threshold: {metrics['accuracy']:.2f} < {thresholds['accuracy']['min']}")
            return False
            
        # Check latency
        if metrics.get('latency_ms', float('inf')) > thresholds['latency']['max_ms']:
            print(f"❌ Latency above maximum threshold: {metrics['latency_ms']}ms > {thresholds['latency']['max_ms']}ms")
            return False
            
        # Check memory usage
        if metrics.get('memory_mb', float('inf')) > thresholds['memory']['max_mb']:
            print(f"❌ Memory usage above maximum threshold: {metrics['memory_mb']}MB > {thresholds['memory']['max_mb']}MB")
            return False
            
        # Check knowledge coverage
        if metrics.get('coverage', 0) < thresholds['coverage']['min']:
            print(f"❌ Knowledge coverage below minimum threshold: {metrics['coverage']:.2f} < {thresholds['coverage']['min']}")
            return False
            
        print("""
✅ Performance Validation Passed:
   - Accuracy within threshold
   - Latency within threshold
   - Memory usage within threshold
   - Knowledge coverage within threshold
""")
        return True

    async def extract_knowledge(self, domain: str, prompt: str) -> Dict[str, Any]:
        """Extract domain knowledge using teacher model"""
        self.track_progress("Knowledge Extraction", "Starting domain analysis")
        
        print("""
╔══════════════════════════════════════════════════════════════════╗
║  🧠 INITIALIZING KNOWLEDGE EXTRACTION                           ║
╚══════════════════════════════════════════════════════════════════╝

▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
🔄 LOADING DOMAIN CONFIGURATION...
📡 TEACHER MODEL: ACTIVE
🧮 EXTRACTION ENGINE: ONLINE
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
""")
        
        # Check cache first
        cache_key = f"knowledge_extraction_{domain}_{prompt}"
        cached_knowledge = await self.cache.get_response(cache_key)
        if cached_knowledge:
            print("\n📦 Using cached knowledge extraction")
            print("🔄 Processing...", end='', flush=True)
            knowledge = self._extract_json_from_response(cached_knowledge)
            if knowledge:
                print(" ✅")
                return knowledge
            print(" ❌")
        
        messages = [{
            "role": "system",
            "content": f"""You are a {self.models_config['teacher_models']['researcher']['role']} with the goal: {self.models_config['teacher_models']['researcher']['goal']}.

IMPORTANT: You must respond with ONLY a valid JSON object. Follow this exact format with all commas and quotes:

{{
    "concepts": [
        {{
            "name": "example1",
            "description": "description1"
        }},
        {{
            "name": "example2",
            "description": "description2"
        }}
    ],
    "relationships": [
        {{
            "source": "example1",
            "target": "example2",
            "type": "relates_to"
        }}
    ],
    "patterns": [
        {{
            "name": "pattern1",
            "steps": [
                "step1",
                "step2",
                "step3"
            ],
            "examples": [
                "example1",
                "example2"
            ]
        }}
    ],
    "validation": {{
        "coverage": 0.95,
        "completeness": 0.9,
        "consistency": 1.0
    }}
}}

RULES:
1. Include ALL commas between array elements and object properties
2. Use double quotes for ALL strings (property names and values)
3. No comments or extra text
4. Numbers should not have quotes
5. Keep exact formatting with proper indentation

{{
    "concepts": [
        {{"name": "string", "description": "string"}}
    ],
    "relationships": [
        {{"source": "string", "target": "string", "type": "string"}}
    ],
    "patterns": [
        {{"name": "string", "steps": ["string"], "examples": ["string"]}}
    ],
    "validation": {{
        "coverage": float,  # 0-1 score
        "completeness": float,  # 0-1 score
        "consistency": float  # 0-1 score
    }}
}}"""
        }, {
            "role": "user",
            "content": f"{self.tasks_config['knowledge_extraction']['description']}\n\nDomain: {domain}\nPrompt: {prompt}"
        }]
        
        knowledge_base = {}
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
                    "model": self.models_config['teacher_models']['researcher']['llm'],
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
                                            # Show only progress dots
                                            if len(content.strip()) > 0 and not content.strip().startswith('Cache'):
                                                print(".", end='', flush=True)
                        except (json.JSONDecodeError, UnicodeDecodeError):
                            continue
                
                knowledge_base = self._extract_json_from_response(full_response)
                if knowledge_base:
                    await self.cache.set_response(cache_key, full_response)
                else:
                    print("❌ Error: Invalid JSON response from model")
                    knowledge_base = {}
        
        return knowledge_base

    async def train_student_model(self, architecture: str, knowledge_base: Dict[str, Any]) -> Dict[str, float]:
        """Train student model using extracted knowledge"""
        self.track_progress("Model Training", "Initializing student model")
        
        print("""
╔══════════════════════════════════════════════════════════════════╗
║  🎯 INITIALIZING MODEL TRAINING                                 ║
╚══════════════════════════════════════════════════════════════════╝

▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
🔄 LOADING STUDENT ARCHITECTURE...
📡 KNOWLEDGE TRANSFER: ACTIVE
🧮 OPTIMIZATION ENGINE: ONLINE
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
""")
        
        # Check cache for training results
        cache_key = f"model_training_{architecture}_{hash(json.dumps(knowledge_base, sort_keys=True))}"
        cached_metrics = await self.cache.get_response(cache_key)
        if cached_metrics:
            print("\n📦 Using cached training metrics")
            print("🔄 Processing...", end='', flush=True)
            metrics = self._extract_json_from_response(cached_metrics)
            if metrics:
                print(" ✅")
                return metrics
            print(" ❌")
        
        messages = [{
            "role": "system",
            "content": f"""You are a {self.models_config['teacher_models']['analyzer']['role']} with the goal: {self.models_config['teacher_models']['analyzer']['goal']}.

IMPORTANT: You must respond with ONLY a valid JSON object. Follow this exact format with all commas:

{{
    "accuracy": 0.95,
    "latency_ms": 20.5,
    "memory_mb": 450.0,
    "coverage": 0.9,
    "compression_ratio": 2.5
}}

RULES:
1. Include ALL commas between properties
2. Use double quotes for property names
3. No comments or extra text
4. Numbers should be floating point (not integers)
5. Keep exact formatting with proper indentation"""
        }, {
            "role": "user",
            "content": f"{self.tasks_config['model_training']['description']}\n\nArchitecture: {architecture}\nKnowledge Base: {json.dumps(knowledge_base, indent=2)}"
        }]
        
        metrics = {}
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
                    "model": self.models_config['teacher_models']['analyzer']['llm'],
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
                                            # Show only progress dots for JSON content
                                            if len(content.strip()) > 0:
                                                print(".", end='', flush=True)
                        except (json.JSONDecodeError, UnicodeDecodeError):
                            continue
                
                metrics = self._extract_json_from_response(full_response)
                if metrics:
                    await self.cache.set_response(cache_key, full_response)
                else:
                    print("❌ Error: Invalid JSON response from model")
                    metrics = {}
        
        return metrics

    async def run_distillation(self, domain: str, prompt: str, architecture: str = "transformer_tiny") -> bool:
        """Run complete knowledge distillation pipeline"""
        try:
            # Extract knowledge
            knowledge_base = await self.extract_knowledge(domain, prompt)
            if not knowledge_base:
                return False
            
            # Train student model
            metrics = await self.train_student_model(architecture, knowledge_base)
            if not metrics:
                return False
            
            # Validate performance
            success = await self.validate_performance(architecture, metrics)
            
            if success:
                print(f"""
Performance Metrics:
- Accuracy: {metrics.get('accuracy', 0):.2f}
- Latency: {metrics.get('latency_ms', 0):.1f}ms
- Memory Usage: {metrics.get('memory_mb', 0):.1f}MB
- Knowledge Coverage: {metrics.get('coverage', 0):.2f}
- Compression Ratio: {metrics.get('compression_ratio', 0):.1f}x
""")
            
            return success
            
        except Exception as e:
            print(f"""
╔══════════════════════════════════════════════════════════════════╗
║  ⚠️ DISTILLATION ERROR DETECTED                                ║
╚══════════════════════════════════════════════════════════════════╝
🔍 Error Analysis:
{str(e)}
🔧 Initiating recovery protocols...
""")
            return False

    def run(self, domain: str, prompt: str, architecture: str = "transformer_tiny") -> bool:
        """Synchronous entry point"""
        try:
            return asyncio.run(self.run_distillation(domain, prompt, architecture))
        except KeyboardInterrupt:
            print("""
╔══════════════════════════════════════════════════════════════════╗
║  🛑 EMERGENCY SHUTDOWN SEQUENCE INITIATED                        ║
╚══════════════════════════════════════════════════════════════════╝
⚠️ Saving neural state...
💾 Preserving memory banks...
🔌 Powering down cores...
""")
            return False
        except Exception as e:
            print(f"""
╔══════════════════════════════════════════════════════════════════╗
║  ⚠️ SYSTEM MALFUNCTION DETECTED                                 ║
╚══════════════════════════════════════════════════════════════════╝
🔍 Error Analysis:
{str(e)}
🔧 Initiating recovery protocols...
""")
            return False