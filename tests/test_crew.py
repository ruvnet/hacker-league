"""Tests for the InsiderMirrorCrew class."""

import pytest
import os
import asyncio
from datetime import datetime, timezone
from unittest.mock import patch, Mock, AsyncMock
from insider_mirror.crew import InsiderMirrorCrew

@pytest.fixture
def mock_env_vars():
    """Set up test environment variables"""
    os.environ["FINNHUB_API_KEY"] = "test_api_key"
    os.environ["FINNHUB_ENDPOINT"] = "https://test.api/insider-trades"
    os.environ["INITIAL_PORTFOLIO_VALUE"] = "100000"
    yield
    del os.environ["FINNHUB_API_KEY"]
    del os.environ["FINNHUB_ENDPOINT"]
    del os.environ["INITIAL_PORTFOLIO_VALUE"]

@pytest.fixture
def crew(mock_env_vars):
    """Create a test instance of InsiderMirrorCrew"""
    return InsiderMirrorCrew()

def test_crew_initialization(crew):
    """Test crew initialization"""
    assert crew.portfolio_value == 100000.0
    assert crew.is_running is False
    assert hasattr(crew, 'data_agent')
    assert hasattr(crew, 'analysis_agent')
    assert hasattr(crew, 'trading_agent')
    assert hasattr(crew, 'reporting_agent')

def test_load_config(crew):
    """Test configuration loading"""
    agents_config = crew._load_config("src/insider_mirror/config/agents.yaml")
    tasks_config = crew._load_config("src/insider_mirror/config/tasks.yaml")
    
    assert "data_agent" in agents_config
    assert "analysis_agent" in agents_config
    assert "trading_agent" in agents_config
    assert "reporting_agent" in agents_config
    
    assert "data_task" in tasks_config
    assert "analysis_task" in tasks_config
    assert "trading_task" in tasks_config
    assert "reporting_task" in tasks_config

def test_load_config_error():
    """Test error handling in configuration loading"""
    crew = InsiderMirrorCrew()
    with pytest.raises(RuntimeError):
        crew._load_config("nonexistent/config.yaml")

