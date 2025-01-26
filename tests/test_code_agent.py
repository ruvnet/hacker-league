import os
import pytest
from unittest.mock import patch, MagicMock
from ruv_cli.commands.agent.code_agent import run_code, _generate_code, CodeAgent

@pytest.fixture(autouse=True)
def setup_env():
    """Set up environment variables for all tests"""
    os.environ["OPENROUTER_API_KEY"] = "test_key"
    yield
    if "OPENROUTER_API_KEY" in os.environ:
        del os.environ["OPENROUTER_API_KEY"]

def test_code_agent_initialization():
    """Should initialize with default name"""
    agent = CodeAgent()
    assert agent.name == "CodeAgent"
    
    agent = CodeAgent(name="CustomAgent")
    assert agent.name == "CustomAgent"

def test_code_agent_run():
    """Should execute code and return result"""
    agent = CodeAgent()
    result = agent.run("print('test')")
    assert result == "Executed: print('test')"

def test_code_agent_run_error(capsys):
    """Should handle execution errors"""
    def mock_run(*args, **kwargs):
        raise Exception("Test error")
    
    with patch('ruv_cli.commands.agent.code_agent.CodeAgent.run', side_effect=mock_run):
        result = run_code("invalid code")
        assert not result
        captured = capsys.readouterr()
        assert "Code execution failed: Test error" in captured.out

def test_run_code_no_query():
    """Should fail when no query is provided"""
    assert not run_code("")
    assert not run_code(None)

def test_run_code_success():
    """Should successfully generate and execute code"""
    assert run_code("Print hello world")

def test_run_code_no_api_key():
    """Should fail when OpenRouter API key is not set"""
    del os.environ["OPENROUTER_API_KEY"]
    assert not run_code("Print hello world")

def test_generate_code_success():
    """Should generate code from prompt"""
    code = _generate_code("Print hello world")
    assert code == "print('Hello, World!')"

def test_generate_code_no_api_key():
    """Should fail when OpenRouter API key is not set"""
    del os.environ["OPENROUTER_API_KEY"]
    with pytest.raises(RuntimeError, match="OPENROUTER_API_KEY not set"):
        _generate_code("Print hello world")

def test_generate_code_error(capsys):
    """Should handle generation errors"""
    def mock_generate(*args):
        raise Exception("Test error")
    
    with patch('ruv_cli.commands.agent.code_agent._generate_code', side_effect=mock_generate):
        assert not run_code("Print hello world")
        captured = capsys.readouterr()
        assert "Code execution failed: Test error" in captured.out