import pytest
from unittest.mock import patch
from ruv_cli.commands.agent.data_agent import DataAgent, run_data_operation

def test_data_agent_initialization():
    """Should initialize with default name"""
    agent = DataAgent()
    assert agent.name == "DataAgent"
    
    agent = DataAgent(name="CustomAgent")
    assert agent.name == "CustomAgent"

def test_data_agent_run_no_operation():
    """Should fail when no operation provided"""
    agent = DataAgent()
    result = agent.run("")
    assert result == ""

def test_data_agent_run_invalid_operation():
    """Should fail with invalid operation"""
    agent = DataAgent()
    result = agent.run("invalid")
    assert result == ""

def test_data_agent_load_success():
    """Should load data successfully"""
    agent = DataAgent()
    result = agent.run("load", file_path="data.csv")
    assert "Loaded data from data.csv" in result

def test_data_agent_load_no_file():
    """Should fail when no file path provided for load"""
    agent = DataAgent()
    result = agent.run("load")
    assert result == ""

def test_data_agent_describe_success():
    """Should describe data successfully"""
    agent = DataAgent()
    result = agent.run("describe", file_path="data.csv", columns=["col1", "col2"])
    assert "Description of col1, col2 in data.csv" in result

def test_data_agent_describe_no_file():
    """Should fail when no file path provided for describe"""
    agent = DataAgent()
    result = agent.run("describe")
    assert result == ""

def test_data_agent_plot_success():
    """Should plot data successfully"""
    agent = DataAgent()
    result = agent.run("plot", file_path="data.csv", columns=["col1", "col2"])
    assert "Plot saved for col1, col2 from data.csv" in result

def test_data_agent_plot_no_file():
    """Should fail when no file path provided for plot"""
    agent = DataAgent()
    result = agent.run("plot")
    assert result == ""

def test_run_data_operation_no_operation():
    """Should fail when no operation provided"""
    assert not run_data_operation("")

def test_run_data_operation_success():
    """Should successfully run data operation"""
    assert run_data_operation("load", file_path="data.csv")

def test_run_data_operation_failure():
    """Should handle operation failures"""
    def mock_run(*args, **kwargs):
        raise Exception("Test error")
    
    with patch('ruv_cli.commands.agent.data_agent.DataAgent.run', side_effect=mock_run):
        assert not run_data_operation("load", file_path="data.csv")

def test_data_agent_describe_all_columns():
    """Should describe all columns when none specified"""
    agent = DataAgent()
    result = agent.run("describe", file_path="data.csv")
    assert "Description of all columns in data.csv" in result

def test_data_agent_plot_all_columns():
    """Should plot all columns when none specified"""
    agent = DataAgent()
    result = agent.run("plot", file_path="data.csv")
    assert "Plot saved for all columns from data.csv" in result