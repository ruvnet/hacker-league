import os
from dotenv import load_dotenv
from e2b_code_interpreter import Sandbox, OutputMessage

# Load environment variables from .env file
load_dotenv(".env")

def handle_stdout(msg: OutputMessage):
    print(f"Output: {msg}")

def test_sandbox():
    """Test E2B sandbox functionality"""
    try:
        api_key = os.getenv("E2B_API_KEY")
        if not api_key:
            raise RuntimeError("E2B_API_KEY not set in environment")
            
        print("Creating sandbox...")
        sandbox = Sandbox(api_key=api_key)
        
        print("Testing code execution...")
        test_code = """
print('Hello from sandbox!')
x = 1 + 1
print(f'2 + 2 = {x + 2}')
"""
        execution = sandbox.run_code(
            code=test_code,
            on_stdout=handle_stdout
        )
        print("✓ Code execution successful")
        
        return True
    except Exception as e:
        print(f"✗ Sandbox test failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_sandbox()