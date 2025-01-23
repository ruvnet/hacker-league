import unittest
import yaml
import os
from hello_world.config.config_loader import ConfigLoader

class TestConfig(unittest.TestCase):
    def setUp(self):
        self.config_loader = ConfigLoader()
        self.config_dir = "src/hello_world/config"

    def test_load_prompts_yaml(self):
        # Test loading prompts.yaml
        prompts = self.config_loader.load_prompts()
        self.assertIsNotNone(prompts)
        self.assertIn("templates", prompts)
        self.assertIn("user_prompts", prompts["templates"])
        self.assertIn("validation_rules", prompts["templates"])

    def test_prompt_templates(self):
        prompts = self.config_loader.load_prompts()
        templates = prompts["templates"]["user_prompts"]

        # Test input templates
        self.assertIn("input", templates)
        self.assertIn("default", templates["input"])
        self.assertIn("validation", templates["input"])

        # Test progress templates
        self.assertIn("progress", templates)
        self.assertIn("start", templates["progress"])
        self.assertIn("step", templates["progress"])
        self.assertIn("complete", templates["progress"])

    def test_progress_tracking_config(self):
        prompts = self.config_loader.load_prompts()
        tracking = prompts["templates"]["progress_tracking"]

        # Test tracking format
        self.assertIn("format", tracking)
        self.assertIsInstance(tracking["format"], str)

        # Test status definitions
        self.assertIn("statuses", tracking)
        self.assertIsInstance(tracking["statuses"], list)
        self.assertGreater(len(tracking["statuses"]), 0)

    def test_backward_compatibility(self):
        # Test with minimal config
        minimal_config = {
            "templates": {
                "user_prompts": {
                    "input": {"default": "Basic prompt"}
                }
            }
        }

        # Verify defaults are applied
        config = self.config_loader.apply_defaults(minimal_config)
        self.assertIn("validation_rules", config["templates"])
        self.assertIn("progress_tracking", config["templates"])

    def test_validation_rules_config(self):
        prompts = self.config_loader.load_prompts()
        rules = prompts["templates"]["validation_rules"]

        # Test thought rules
        self.assertIn("thought", rules)
        self.assertIn("format", rules["thought"])
        self.assertIn("min_length", rules["thought"])

        # Test action rules
        self.assertIn("action", rules)
        self.assertIn("format", rules["action"])
        self.assertIn("required_fields", rules["action"])

    def test_config_validation(self):
        # Test invalid config detection
        invalid_config = {"invalid": "structure"}
        with self.assertRaises(ValueError):
            self.config_loader.validate_config(invalid_config)

        # Test missing required fields
        incomplete_config = {"templates": {}}
        with self.assertRaises(ValueError):
            self.config_loader.validate_config(incomplete_config)

if __name__ == "__main__":
    unittest.main()
