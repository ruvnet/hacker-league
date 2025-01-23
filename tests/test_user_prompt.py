import unittest
from hello_world.tools.user_prompt import BaseUserPrompt

class TestBaseUserPrompt(unittest.TestCase):
    def setUp(self):
        self.prompt = BaseUserPrompt()

    def test_input_validation(self):
        # Test valid input
        schema = {"name": str, "age": int}
        valid_input = {"name": "test", "age": 25}
        self.assertTrue(self.prompt.validate_input(valid_input, schema))

        # Test invalid input - missing field
        invalid_input = {"name": "test"}
        self.assertFalse(self.prompt.validate_input(invalid_input, schema))

        # Test invalid input - wrong type
        invalid_type = {"name": "test", "age": "25"}
        self.assertFalse(self.prompt.validate_input(invalid_type, schema))

    def test_response_formatting(self):
        # Test text format
        data = {"key": "value"}
        self.assertEqual(self.prompt.format_response(data, "text"), str(data))

        # Test JSON format
        import json
        self.assertEqual(
            self.prompt.format_response(data, "json"),
            json.dumps(data)
        )

        # Test invalid format
        with self.assertRaises(ValueError):
            self.prompt.format_response(data, "invalid")

    def test_progress_tracking(self):
        # Test normal progress
        progress = self.prompt.track_progress(5, 10)
        self.assertEqual(progress, 50.0)
        self.assertEqual(self.prompt.current_step, 5)
        self.assertEqual(self.prompt.total_steps, 10)

        # Test zero total steps
        progress = self.prompt.track_progress(0, 0)
        self.assertEqual(progress, 0)

    def test_status_update(self):
        status = "Testing status"
        self.prompt.update_status(status)
        self.assertEqual(self.prompt.status, status)

    def test_input_sanitization(self):
        input_str = " test input \n"
        clean_str = self.prompt._sanitize_input(input_str)
        self.assertEqual(clean_str, "test input")

if __name__ == '__main__':
    unittest.main()
