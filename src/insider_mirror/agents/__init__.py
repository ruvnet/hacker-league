"""
Agent modules for the Insider Trading Mirror System.
Each agent is responsible for a specific aspect of the system:
- DataAgent: Fetches and validates insider trading data
- AnalysisAgent: Analyzes and filters significant trades
- TradingAgent: Executes trades with risk management
- ReportingAgent: Generates performance reports
"""

from .base_agent import BaseAgent
from .data_agent import DataAgent
from .analysis_agent import AnalysisAgent
from .trading_agent import TradingAgent
from .reporting_agent import ReportingAgent

__all__ = [
    'BaseAgent',
    'DataAgent',
    'AnalysisAgent',
    'TradingAgent',
    'ReportingAgent'
]