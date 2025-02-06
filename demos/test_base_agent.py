from src.insider_mirror.agents.base_agent import BaseAgent

def main():
    # Create a test configuration
    config = {
        "verbose": True,
        "react_validation": {
            "thought_required": True,
            "reasoning_depth": 2
        }
    }
    
    # Initialize base agent
    agent = BaseAgent("test_agent", config)
    
    # Test progress tracking
    agent.track_progress(1, "Initializing test agent")
    
    # Test reasoning validation
    reasoning = "This is a test thought. It demonstrates multiple sentence validation."
    is_valid = agent.validate_reasoning(reasoning)
    print(f"\nReasoning validation result: {is_valid}")
    
    # Test action validation 
    action = "Test action being performed"
    is_valid = agent.validate_action(action)
    print(f"Action validation result: {is_valid}")
    
    # Test progress update
    agent.update_progress(1, 3, "Testing progress updates")
    
    # Clean up
    agent.cleanup()

if __name__ == "__main__":
    main()
