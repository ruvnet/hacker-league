import os
from e2b_code_interpreter import Sandbox

def test_sdk():
    """Test E2B SDK directly"""
    try:
        print("Testing E2B SDK...")
        api_key = os.getenv("E2B_API_KEY")
        if not api_key:
            raise RuntimeError("E2B_API_KEY not set")
            
        print(f"Using API key: {api_key}")
        print("Creating sandbox...")
        sandbox = Sandbox(api_key=api_key)
        
        print("Running test code...")
        test_code = """
print('Hello from sandbox!')
x = 1 + 1
print(f'2 + 2 = {x + 2}')
"""
        result = sandbox.run_code(test_code)
        print("✓ Code execution successful")
        print(f"Result: {result}")
        
    except Exception as e:
        print(f"✗ Test failed: {str(e)}")

if __name__ == "__main__":
    test_sdk()