"""Tests for the CLI interface."""

import pytest
import argparse
import os
import sys
from unittest.mock import patch, Mock, AsyncMock
from insider_mirror.cli import InsiderMirrorCLI

@pytest.fixture
def cli():
    """Create a test instance of InsiderMirrorCLI"""
    return InsiderMirrorCLI()

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

def test_cli_initialization(cli):
    """Test CLI initialization"""
    assert isinstance(cli.parser, argparse.ArgumentParser)
    assert hasattr(cli, 'crew')

def test_parser_commands(cli):
    """Test parser command configuration"""
    # Get all subparsers
    subparsers = cli.parser._subparsers._group_actions[0].choices
    
    # Check main commands
    assert "data" in subparsers
    assert "analyze" in subparsers
    assert "trade" in subparsers
    assert "report" in subparsers
    assert "run" in subparsers

def test_data_command_options(cli):
    """Test data command options"""
    args = cli.parser.parse_args(['data', 'fetch', '--limit', '100'])
    assert args.command == "data"
    assert args.subcommand == "fetch"
    assert args.limit == 100
    
    args = cli.parser.parse_args(['data', 'validate', '--strict'])
    assert args.command == "data"
    assert args.subcommand == "validate"
    assert args.strict is True

def test_analyze_command_options(cli):
    """Test analyze command options"""
    args = cli.parser.parse_args(['analyze', 'trades', '--min-value', '100000'])
    assert args.command == "analyze"
    assert args.subcommand == "trades"
    assert args.min_value == 100000
    
    args = cli.parser.parse_args(['analyze', 'risks', '--symbol', 'AAPL'])
    assert args.command == "analyze"
    assert args.subcommand == "risks"
    assert args.symbol == "AAPL"

def test_trade_command_options(cli):
    """Test trade command options"""
    args = cli.parser.parse_args(['trade', 'execute', '--mode', 'paper'])
    assert args.command == "trade"
    assert args.subcommand == "execute"
    assert args.mode == "paper"
    
    args = cli.parser.parse_args(['trade', 'status'])
    assert args.command == "trade"
    assert args.subcommand == "status"

def test_report_command_options(cli):
    """Test report command options"""
    args = cli.parser.parse_args(['report', 'generate', '--format', 'html'])
    assert args.command == "report"
    assert args.subcommand == "generate"
    assert args.format == "html"
    
    args = cli.parser.parse_args(['report', 'metrics'])
    assert args.command == "report"
    assert args.subcommand == "metrics"

def test_run_command_options(cli):
    """Test run command options"""
    args = cli.parser.parse_args(['run', '--interval', '1800'])
    assert args.command == "run"
    assert args.interval == 1800

@pytest.mark.asyncio
async def test_handle_data_fetch(cli, mock_env_vars, sample_trade_data):
    """Test data fetch command handling"""
    args = cli.parser.parse_args(['data', 'fetch', '--limit', '100'])
    
    mock_result = {
        "status": "success",
        "data": sample_trade_data
    }
    
    with patch.object(cli.crew.data_agent, 'execute', AsyncMock(return_value=mock_result)):
        await cli.handle_data(args)

@pytest.mark.asyncio
async def test_handle_analysis_trades(cli, mock_env_vars, sample_trade_data):
    """Test trade analysis command handling"""
    args = cli.parser.parse_args(['analyze', 'trades', '--min-value', '100000'])
    
    mock_data_result = {
        "status": "success",
        "data": sample_trade_data
    }
    
    mock_analysis_result = {
        "status": "success",
        "filtered_trades": sample_trade_data[:1],
        "risk_metrics": {"test": "metrics"}
    }
    
    with patch.object(cli.crew.data_agent, 'execute', AsyncMock(return_value=mock_data_result)), \
         patch.object(cli.crew.analysis_agent, 'execute', AsyncMock(return_value=mock_analysis_result)):
        await cli.handle_analysis(args)

