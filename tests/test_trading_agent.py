"""Tests for the trading agent."""

import pytest
from datetime import datetime, timezone
from insider_mirror.agents.trading_agent import TradingAgent

@pytest.mark.asyncio
async def test_trading_agent_initialization(agent_config):
    """Test TradingAgent initialization"""
    agent = TradingAgent(agent_config["trading_agent"])
    assert agent.name == "trading_agent"
    assert agent.config == agent_config["trading_agent"]
    assert agent.positions == {}
    assert agent.daily_trades == []
    assert agent.daily_pnl == 0.0

def test_check_risk_limits_position_size(agent_config):
    """Test position size risk limit checking"""
    agent = TradingAgent(agent_config["trading_agent"])
    portfolio_value = 100000
    
    # Test trade within limits (5% of portfolio = $5000)
    trade = {
        "symbol": "AAPL",
        "shares": 30,
        "price": 150.0,  # Total value = $4500
        "transaction_type": "PURCHASE"
    }
    result, message = agent.check_risk_limits(trade, portfolio_value)
    assert result is True
    assert message is None
    
    # Test trade exceeding position size limit
    trade = {
        "symbol": "AAPL",
        "shares": 100,
        "price": 150.0,  # Total value = $15000
        "transaction_type": "PURCHASE"
    }
    result, message = agent.check_risk_limits(trade, portfolio_value)
    assert result is False
    assert "Position size" in message

def test_check_risk_limits_daily_trades(agent_config):
    """Test daily trade limit checking"""
    agent = TradingAgent(agent_config["trading_agent"])
    portfolio_value = 100000
    
    # Add maximum allowed daily trades
    max_trades = agent.risk_config["max_daily_trades"]
    agent.daily_trades = [{"id": i} for i in range(max_trades)]
    
    trade = {
        "symbol": "AAPL",
        "shares": 30,
        "price": 150.0,
        "transaction_type": "PURCHASE"
    }
    result, message = agent.check_risk_limits(trade, portfolio_value)
    assert result is False
    assert "Daily trade limit" in message

def test_check_risk_limits_concentration(agent_config):
    """Test position concentration limit checking"""
    agent = TradingAgent(agent_config["trading_agent"])
    portfolio_value = 100000
    
    # Add existing position at 15% concentration
    agent.positions["AAPL"] = {
        "shares": 100,
        "value": 15000.0
    }
    
    # Test trade that would exceed concentration limit
    trade = {
        "symbol": "AAPL",
        "shares": 50,
        "price": 150.0,  # Would add $7500 to position
        "transaction_type": "PURCHASE"
    }
    result, message = agent.check_risk_limits(trade, portfolio_value)
    assert result is False
    assert "Symbol concentration" in message

def test_update_position_new_position(agent_config):
    """Test position update for new position"""
    agent = TradingAgent(agent_config["trading_agent"])
    
    trade = {
        "symbol": "AAPL",
        "shares": 100,
        "price": 150.0,
        "transaction_type": "PURCHASE"
    }
    agent.update_position(trade)
    assert "AAPL" in agent.positions
    assert agent.positions["AAPL"]["value"] == 15000.0
    assert agent.positions["AAPL"]["shares"] == 100

def test_update_position_existing_position(agent_config):
    """Test position update for existing position"""
    agent = TradingAgent(agent_config["trading_agent"])
    
    # Add initial position
    agent.positions["AAPL"] = {
        "shares": 100,
        "value": 15000.0
    }
    
    # Add to position
    trade = {
        "symbol": "AAPL",
        "shares": 50,
        "price": 160.0,
        "transaction_type": "PURCHASE"
    }
    agent.update_position(trade)
    assert agent.positions["AAPL"]["shares"] == 150
    assert agent.positions["AAPL"]["value"] == 24000.0

def test_update_position_full_sale(agent_config):
    """Test position update for complete position sale"""
    agent = TradingAgent(agent_config["trading_agent"])
    
    # Add initial position
    agent.positions["AAPL"] = {
        "shares": 100,
        "value": 15000.0
    }
    
    # Sell entire position
    trade = {
        "symbol": "AAPL",
        "shares": 100,
        "price": 160.0,
        "transaction_type": "SALE"
    }
    agent.update_position(trade)
    assert "AAPL" not in agent.positions

@pytest.mark.asyncio
async def test_execute_trade_success(agent_config):
    """Test successful trade execution"""
    agent = TradingAgent(agent_config["trading_agent"])
    portfolio_value = 100000
    
    trade = {
        "symbol": "AAPL",
        "shares": 30,  # Small enough to pass risk limits
        "price": 150.0,
        "transaction_type": "PURCHASE"
    }
    result = await agent.execute_trade(trade, portfolio_value)
    assert result["status"] == "executed"
    assert "trade" in result
    assert "timestamp" in result

@pytest.mark.asyncio
async def test_execute_trade_rejection(agent_config):
    """Test trade rejection due to risk limits"""
    agent = TradingAgent(agent_config["trading_agent"])
    portfolio_value = 100000
    
    # Add maximum daily trades
    max_trades = agent.risk_config["max_daily_trades"]
    agent.daily_trades = [{"id": i} for i in range(max_trades)]
    
    trade = {
        "symbol": "AAPL",
        "shares": 100,
        "price": 150.0,
        "transaction_type": "PURCHASE"
    }
    result = await agent.execute_trade(trade, portfolio_value)
    assert result["status"] == "rejected"
    assert "reason" in result

def test_get_portfolio_summary(agent_config):
    """Test portfolio summary generation"""
    agent = TradingAgent(agent_config["trading_agent"])
    
    # Add some positions
    agent.positions["AAPL"] = {
        "shares": 100,
        "value": 15000.0
    }
    agent.positions["MSFT"] = {
        "shares": 50,
        "value": 10000.0
    }
    
    agent.daily_trades = [{"id": 1}, {"id": 2}]
    agent.daily_pnl = 1000.0
    
    summary = agent.get_portfolio_summary()
    assert summary["total_value"] == 25000.0
    assert summary["position_count"] == 2
    assert summary["daily_trades"] == 2
    assert summary["daily_pnl"] == 1000.0

@pytest.mark.asyncio
async def test_execute_success(agent_config, sample_trade_data):
    """Test successful execution of trading agent"""
    agent = TradingAgent(agent_config["trading_agent"])
    portfolio_value = 100000
    
    # Modify sample trades to pass risk limits
    modified_trades = []
    for trade in sample_trade_data:
        modified_trade = trade.copy()
        modified_trade["shares"] = 30  # Small enough to pass risk limits
        modified_trades.append(modified_trade)
    
    result = await agent.execute(modified_trades, portfolio_value)
    assert result["status"] == "success"
    assert "timestamp" in result
    assert "executions" in result
    assert "portfolio" in result

@pytest.mark.asyncio
async def test_execute_error_handling(agent_config):
    """Test error handling during execution"""
    agent = TradingAgent(agent_config["trading_agent"])
    
    # Test with invalid data
    invalid_data = [{"invalid": "data"}]
    result = await agent.execute(invalid_data, 100000)
    
    assert result["status"] == "error"
    assert "error" in result
    assert "timestamp" in result

def test_reset_daily_tracking(agent_config):
    """Test reset of daily tracking metrics"""
    agent = TradingAgent(agent_config["trading_agent"])
    
    # Add some daily tracking data
    agent.daily_trades = [{"id": 1}, {"id": 2}]
    agent.daily_pnl = 1000.0
    
    agent.reset_daily_tracking()
    assert agent.daily_trades == []
    assert agent.daily_pnl == 0.0