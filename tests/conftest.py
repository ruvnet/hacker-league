"""Test configuration and fixtures for the Insider Trading Mirror System."""

import os
import pytest
import yaml
from pathlib import Path
from typing import Dict, Any

# Ensure we're using test configurations
os.environ["TESTING"] = "true"
os.environ["FINNHUB_API_KEY"] = "test_api_key"
os.environ["FINNHUB_ENDPOINT"] = "https://api.finnhub.io/api/v1/stock/insider-transactions"
os.environ["INITIAL_PORTFOLIO_VALUE"] = "100000"

@pytest.fixture
def sample_trade_data() -> list[Dict[str, Any]]:
    """Sample insider trading data for testing"""
    return [
        {
            "symbol": "AAPL",
            "transaction_type": "PURCHASE",
            "shares": 1000,
            "price": 150.0,
            "value": 150000.0,
            "filing_date": "2024-01-25T00:00:00Z"
        },
        {
            "symbol": "TSLA",
            "transaction_type": "SALE",
            "shares": 500,
            "price": 180.0,
            "value": 90000.0,
            "filing_date": "2024-01-25T00:00:00Z"
        },
        {
            "symbol": "MSFT",
            "transaction_type": "PURCHASE",
            "shares": 2000,
            "price": 200.0,
            "value": 400000.0,
            "filing_date": "2024-01-25T00:00:00Z"
        }
    ]

@pytest.fixture
def agent_config() -> Dict[str, Any]:
    """Load agent configuration for testing"""
    config_path = Path("src/insider_mirror/config/agents.yaml")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config

@pytest.fixture
def tasks_config() -> Dict[str, Any]:
    """Load tasks configuration for testing"""
    config_path = Path("src/insider_mirror/config/tasks.yaml")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config

@pytest.fixture
def analysis_config() -> Dict[str, Any]:
    """Load analysis configuration for testing"""
    config_path = Path("src/insider_mirror/config/analysis.yaml")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config

@pytest.fixture
def mock_api_response(sample_trade_data) -> Dict[str, Any]:
    """Mock API response for testing"""
    return {
        "status": "success",
        "data": sample_trade_data
    }

@pytest.fixture
def test_reports_dir(tmp_path) -> Path:
    """Create a temporary directory for test reports"""
    reports_dir = tmp_path / "reports"
    reports_dir.mkdir()
    return reports_dir