@pytest.mark.asyncio
async def test_run_cycle_success(crew, sample_trade_data):
    """Test successful execution of a complete cycle"""
    # Mock successful data agent execution
    mock_data_result = {
        "status": "success",
        "data": sample_trade_data,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    # Mock successful analysis agent execution
    mock_analysis_result = {
        "status": "success",
        "filtered_trades": sample_trade_data[:1],  # Only first trade passes filters
        "patterns": {"test": "patterns"},
        "risk_metrics": {"test": "metrics"},
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    # Mock successful trading agent execution
    mock_trading_result = {
        "status": "success",
        "executions": [{"trade": "details"}],
        "portfolio": {
            "total_value": 110000,
            "positions": {"AAPL": {"shares": 100}}
        },
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    # Mock successful reporting agent execution
    mock_report_result = {
        "status": "success",
        "metrics": {"test": "metrics"},
        "reports": {"html": "report.html"},
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    # Apply mocks
    with patch.object(crew.data_agent, 'execute', AsyncMock(return_value=mock_data_result)), \
         patch.object(crew.analysis_agent, 'execute', AsyncMock(return_value=mock_analysis_result)), \
         patch.object(crew.trading_agent, 'execute', AsyncMock(return_value=mock_trading_result)), \
         patch.object(crew.reporting_agent, 'execute', AsyncMock(return_value=mock_report_result)):
        
        result = await crew.run_cycle()
        
        assert result["status"] == "success"
        assert "timestamp" in result
        assert "data" in result
        assert result["data"]["trades_fetched"] == len(sample_trade_data)
        assert result["data"]["trades_analyzed"] == 1
        assert result["data"]["trades_executed"] == 1
        assert result["data"]["portfolio_value"] == 110000
        assert "reports" in result["data"]

@pytest.mark.asyncio
async def test_run_cycle_data_error(crew):
    """Test cycle handling of data fetch error"""
    mock_error_result = {
        "status": "error",
        "error": "API Error",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    with patch.object(crew.data_agent, 'execute', AsyncMock(return_value=mock_error_result)):
        result = await crew.run_cycle()
        
        assert result["status"] == "error"
        assert "error" in result
        assert "API Error" in result["error"]

@pytest.mark.asyncio
async def test_run_cycle_no_trades(crew, sample_trade_data):
    """Test cycle handling when no trades pass analysis"""
    # Mock successful data fetch but no trades pass analysis
    mock_data_result = {
        "status": "success",
        "data": sample_trade_data,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    mock_analysis_result = {
        "status": "success",
        "filtered_trades": [],  # No trades pass filters
        "patterns": {"test": "patterns"},
        "risk_metrics": {"test": "metrics"},
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    # Mock empty trading result
    mock_trading_result = {
        "status": "success",
        "executions": [],
        "portfolio": {
            "total_value": crew.portfolio_value,
            "positions": {}
        },
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    # Mock empty report result
    mock_report_result = {
        "status": "success",
        "metrics": {},
        "reports": {"html": "report.html"},
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    with patch.object(crew.data_agent, 'execute', AsyncMock(return_value=mock_data_result)), \
         patch.object(crew.analysis_agent, 'execute', AsyncMock(return_value=mock_analysis_result)), \
         patch.object(crew.trading_agent, 'execute', AsyncMock(return_value=mock_trading_result)), \
         patch.object(crew.reporting_agent, 'execute', AsyncMock(return_value=mock_report_result)):
        
        result = await crew.run_cycle()
        
        assert result["status"] == "success"
        assert result["data"]["trades_analyzed"] == 0
        assert result["data"]["trades_executed"] == 0
        assert result["data"]["portfolio_value"] == crew.portfolio_value

@pytest.mark.asyncio
async def test_start_stop(crew):
    """Test system start and stop functionality"""
    # Mock run_cycle to avoid actual execution
    mock_cycle_result = {
        "status": "success",
        "data": {
            "trades_fetched": 0,
            "trades_analyzed": 0,
            "trades_executed": 0,
            "portfolio_value": 100000,
            "reports": {}
        },
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    with patch.object(crew, 'run_cycle', AsyncMock(return_value=mock_cycle_result)):
        # Start system with very short interval for testing
        start_task = asyncio.create_task(crew.start(interval_seconds=0.1))
        
        # Let it run briefly
        await asyncio.sleep(0.2)
        
        # Stop system
        await crew.stop()
        
        assert crew.is_running is False

@pytest.mark.asyncio
async def test_error_recovery(crew, sample_trade_data):
    """Test system recovery from errors"""
    # Mock cycle to fail once then succeed
    mock_results = iter([
        {
            "status": "error",
            "error": "Temporary error",
            "timestamp": datetime.now(timezone.utc).isoformat()
        },
        {
            "status": "success",
            "data": {
                "trades_fetched": len(sample_trade_data),
                "trades_analyzed": 1,
                "trades_executed": 1,
                "portfolio_value": 100000,
                "reports": {"html": "report.html"}
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    ])
    
    with patch.object(crew, 'run_cycle', AsyncMock(side_effect=lambda: next(mock_results))):
        # Start system with very short interval
        start_task = asyncio.create_task(crew.start(interval_seconds=0.1))
        
        # Let it run briefly
        await asyncio.sleep(0.3)
        
        # Stop system
        await crew.stop()
        
        assert crew.is_running is False
        # System should have recovered from the error

@pytest.mark.asyncio
async def test_cleanup_on_stop(crew):
    """Test cleanup of resources on system stop"""
    crew.is_running = True
    crew.portfolio_value = 150000  # Modified value
    
    await crew.stop()
    
    assert crew.is_running is False
    # Verify agents were cleaned up
    assert crew.data_agent.validation_status == {"reasoning": [], "actions": []}
    assert crew.analysis_agent.validation_status == {"reasoning": [], "actions": []}
    assert crew.trading_agent.validation_status == {"reasoning": [], "actions": []}
    assert crew.reporting_agent.validation_status == {"reasoning": [], "actions": []}