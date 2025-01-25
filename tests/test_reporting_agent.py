"""Tests for the ReportingAgent class."""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta
from pathlib import Path
from unittest.mock import patch
from insider_mirror.agents.reporting_agent import ReportingAgent

@pytest.mark.asyncio
async def test_reporting_agent_initialization(agent_config):
    """Test ReportingAgent initialization"""
    agent = ReportingAgent(agent_config["reporting_agent"])
    assert agent.name == "reporting_agent"
    assert agent.config == agent_config["reporting_agent"]
    assert agent.validation_status == {"reasoning": [], "actions": []}
    assert agent.reports_dir.exists()

def test_calculate_metrics_win_rate(agent_config):
    """Test win rate calculation"""
    agent = ReportingAgent(agent_config["reporting_agent"])
    
    # Create trades across multiple days
    base_date = datetime.now(timezone.utc)
    trades = [
        {
            "symbol": "AAPL",
            "pnl": 100,
            "timestamp": (base_date - timedelta(days=2)).isoformat()
        },
        {
            "symbol": "MSFT",
            "pnl": -50,
            "timestamp": (base_date - timedelta(days=1)).isoformat()
        },
        {
            "symbol": "GOOGL",
            "pnl": 75,
            "timestamp": base_date.isoformat()
        }
    ]
    
    metrics = agent._calculate_metrics(trades)
    assert "win_rate" in metrics
    assert metrics["win_rate"] == 2/3  # 2 winning trades out of 3

def test_calculate_metrics_profit_factor(agent_config):
    """Test profit factor calculation"""
    agent = ReportingAgent(agent_config["reporting_agent"])
    
    # Create trades across multiple days
    base_date = datetime.now(timezone.utc)
    trades = [
        {
            "symbol": "AAPL",
            "pnl": 100,
            "timestamp": (base_date - timedelta(days=2)).isoformat()
        },
        {
            "symbol": "MSFT",
            "pnl": -50,
            "timestamp": (base_date - timedelta(days=1)).isoformat()
        },
        {
            "symbol": "GOOGL",
            "pnl": 200,
            "timestamp": base_date.isoformat()
        }
    ]
    
    metrics = agent._calculate_metrics(trades)
    assert "profit_factor" in metrics
    assert metrics["profit_factor"] == 6.0  # (100 + 200) / 50

def test_calculate_metrics_sharpe_ratio(agent_config):
    """Test Sharpe ratio calculation"""
    agent = ReportingAgent(agent_config["reporting_agent"])
    
    # Create trades across multiple days with consistent returns
    base_date = datetime.now(timezone.utc)
    trades = [
        {
            "symbol": "AAPL",
            "pnl": 100,
            "timestamp": (base_date - timedelta(days=2)).isoformat()
        },
        {
            "symbol": "MSFT",
            "pnl": 150,
            "timestamp": (base_date - timedelta(days=1)).isoformat()
        },
        {
            "symbol": "GOOGL",
            "pnl": 200,
            "timestamp": base_date.isoformat()
        }
    ]
    
    metrics = agent._calculate_metrics(trades)
    assert "sharpe_ratio" in metrics
    assert metrics["sharpe_ratio"] > 0  # Should be positive for consistent gains

def test_calculate_metrics_max_drawdown(agent_config):
    """Test maximum drawdown calculation"""
    agent = ReportingAgent(agent_config["reporting_agent"])
    
    # Create trades across multiple days
    base_date = datetime.now(timezone.utc)
    trades = [
        {
            "symbol": "AAPL",
            "pnl": 100,
            "timestamp": (base_date - timedelta(days=2)).isoformat()
        },
        {
            "symbol": "MSFT",
            "pnl": -150,
            "timestamp": (base_date - timedelta(days=1)).isoformat()
        },
        {
            "symbol": "GOOGL",
            "pnl": 50,
            "timestamp": base_date.isoformat()
        }
    ]
    
    metrics = agent._calculate_metrics(trades)
    assert "max_drawdown" in metrics
    assert metrics["max_drawdown"] == 150  # Largest negative excursion

