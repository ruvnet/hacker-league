import os
from typing import Optional

class CodeAgent:
    """Agent for code generation and execution"""
    def __init__(self, name: str = "CodeAgent"):
        self.name = name
        
    def log(self, message: str):
        """Print a log message with agent name prefix"""
        print(f"[{self.name}] {message}")
        
    def run(self, code: str) -> str:
        """Execute code in sandbox"""
        try:
            # In real implementation, this would use E2B CodeInterpreter
            # For testing, we'll just simulate execution
            return f"Executed: {code}"
        except Exception as e:
            self.log(f"Error executing code: {str(e)}")
            return ""

def run_code(user_query: str) -> bool:
    """Generate and execute Python code based on user query"""
    if not user_query:
        print("[ERROR] No query provided for code agent.")
        return False
        
    try:
        # Generate code from LLM
        code = _generate_code(user_query)
        if not code:
            print("[ERROR] Failed to generate code.")
            return False
            
        # Execute in sandbox
        agent = CodeAgent()
        result = agent.run(code)
        agent.log(f"Execution Result:\n{result}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Code execution failed: {str(e)}")
        return False

def _generate_code(prompt: str) -> Optional[str]:
    """Generate Python code from text prompt"""
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    if not openrouter_key:
        raise RuntimeError("OPENROUTER_API_KEY not set.")
        
    try:
        # In real implementation, this would use OpenRouter API
        # For testing, we'll just return a simple code snippet
        return "print('Hello, World!')"
        
    except Exception as e:
        print(f"[ERROR] Code generation failed: {str(e)}")
        return None