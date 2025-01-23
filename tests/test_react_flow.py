import unittest
import yaml
from hello_world.config.react_validation import ReactValidator

class TestReactFlow(unittest.TestCase):
    def setUp(self):
        # Load validation rules from prompts.yaml
        with open("src/hello_world/config/prompts.yaml", "r") as f:
            self.config = yaml.safe_load(f)
        self.validator = ReactValidator(self.config["templates"]["validation_rules"])

    def test_thought_validation(self):
        # Test valid thought format
        valid_thought = "Thought: I should analyze the user input before proceeding"
        self.assertTrue(self.validator.validate_thought(valid_thought))

        # Test invalid format
        invalid_thought = "Invalid thought format"
        self.assertFalse(self.validator.validate_thought(invalid_thought))

        # Test minimum length requirement
        short_thought = "Thought: Too short"
        self.assertFalse(self.validator.validate_thought(short_thought))

    def test_action_validation(self):
        # Test valid action format
        valid_action = "Action: search_web(query=\"CrewAI framework\")"
        self.assertTrue(self.validator.validate_action(valid_action))

        # Test invalid format
        invalid_action = "Invalid action format"
        self.assertFalse(self.validator.validate_action(invalid_action))

        # Test missing required fields
        incomplete_action = "Action: search_web"
        self.assertFalse(self.validator.validate_action(incomplete_action))

    def test_observation_validation(self):
        # Test valid observation
        valid_obs = "Observation: Found 5 relevant articles about CrewAI"
        self.assertTrue(self.validator.validate_observation(valid_obs))

        # Test invalid format
        invalid_obs = "Invalid observation"
        self.assertFalse(self.validator.validate_observation(invalid_obs))

    def test_progress_tracking(self):
        # Initialize tracking
        self.validator.start_tracking("test_task")
        
        # Test progress update
        self.validator.update_progress(1, 3, "Started analysis")
        self.assertEqual(self.validator.current_step, 1)
        self.assertEqual(self.validator.total_steps, 3)

        # Test completion
        self.validator.complete_task()
        self.assertTrue(self.validator.is_complete)

    def test_streaming_updates(self):
        # Test stream initialization
        stream = self.validator.create_stream()
        self.assertIsNotNone(stream)

        # Test streaming messages
        message = "Test progress update"
        self.validator.stream_update(message)
        self.assertIn(message, self.validator.stream_history)

if __name__ == "__main__":
    unittest.main()
