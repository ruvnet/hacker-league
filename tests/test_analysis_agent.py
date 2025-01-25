"""Tests for the analysis agent."""

import pytest
from datetime import datetime, timezone
import pandas as pd
from insider_mirror.agents.analysis_agent import AnalysisAgent

@pytest.mark.asyncio
async def test_analysis_agent_initialization(agent_config):
    """Test AnalysisAgent initialization"""
    agent = AnalysisAgent(agent_config["analysis_agent"])
    assert agent.name == "analysis_agent"
    assert agent.config == agent_config["analysis_agent"]

def test_convert_to_dataframe(agent_config, sample_trade_data):
    """Test conversion of trade data to DataFrame"""
    agent = AnalysisAgent(agent_config["analysis_agent"])
    df = agent.convert_to_dataframe(sample_trade_data)
    assert isinstance(df, pd.DataFrame)
    assert 'filing_date' in df.columns
    assert pd.api.types.is_datetime64_any_dtype(df['filing_date'])

def test_filter_significant_trades(agent_config, sample_trade_data):
    """Test trade filtering based on significance"""
    agent = AnalysisAgent(agent_config["analysis_agent"])
    filtered = agent.filter_significant_trades(sample_trade_data)
    assert isinstance(filtered, list)
    assert len(filtered) <= len(sample_trade_data)

def test_analyze_patterns(agent_config, sample_trade_data):
    """Test pattern analysis"""
    agent = AnalysisAgent(agent_config["analysis_agent"])
    patterns = agent.analyze_patterns(sample_trade_data)
    assert isinstance(patterns, dict)
    assert "time_patterns" in patterns
    assert "symbol_patterns" in patterns

def test_analyze_clusters(agent_config, sample_trade_data):
    """Test trade clustering analysis"""
    agent = AnalysisAgent(agent_config["analysis_agent"])
    clusters = agent.analyze_clusters(sample_trade_data)
    assert isinstance(clusters, dict)
    assert "time_clusters" in clusters

def test_analyze_trends(agent_config, sample_trade_data):
    """Test trend analysis"""
    agent = AnalysisAgent(agent_config["analysis_agent"])
    trends = agent.analyze_trends(sample_trade_data)
    assert isinstance(trends, dict)
    assert "daily_trends" in trends
    assert "moving_averages" in trends

def test_analyze_correlations(agent_config, sample_trade_data):
    """Test correlation analysis"""
    agent = AnalysisAgent(agent_config["analysis_agent"])
    correlations = agent.analyze_correlations(sample_trade_data)
    assert isinstance(correlations, dict)
    assert "metric_correlations" in correlations

def test_calculate_risk_metrics(agent_config, sample_trade_data):
    """Test risk metrics calculation"""
    agent = AnalysisAgent(agent_config["analysis_agent"])
    metrics = agent.calculate_risk_metrics(sample_trade_data)
    assert isinstance(metrics, dict)
    assert "var_95" in metrics
    assert "var_99" in metrics
    assert "symbol_concentration" in metrics

@pytest.mark.asyncio
async def test_execute_success(agent_config, sample_trade_data):
    """Test successful execution of analysis agent"""
    agent = AnalysisAgent(agent_config["analysis_agent"])
    result = await agent.execute(sample_trade_data)
    
    assert result["status"] == "success"
    assert "timestamp" in result
    assert "filtered_trades" in result
    assert "patterns" in result
    assert "risk_metrics" in result

@pytest.mark.asyncio
async def test_execute_error_handling(agent_config):
    """Test error handling during execution"""
    agent = AnalysisAgent(agent_config["analysis_agent"])
    
    # Test with invalid data
    invalid_data = [{"invalid": "data"}]
    result = await agent.execute(invalid_data)
    
    assert result["status"] == "error"
    assert "error" in result
    assert "timestamp" in result

def test_cleanup(agent_config):
    """Test cleanup of agent resources"""
    agent = AnalysisAgent(agent_config["analysis_agent"])
    agent.cleanup()
    assert agent.validation_status == {"reasoning": [], "actions": []}