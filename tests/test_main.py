import sys
import pytest
from unittest.mock import patch
from ruv_cli import cli

def test_main_execution():
    """Should execute main() function from cli module"""
    with patch.object(sys, 'argv', ['ruv']):
        with pytest.raises(SystemExit) as exc_info:
            cli.main()
        assert exc_info.value.code == 0

def test_main_import():
    """Should not execute main() when imported"""
    with patch('ruv_cli.cli.main') as mock_main:
        # Simulate importing the module
        with patch('builtins.__name__', 'not_main'):
            from ruv_cli import __main__
            mock_main.assert_not_called()