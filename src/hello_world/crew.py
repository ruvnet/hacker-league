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

class HelloWorldCrew:
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
            
    async def run_with_streaming(self, prompt="Tell me about yourself", task_type="both"):
        """Run crew with streaming responses using advanced medical diagnostic workflow"""
        # Create tools
        tools = [CustomTool()]
        
        self.progress_tracker["total_steps"] = 7  # Triage + Diagnostics + Pathology + Radiology + Specialist + Review + Final Report
        
        if task_type in ["research", "both"]:
            await self._run_triage(prompt)
            await self._run_diagnostician(prompt)
            
        if task_type in ["execute", "both"]:
            await self._run_pathologist(prompt)
            await self._run_radiologist(prompt)
            await self._run_specialist(prompt)
            
        if task_type in ["analyze", "both"]:
            await self._run_reviewer(prompt)
            
        return True

    async def _run_triage(self, prompt):
        """Run the emergency triage specialist agent"""
        triage_messages = [{
            "role": "system",
            "content": f"""You are a {self.agents_config['triage']['role']} with the goal: {self.agents_config['triage']['goal']}.
Use ReACT (Reasoning and Acting) methodology with the following structure:

1. Thought: Assess urgency and severity of presenting symptoms
2. Action: Check vital signs and perform rapid assessment
3. Observation: Document key findings and red flags
4. Priority: Assign triage level and immediate actions needed

Format your response using this template:
[THOUGHT] Your urgency assessment...
[ACTION] Your triage steps...
[OBSERVATION] Key findings...
[PRIORITY] Triage level and next steps...
"""
        }, {
            "role": "user",
            "content": f"{self.tasks_config['triage_task']['description']}\n\nUser Prompt: {prompt}"
        }]
        
        self.track_progress("Emergency Triage", "Starting rapid assessment")
        
        print("""
╔══════════════════════════════════════════════════════════════════╗
║  🚨 INITIALIZING EMERGENCY TRIAGE v2.0 - RAPID ASSESSMENT CORE  ║
╚══════════════════════════════════════════════════════════════════╝
        
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
🔄 ACTIVATING TRIAGE PROTOCOLS...
💉 VITAL SIGNS MONITOR: ACTIVE
⚡ RAPID ASSESSMENT: ONLINE
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

[SYS]: Beginning Emergency Triage Assessment...
""")
        await stream_openrouter_response(triage_messages, self.agents_config['triage']['llm'])

    async def _run_diagnostician(self, prompt):
        """Run the primary diagnostician agent"""
        diagnostician_messages = [{
            "role": "system",
            "content": f"""You are a {self.agents_config['diagnostician']['role']} with the goal: {self.agents_config['diagnostician']['goal']}.
Use ReACT (Reasoning and Acting) methodology with the following structure:

1. Thought: Analyze patient history and triage findings
2. Action: Perform detailed physical examination
3. Observation: Document comprehensive clinical findings
4. Plan: Order diagnostic tests and develop initial plan
5. Documentation: Record detailed clinical notes

Format your response using this template:
[THOUGHT] Your diagnostic reasoning...
[ACTION] Your examination steps...
[OBSERVATION] Clinical findings...
[PLAN] Diagnostic tests ordered...
[DOCUMENTATION] Clinical notes...
"""
        }, {
            "role": "user",
            "content": f"{self.tasks_config['diagnostic_task']['description']}\n\nUser Prompt: {prompt}"
        }]
        
        self.track_progress("Primary Diagnosis", "Conducting comprehensive evaluation")
        
        print("""
╔══════════════════════════════════════════════════════════════════╗
║  🏥 INITIALIZING PRIMARY DIAGNOSTICIAN v2.0 - CLINICAL CORE     ║
╚══════════════════════════════════════════════════════════════════╝
        
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
🔄 ACTIVATING DIAGNOSTIC PROTOCOLS...
📋 CLINICAL ASSESSMENT: ACTIVE
🔬 DIAGNOSTIC ENGINE: ONLINE
📝 DOCUMENTATION SYSTEM: READY
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

[SYS]: Beginning Comprehensive Medical Assessment...
""")
        await stream_openrouter_response(diagnostician_messages, self.agents_config['diagnostician']['llm'])

    async def _run_pathologist(self, prompt):
        """Run the clinical pathologist agent"""
        pathologist_messages = [{
            "role": "system",
            "content": f"""You are a {self.agents_config['pathologist']['role']} with the goal: {self.agents_config['pathologist']['goal']}.
Use ReACT (Reasoning and Acting) methodology with the following structure:

1. Thought: Review laboratory test orders and specimens
2. Action: Analyze laboratory results and tissue samples
3. Observation: Document microscopic and molecular findings
4. Integration: Correlate findings with clinical presentation
5. Report: Generate detailed pathology report

Format your response using this template:
[THOUGHT] Your analysis approach...
[ACTION] Your laboratory steps...
[OBSERVATION] Pathological findings...
[INTEGRATION] Clinical correlation...
[REPORT] Pathology report...
"""
        }, {
            "role": "user",
            "content": f"{self.tasks_config['pathology_task']['description']}\n\nUser Prompt: {prompt}"
        }]
        
        self.track_progress("Pathology Analysis", "Processing laboratory results")
        
        print("""
╔══════════════════════════════════════════════════════════════════╗
║  🔬 INITIALIZING PATHOLOGY LAB v2.0 - ANALYSIS CORE            ║
╚══════════════════════════════════════════════════════════════════╝
        
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
🔄 LOADING LABORATORY PROTOCOLS...
🧪 SPECIMEN ANALYSIS: ACTIVE
🔍 MICROSCOPY SYSTEM: ONLINE
📊 MOLECULAR DIAGNOSTICS: READY
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

[SYS]: Beginning Laboratory Analysis...
""")
        await stream_openrouter_response(pathologist_messages, self.agents_config['pathologist']['llm'])

    async def _run_radiologist(self, prompt):
        """Run the imaging specialist agent"""
        radiologist_messages = [{
            "role": "system",
            "content": f"""You are a {self.agents_config['radiologist']['role']} with the goal: {self.agents_config['radiologist']['goal']}.
Use ReACT (Reasoning and Acting) methodology with the following structure:

1. Thought: Review imaging orders and clinical history
2. Action: Analyze medical imaging studies
3. Observation: Document imaging findings and measurements
4. Integration: Correlate with clinical presentation
5. Report: Generate detailed radiology report

Format your response using this template:
[THOUGHT] Your analysis approach...
[ACTION] Your imaging review steps...
[OBSERVATION] Radiological findings...
[INTEGRATION] Clinical correlation...
[REPORT] Radiology report...
"""
        }, {
            "role": "user",
            "content": f"{self.tasks_config['radiology_task']['description']}\n\nUser Prompt: {prompt}"
        }]
        
        self.track_progress("Radiology Analysis", "Interpreting imaging studies")
        
        print("""
╔══════════════════════════════════════════════════════════════════╗
║  📷 INITIALIZING RADIOLOGY SYSTEM v2.0 - IMAGING CORE          ║
╚══════════════════════════════════════════════════════════════════╝
        
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
🔄 LOADING IMAGING PROTOCOLS...
🖥️ IMAGE PROCESSING: ACTIVE
📊 MEASUREMENT TOOLS: ONLINE
📋 REPORTING SYSTEM: READY
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

[SYS]: Beginning Imaging Analysis...
""")
        await stream_openrouter_response(radiologist_messages, self.agents_config['radiologist']['llm'])

    async def _run_specialist(self, prompt):
        """Run the medical specialist agent"""
        specialist_messages = [{
            "role": "system",
            "content": f"""You are a {self.agents_config['specialist']['role']} with the goal: {self.agents_config['specialist']['goal']}.
Use ReACT (Reasoning and Acting) methodology with the following structure:

1. Thought: Review all diagnostic, pathology, and imaging findings
2. Action: Synthesize findings and develop treatment strategy
3. Analysis: Consider treatment options and evidence base
4. Plan: Create detailed, personalized treatment plan
5. Documentation: Record comprehensive treatment rationale

Format your response using this template:
[THOUGHT] Your comprehensive analysis...
[ACTION] Your synthesis approach...
[ANALYSIS] Treatment considerations...
[PLAN] Detailed treatment plan...
[DOCUMENTATION] Treatment rationale...
"""
        }, {
            "role": "user",
            "content": f"{self.tasks_config['specialist_task']['description']}\n\nUser Prompt: {prompt}"
        }]
        
        self.track_progress("Specialist Analysis", "Developing comprehensive treatment plan")
        
        print("""
╔══════════════════════════════════════════════════════════════════╗
║  🏥 ACTIVATING MEDICAL SPECIALIST v2.0 - TREATMENT CORE         ║
║     WITH EVIDENCE-BASED PROTOCOLS                               ║
╚══════════════════════════════════════════════════════════════════╝

▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
🎯 TREATMENT PROTOCOLS LOADED
⚕️ CLINICAL GUIDELINES: ENABLED
📚 EVIDENCE DATABASE: ACTIVE
✅ MEDICAL VALIDATION: ONLINE
🔍 SAFETY CHECKS: READY
📝 DOCUMENTATION SYSTEM: INITIALIZED
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

[SYS]: Beginning Comprehensive Treatment Planning...
""")
        await stream_openrouter_response(specialist_messages, self.agents_config['specialist']['llm'])

    async def _run_reviewer(self, prompt):
        """Run the medical review board agent"""
        with open('config/analysis.yaml', 'r') as f:
            analysis_config = yaml.safe_load(f)
            
        reviewer_messages = [{
            "role": "system",
            "content": f"""You are a {self.agents_config['reviewer']['role']} with the goal: {self.agents_config['reviewer']['goal']}.
Use ReACT (Reasoning and Acting) methodology with the following structure:

1. Thought: Review all diagnostic findings and specialist recommendations
2. Action: Validate treatment plan against evidence-based guidelines
3. Analysis: Consider alternative approaches and risk factors
4. Discussion: Document multi-disciplinary team conclusions
5. Recommendation: Provide final consensus recommendations
6. Quality: Assess adherence to clinical standards

Format your response using this template:
[THOUGHT] Your review process...
[ACTION] Your validation steps...
[ANALYSIS] Alternative considerations...
[DISCUSSION] Team conclusions...
[RECOMMENDATION] Final consensus plan...
[QUALITY] Standards assessment...

Analysis Configuration:
{yaml.dump(analysis_config, default_flow_style=False)}
"""
        }, {
            "role": "user",
            "content": f"{self.tasks_config['review_task']['description']}\n\nUser Prompt: {prompt}"
        }]
        
        self.track_progress("Medical Review Board", "Conducting multi-disciplinary review")
        
        print("""
╔══════════════════════════════════════════════════════════════════╗
║  🏥 INITIALIZING MEDICAL REVIEW BOARD v2.0 - CONSENSUS CORE     ║
╚══════════════════════════════════════════════════════════════════╝
        
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
🔄 LOADING CLINICAL GUIDELINES...
📚 EVIDENCE DATABASE: ACTIVE
👥 TEAM CONSENSUS: ENABLED
✅ VALIDATION ENGINE: ONLINE
📊 QUALITY METRICS: READY
📝 DOCUMENTATION SYSTEM: INITIALIZED
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

[SYS]: Beginning Multi-Disciplinary Review Process...
""")
        await stream_openrouter_response(reviewer_messages, self.agents_config['reviewer']['llm'])
        
    def run(self, prompt="Tell me about yourself", task_type="both"):
        """Run crew synchronously"""
        try:
            return asyncio.run(self.run_with_streaming(prompt=prompt, task_type=task_type))
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