@pytest.mark.asyncio
async def test_handle_trading_execute(cli, mock_env_vars, sample_trade_data):
    """Test trade execution command handling"""
    args = cli.parser.parse_args(['trade', 'execute', '--mode', 'paper'])
    
    mock_data_result = {
        "status": "success",
        "data": sample_trade_data
    }
    
    mock_analysis_result = {
        "status": "success",
        "filtered_trades": sample_trade_data[:1]
    }
    
    mock_trading_result = {
        "status": "success",
        "executions": [{"trade": "details"}],
        "portfolio": {
            "total_value": 110000,
            "position_count": 1
        }
    }
    
    with patch.object(cli.crew.data_agent, 'execute', AsyncMock(return_value=mock_data_result)), \
         patch.object(cli.crew.analysis_agent, 'execute', AsyncMock(return_value=mock_analysis_result)), \
         patch.object(cli.crew.trading_agent, 'execute', AsyncMock(return_value=mock_trading_result)):
        await cli.handle_trading(args)

@pytest.mark.asyncio
async def test_handle_reporting_generate(cli):
    """Test report generation command handling"""
    args = cli.parser.parse_args(['report', 'generate', '--format', 'html'])
    
    mock_portfolio = {
        "total_value": 110000,
        "position_count": 1,
        "daily_trades": 5,
        "daily_pnl": 1000
    }
    
    mock_report_result = {
        "status": "success",
        "metrics": {"test": "metrics"},
        "reports": {"html": "report.html"}
    }
    
    with patch.object(cli.crew.trading_agent, 'get_portfolio_summary', return_value=mock_portfolio), \
         patch.object(cli.crew.reporting_agent, 'execute', AsyncMock(return_value=mock_report_result)):
        await cli.handle_reporting(args)

@pytest.mark.asyncio
async def test_handle_run_command(cli):
    """Test run command handling"""
    args = cli.parser.parse_args(['run', '--interval', '1800'])
    
    with patch.object(cli.crew, 'start', AsyncMock()) as mock_start:
        await cli.run(args)
        mock_start.assert_called_once_with(interval_seconds=1800)

def test_execute_no_command(cli, capsys):
    """Test CLI execution with no command"""
    with patch('sys.argv', ['insider-mirror']):
        cli.execute()
        captured = capsys.readouterr()
        assert "usage:" in captured.out

def test_execute_keyboard_interrupt(cli):
    """Test CLI handling of keyboard interrupt"""
    with patch.object(cli.parser, 'parse_args', return_value=Mock(command='run')), \
         patch.object(cli, 'run', AsyncMock(side_effect=KeyboardInterrupt)), \
         patch('sys.exit') as mock_exit:
        cli.execute()
        mock_exit.assert_not_called()

def test_execute_error(cli):
    """Test CLI error handling"""
    with patch.object(cli.parser, 'parse_args', return_value=Mock(command='data', subcommand='fetch')), \
         patch.object(cli, 'handle_data', AsyncMock(side_effect=Exception("Test error"))), \
         patch('sys.exit') as mock_exit:
        cli.execute()
        mock_exit.assert_called_once_with(1)

def test_execute_command_chain(cli, mock_env_vars, sample_trade_data):
    """Test execution of multiple commands in sequence"""
    # Mock all agent responses
    mock_data_result = {"status": "success", "data": sample_trade_data}
    mock_analysis_result = {"status": "success", "filtered_trades": sample_trade_data[:1]}
    mock_trading_result = {
        "status": "success",
        "executions": [{"trade": "details"}],
        "portfolio": {
            "total_value": 110000,
            "position_count": 1
        }
    }
    mock_report_result = {
        "status": "success",
        "metrics": {
            "win_rate": 0.65,
            "profit_factor": 2.1,
            "sharpe_ratio": 1.5,
            "max_drawdown": 5000.0
        },
        "reports": {"html": "report.html"}
    }
    
    with patch.object(cli.crew.data_agent, 'execute', AsyncMock(return_value=mock_data_result)), \
         patch.object(cli.crew.analysis_agent, 'execute', AsyncMock(return_value=mock_analysis_result)), \
         patch.object(cli.crew.trading_agent, 'execute', AsyncMock(return_value=mock_trading_result)), \
         patch.object(cli.crew.reporting_agent, 'execute', AsyncMock(return_value=mock_report_result)), \
         patch.object(cli.parser, 'parse_args') as mock_parse_args:
        
        # Run fetch -> analyze -> trade -> report sequence
        mock_parse_args.side_effect = [
            Mock(command='data', subcommand='fetch'),
            Mock(command='analyze', subcommand='trades'),
            Mock(command='trade', subcommand='execute', mode='paper'),
            Mock(command='report', subcommand='generate')
        ]
        
        cli.execute()  # data fetch
        cli.execute()  # analyze trades
        cli.execute()  # trade execute
        cli.execute()  # report generate