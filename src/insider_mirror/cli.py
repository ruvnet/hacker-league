"""Command-line interface for the Insider Trading Mirror System."""

import argparse
import asyncio
import os
import sys
from typing import Optional, List
from .crew import InsiderMirrorCrew

class InsiderMirrorCLI:
    """Command-line interface for the system"""
    
    def __init__(self):
        self.crew = InsiderMirrorCrew()
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create and configure argument parser"""
        parser = argparse.ArgumentParser(
            description="Insider Trading Mirror System CLI",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Fetch latest insider trading data
  insider-mirror data fetch --limit 100
  
  # Analyze trades with specific criteria
  insider-mirror analyze trades --min-value 100000
  
  # Execute trades in paper trading mode
  insider-mirror trade execute --mode paper
  
  # Generate HTML report
  insider-mirror report generate --format html
  
  # Run the complete system
  insider-mirror run --interval 3600
            """
        )
        
        subparsers = parser.add_subparsers(dest="command", help="Available commands")
        
        # Data Management
        data_parser = subparsers.add_parser("data", help="Data management commands")
        data_subparsers = data_parser.add_subparsers(dest="subcommand")
        
        # data fetch
        fetch_parser = data_subparsers.add_parser("fetch", help="Fetch insider trading data")
        fetch_parser.add_argument("--limit", type=int, default=50, help="Max records to fetch")
        
        # data validate
        validate_parser = data_subparsers.add_parser("validate", help="Validate existing data")
        validate_parser.add_argument("--strict", action="store_true", help="Use strict validation")
        
        # Analysis
        analysis_parser = subparsers.add_parser("analyze", help="Analysis commands")
        analysis_subparsers = analysis_parser.add_subparsers(dest="subcommand")
        
        # analyze trades
        trades_parser = analysis_subparsers.add_parser("trades", help="Analyze trades")
        trades_parser.add_argument("--min-value", type=int, help="Minimum trade value")
        trades_parser.add_argument("--min-shares", type=int, help="Minimum shares")
        
        # analyze risks
        risks_parser = analysis_subparsers.add_parser("risks", help="Analyze risks")
        risks_parser.add_argument("--symbol", help="Focus on specific symbol")
        
        # Trading
        trading_parser = subparsers.add_parser("trade", help="Trading commands")
        trading_subparsers = trading_parser.add_subparsers(dest="subcommand")
        
        # trade execute
        execute_parser = trading_subparsers.add_parser("execute", help="Execute trades")
        execute_parser.add_argument(
            "--mode", 
            choices=["paper", "live"], 
            default="paper",
            help="Trading mode"
        )
        
        # trade status
        status_parser = trading_subparsers.add_parser("status", help="Check trade status")
        
        # Reporting
        report_parser = subparsers.add_parser("report", help="Reporting commands")
        report_subparsers = report_parser.add_subparsers(dest="subcommand")
        
        # report generate
        generate_parser = report_subparsers.add_parser("generate", help="Generate reports")
        generate_parser.add_argument(
            "--format",
            choices=["html", "csv"],
            default="html",
            help="Report format"
        )
        
        # report metrics
        metrics_parser = report_subparsers.add_parser("metrics", help="Show metrics")
        
        # System
        run_parser = subparsers.add_parser("run", help="Run the complete system")
        run_parser.add_argument(
            "--interval",
            type=int,
            default=3600,
            help="Update interval in seconds"
        )
        
        return parser

    async def handle_data(self, args: argparse.Namespace) -> None:
        """Handle data management commands"""
        if args.subcommand == "fetch":
            result = await self.crew.data_agent.execute(
                api_key=os.environ.get("FINNHUB_API_KEY"),
                endpoint=os.environ.get("FINNHUB_ENDPOINT")
            )
            
            if result["status"] == "success":
                print(f"Successfully fetched {len(result['data'])} records")
            else:
                print(f"Error: {result.get('error')}")
                sys.exit(1)
                
        elif args.subcommand == "validate":
            # Implementation for validate command
            pass

    async def handle_analysis(self, args: argparse.Namespace) -> None:
        """Handle analysis commands"""
        if args.subcommand == "trades":
            # Get data first
            data_result = await self.crew.data_agent.execute(
                api_key=os.environ.get("FINNHUB_API_KEY"),
                endpoint=os.environ.get("FINNHUB_ENDPOINT")
            )
            
            if data_result["status"] != "success":
                print(f"Error fetching data: {data_result.get('error')}")
                sys.exit(1)
            
            # Analyze trades
            result = await self.crew.analysis_agent.execute(trades=data_result["data"])
            
            if result["status"] == "success":
                print(f"""
Analysis Results:
- Input Trades: {len(data_result['data'])}
- Filtered Trades: {len(result['filtered_trades'])}
- Risk Metrics: {result.get('risk_metrics', {})}
""")
            else:
                print(f"Error: {result.get('error')}")
                sys.exit(1)
                
        elif args.subcommand == "risks":
            # Implementation for risks command
            pass

    async def handle_trading(self, args: argparse.Namespace) -> None:
        """Handle trading commands"""
        if args.subcommand == "execute":
            # Get analyzed trades first
            data_result = await self.crew.data_agent.execute(
                api_key=os.environ.get("FINNHUB_API_KEY"),
                endpoint=os.environ.get("FINNHUB_ENDPOINT")
            )
            
            if data_result["status"] != "success":
                print(f"Error fetching data: {data_result.get('error')}")
                sys.exit(1)
            
            analysis_result = await self.crew.analysis_agent.execute(
                trades=data_result["data"]
            )
            
            if analysis_result["status"] != "success":
                print(f"Error analyzing trades: {analysis_result.get('error')}")
                sys.exit(1)
            
            # Execute trades
            if analysis_result["filtered_trades"]:
                result = await self.crew.trading_agent.execute(
                    trades=analysis_result["filtered_trades"],
                    portfolio_value=float(os.environ.get("INITIAL_PORTFOLIO_VALUE", "100000"))
                )
                
                if result["status"] == "success":
                    print(f"""
Trading Results:
- Executions: {len(result['executions'])}
- Portfolio Value: ${result['portfolio']['total_value']:,.2f}
- Position Count: {result['portfolio']['position_count']}
""")
                else:
                    print(f"Error: {result.get('error')}")
                    sys.exit(1)
            else:
                print("No trades to execute")
                
        elif args.subcommand == "status":
            portfolio = self.crew.trading_agent.get_portfolio_summary()
            print(f"""
Portfolio Status:
- Total Value: ${portfolio['total_value']:,.2f}
- Positions: {portfolio['position_count']}
- Daily Trades: {portfolio['daily_trades']}
- Daily P&L: ${portfolio['daily_pnl']:,.2f}
""")

    async def handle_reporting(self, args: argparse.Namespace) -> None:
        """Handle reporting commands"""
        if args.subcommand == "generate":
            # Get trading results first
            portfolio = self.crew.trading_agent.get_portfolio_summary()
            
            result = await self.crew.reporting_agent.execute(
                trades=self.crew.trading_agent.daily_trades,
                portfolio_summary=portfolio
            )
            
            if result["status"] == "success":
                print(f"""
Report Generation Complete:
- Generated Reports: {', '.join(result['reports'].keys())}
- Metrics Calculated: {len(result['metrics'])}
- Report Locations:
  {chr(10).join(f'  - {format}: {path}' for format, path in result['reports'].items())}
""")
            else:
                print(f"Error: {result.get('error')}")
                sys.exit(1)
                
        elif args.subcommand == "metrics":
            portfolio = self.crew.trading_agent.get_portfolio_summary()
            print(f"""
Current Metrics:
- Portfolio Value: ${portfolio['total_value']:,.2f}
- Daily P&L: ${portfolio['daily_pnl']:,.2f}
- Position Count: {portfolio['position_count']}
- Daily Trades: {portfolio['daily_trades']}
""")

    async def run(self, args: argparse.Namespace) -> None:
        """Run the complete system"""
        await self.crew.start(interval_seconds=args.interval)

    def execute(self) -> None:
        """Execute CLI command"""
        try:
            args = self.parser.parse_args()
            
            if not args.command:
                self.parser.print_help()
                return
            
            try:
                if args.command == "data":
                    asyncio.run(self.handle_data(args))
                elif args.command == "analyze":
                    asyncio.run(self.handle_analysis(args))
                elif args.command == "trade":
                    asyncio.run(self.handle_trading(args))
                elif args.command == "report":
                    asyncio.run(self.handle_reporting(args))
                elif args.command == "run":
                    asyncio.run(self.run(args))
                
            except KeyboardInterrupt:
                print("\nOperation cancelled by user")
                return
            except Exception as e:
                print(f"Error: {str(e)}")
                sys.exit(1)
                
        except SystemExit as e:
            # Re-raise SystemExit with code 1 for errors
            if e.code != 0:
                sys.exit(1)
            raise