def test_generate_html_report(agent_config, test_reports_dir):
    """Test HTML report generation"""
    agent = ReportingAgent(agent_config["reporting_agent"])
    agent.reports_dir = test_reports_dir
    
    data = {
        "trades": [
            {
                "symbol": "AAPL",
                "transaction_type": "PURCHASE",
                "shares": 100,
                "price": 150.0,
                "value": 15000.0,
                "timestamp": "2024-01-25T10:00:00Z"
            }
        ],
        "metrics": {
            "win_rate": 0.65,
            "profit_factor": 2.1,
            "sharpe_ratio": 1.5,
            "max_drawdown": 5000.0
        }
    }
    
    html_content = agent._generate_html_report(data)
    assert isinstance(html_content, str)
    assert "<!DOCTYPE html>" in html_content
    assert "Insider Trading Mirror Report" in html_content
    assert "AAPL" in html_content
    
    # Check for formatted metric values in HTML
    assert "65.00%" in html_content  # win_rate
    assert "2.10" in html_content    # profit_factor
    assert "1.50" in html_content    # sharpe_ratio
    assert "5,000.00" in html_content  # max_drawdown

def test_generate_csv_report(agent_config, test_reports_dir):
    """Test CSV report generation"""
    agent = ReportingAgent(agent_config["reporting_agent"])
    agent.reports_dir = test_reports_dir
    
    data = {
        "trades": [
            {
                "symbol": "AAPL",
                "transaction_type": "PURCHASE",
                "shares": 100,
                "price": 150.0,
                "value": 15000.0,
                "timestamp": "2024-01-25T10:00:00Z"
            }
        ],
        "metrics": {
            "win_rate": 0.65,
            "profit_factor": 2.1,
            "sharpe_ratio": 1.5,
            "max_drawdown": 5000.0
        }
    }
    
    csv_content = agent._generate_csv_report(data)
    assert isinstance(csv_content, str)
    assert "symbol" in csv_content
    assert "AAPL" in csv_content
    assert "win_rate" in csv_content
    assert "0.65" in csv_content

def test_save_report(agent_config, test_reports_dir):
    """Test report saving functionality"""
    agent = ReportingAgent(agent_config["reporting_agent"])
    agent.reports_dir = test_reports_dir
    
    content = "Test report content"
    format = "html"
    
    filepath = agent.save_report(content, format)
    saved_file = Path(filepath)
    
    assert saved_file.exists()
    assert saved_file.suffix == f".{format}"
    with open(saved_file, 'r', encoding='utf-8') as f:
        assert f.read() == content

@pytest.mark.asyncio
async def test_execute_success(agent_config, test_reports_dir):
    """Test successful execution of reporting agent"""
    agent = ReportingAgent(agent_config["reporting_agent"])
    agent.reports_dir = test_reports_dir
    
    base_date = datetime.now(timezone.utc)
    trades = [
        {
            "symbol": "AAPL",
            "transaction_type": "PURCHASE",
            "shares": 100,
            "price": 150.0,
            "value": 15000.0,
            "timestamp": base_date.isoformat(),
            "pnl": 500.0
        }
    ]
    
    portfolio_summary = {
        "total_value": 115000.0,
        "position_count": 1,
        "daily_trades": 1,
        "daily_pnl": 500.0
    }
    
    result = await agent.execute(trades, portfolio_summary)
    
    assert result["status"] == "success"
    assert "timestamp" in result
    assert "metrics" in result
    assert "reports" in result
    assert all(format in result["reports"] for format in agent.report_config["formats"])
    
    # Verify report files exist
    for filepath in result["reports"].values():
        assert Path(filepath).exists()

@pytest.mark.asyncio
async def test_execute_error_handling(agent_config, test_reports_dir):
    """Test error handling during execution"""
    agent = ReportingAgent(agent_config["reporting_agent"])
    agent.reports_dir = test_reports_dir
    
    # Test with invalid data
    invalid_trades = [{"invalid": "data"}]
    invalid_portfolio = {"invalid": "data"}
    
    result = await agent.execute(invalid_trades, invalid_portfolio)
    
    assert result["status"] == "error"
    assert "error" in result
    assert "timestamp" in result

def test_cleanup(agent_config):
    """Test cleanup of reporting agent resources"""
    agent = ReportingAgent(agent_config["reporting_agent"])
    
    # Add some test data to cleanup
    agent.validation_status = {
        "reasoning": ["test"],
        "actions": ["test"]
    }
    
    agent.cleanup()
    
    assert agent.validation_status == {"reasoning": [], "actions": []}
    assert agent.progress_tracker == {"current_step": 0, "total_steps": 0, "status": ""}