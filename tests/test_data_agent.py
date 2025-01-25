"""Tests for the DataAgent class."""

import pytest
import aiohttp
import asyncio
from datetime import datetime, timezone
from unittest.mock import Mock, patch, AsyncMock
from aioresponses import aioresponses
from insider_mirror.agents.data_agent import DataAgent

@pytest.mark.asyncio
async def test_data_agent_initialization(agent_config):
    """Test DataAgent initialization"""
    agent = DataAgent(agent_config["data_agent"])
    assert agent.name == "data_agent"
    assert agent.config == agent_config["data_agent"]
    assert agent.validation_status == {"reasoning": [], "actions": []}

@pytest.mark.asyncio
async def test_fetch_data_success(agent_config, sample_trade_data):
    """Test successful data fetching"""
    agent = DataAgent(agent_config["data_agent"])
    test_url = "https://test.api/insider-trades"
    
    with aioresponses() as mocked:
        mocked.get(
            test_url,
            status=200,
            payload=sample_trade_data
        )
        
        result = await agent.fetch_data(
            api_key="test_key",
            endpoint=test_url
        )
        
        assert result == sample_trade_data

@pytest.mark.asyncio
async def test_fetch_data_api_error(agent_config):
    """Test handling of API errors during fetch"""
    agent = DataAgent(agent_config["data_agent"])
    test_url = "https://test.api/insider-trades"
    
    with aioresponses() as mocked:
        mocked.get(
            test_url,
            status=500,
            body="Internal Server Error"
        )
        
        with pytest.raises(aiohttp.ClientError):
            await agent.fetch_data(
                api_key="test_key",
                endpoint=test_url
            )

def test_validate_data_success(agent_config, sample_trade_data):
    """Test successful data validation"""
    agent = DataAgent(agent_config["data_agent"])
    validated_data = agent.validate_data(sample_trade_data)
    
    assert len(validated_data) == len(sample_trade_data)
    for trade in validated_data:
        assert "symbol" in trade
        assert "transaction_type" in trade
        assert "shares" in trade
        assert "price" in trade
        assert "value" in trade
        assert "filing_date" in trade

def test_validate_data_missing_fields(agent_config):
    """Test validation with missing required fields"""
    agent = DataAgent(agent_config["data_agent"])
    invalid_data = [
        {
            "symbol": "AAPL",
            # Missing transaction_type
            "shares": 1000,
            "price": 150.0
        }
    ]
    
    validated_data = agent.validate_data(invalid_data)
    assert len(validated_data) == 0

def test_validate_data_invalid_types(agent_config):
    """Test validation with invalid data types"""
    agent = DataAgent(agent_config["data_agent"])
    invalid_data = [
        {
            "symbol": "AAPL",
            "transaction_type": "PURCHASE",
            "shares": "not_a_number",  # Invalid type
            "price": 150.0,
            "value": 150000.0,
            "filing_date": "2024-01-25T00:00:00Z"
        }
    ]
    
    validated_data = agent.validate_data(invalid_data)
    assert len(validated_data) == 0

@pytest.mark.asyncio
async def test_execute_success(agent_config, sample_trade_data):
    """Test successful execution of data agent"""
    agent = DataAgent(agent_config["data_agent"])
    test_url = "https://test.api/insider-trades"
    
    with aioresponses() as mocked:
        mocked.get(
            test_url,
            status=200,
            payload=sample_trade_data
        )
        
        result = await agent.execute(
            api_key="test_key",
            endpoint=test_url
        )
        
        assert result["status"] == "success"
        assert len(result["data"]) == len(sample_trade_data)
        assert "timestamp" in result
        
        # Verify timestamp format
        datetime.fromisoformat(result["timestamp"].replace('Z', '+00:00'))

@pytest.mark.asyncio
async def test_execute_fetch_error(agent_config):
    """Test execution handling of fetch errors"""
    agent = DataAgent(agent_config["data_agent"])
    test_url = "https://test.api/insider-trades"
    
    with aioresponses() as mocked:
        mocked.get(
            test_url,
            status=500,
            body="Internal Server Error"
        )
        
        result = await agent.execute(
            api_key="test_key",
            endpoint=test_url
        )
        
        assert result["status"] == "error"
        assert "error" in result
        assert "timestamp" in result

@pytest.mark.asyncio
async def test_cleanup(agent_config):
    """Test cleanup of data agent resources"""
    agent = DataAgent(agent_config["data_agent"])
    
    # Add some test data to cleanup
    agent.validation_status = {
        "reasoning": ["test"],
        "actions": ["test"]
    }
    
    # Create a session to clean up
    await agent._init_session()
    assert agent.session is not None
    
    # Cleanup
    agent.cleanup()
    await asyncio.sleep(0.1)  # Give time for session cleanup
    
    assert agent.validation_status == {"reasoning": [], "actions": []}
    assert agent.progress_tracker == {"current_step": 0, "total_steps": 0, "status": ""}
    assert agent.session is None or agent.session.closed

@pytest.mark.asyncio
async def test_session_management(agent_config):
    """Test session initialization and cleanup"""
    agent = DataAgent(agent_config["data_agent"])
    
    # Test session initialization
    await agent._init_session()
    assert agent.session is not None
    assert not agent.session.closed
    
    # Test session cleanup
    await agent._close_session()
    assert agent.session.closed

@pytest.mark.asyncio
async def test_session_reuse(agent_config, sample_trade_data):
    """Test session reuse for multiple requests"""
    agent = DataAgent(agent_config["data_agent"])
    test_url = "https://test.api/insider-trades"
    
    with aioresponses() as mocked:
        mocked.get(
            test_url,
            status=200,
            payload=sample_trade_data
        )
        mocked.get(
            test_url,
            status=200,
            payload=sample_trade_data
        )
        
        # First request should create session
        await agent.fetch_data("test_key", test_url)
        original_session = agent.session
        
        # Second request should reuse session
        await agent.fetch_data("test_key", test_url)
        assert agent.session is original_session
        
        # Cleanup
        await agent._close_session()