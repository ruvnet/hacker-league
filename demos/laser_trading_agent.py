"""Demo agent that implements the LASER trading strategy using Finnhub and OpenRouter."""

import asyncio
import logging
import aiohttp
import json
import os
import ssl
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ANSI color codes for formatted output
CYAN = '\033[0;36m'
GREEN = '\033[0;32m'
NC = '\033[0m'  # No Color

class LaserTradingAgent:
    """Agent that implements the LASER trading strategy using Finnhub data."""

    def __init__(self, config: Dict[str, Any]):
        self.log = logging.getLogger("demos.laser_trading_agent")
        self.name = "laser_trading_agent"
        self.config = config
        self.session = None

    async def _init_session(self) -> None:
        """Initialize aiohttp session with SSL context"""
        if self.session is None or self.session.closed:
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = True
            ssl_context.verify_mode = ssl.CERT_REQUIRED
            
            timeout = aiohttp.ClientTimeout(total=30)
            connector = aiohttp.TCPConnector(ssl=ssl_context)
            self.session = aiohttp.ClientSession(
                connector=connector,
                timeout=timeout
            )

    async def _close_session(self) -> None:
        """Close aiohttp session"""
        if self.session and not self.session.closed:
            await self.session.close()

    async def _fetch_insider_trades(self, symbol: str) -> Dict[str, Any]:
        """Fetch insider trading data from Finnhub API"""
        try:
            await self._init_session()
            
            api_key = os.getenv("FINNHUB_API_KEY")
            if not api_key:
                raise ValueError("FINNHUB_API_KEY environment variable is required")
            
            headers = {
                "X-Finnhub-Token": api_key
            }
            
            # Fetch insider transactions with from/to dates
            from_date = (datetime.now(timezone.utc) - timedelta(days=30)).strftime("%Y-%m-%d")
            to_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            
            self.log.info(f"Fetching insider transactions for {symbol}")
            async with self.session.get(
                f"https://finnhub.io/api/v1/stock/insider-transactions",
                params={
                    "symbol": symbol,
                    "from": from_date,
                    "to": to_date
                },
                headers=headers
            ) as response:
                if response.status == 200:
                    transactions_data = await response.json()
                else:
                    error_text = await response.text()
                    raise RuntimeError(f"Insider transactions API error: {error_text}")
            
            # Fetch company profile for additional context
            self.log.info(f"Fetching company profile for {symbol}")
            async with self.session.get(
                f"https://finnhub.io/api/v1/stock/profile2?symbol={symbol}",
                headers=headers
            ) as response:
                if response.status == 200:
                    profile_data = await response.json()
                else:
                    error_text = await response.text()
                    raise RuntimeError(f"Profile API error: {error_text}")
            
            # Combine data
            return {
                "data": transactions_data.get("data", []),
                "profile": profile_data
            }
            
        except Exception as e:
            self.log.error(f"Error fetching insider trades: {str(e)}")
            raise
            
        finally:
            await self._close_session()

    async def _analyze_trades(self, trades_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze insider trades using LASER strategy and OpenRouter"""
        try:
            trades = trades_data.get("data", [])
            profile = trades_data.get("profile", {})
            
            # Format data for analysis
            system_prompt = """You are an expert in analyzing insider trading patterns using the LASER methodology.
Follow this structure:

[THOUGHT] First, analyze the insider trading patterns and company context
[ACTION] Apply LASER strategy filters and identify significant trades
[OBSERVATION] Document key findings and patterns
[REFLECTION] Synthesize insights and trading signals

Format your response using these sections clearly."""

            # Prepare trade summary
            trade_summary = []
            for trade in trades[:5]:  # Summarize recent trades
                trade_summary.append(f"""
Trade: {trade.get('transactionShares', 0):,} shares @ ${trade.get('transactionPrice', 0):.2f}
Type: {trade.get('transactionType', 'Unknown')}
Value: ${trade.get('transactionShares', 0) * trade.get('transactionPrice', 0):,.2f}
Filing Date: {trade.get('filingDate', 'Unknown')}
""")

            user_prompt = f"""Analyze these insider trades for {profile.get('name', 'Unknown')} ({profile.get('ticker', 'Unknown')}):

Company Profile:
• Industry: {profile.get('finnhubIndustry', 'Unknown')}
• Market Cap: ${profile.get('marketCapitalization', 0):,.2f}M
• Exchange: {profile.get('exchange', 'Unknown')}

Recent Insider Trades:
{''.join(trade_summary)}

Total Trades: {len(trades)}

Apply LASER strategy to identify significant trading patterns and generate trading signals."""

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            # Get analysis from OpenRouter
            api_key = os.getenv("OPENROUTER_API_KEY")
            if not api_key:
                raise ValueError("OPENROUTER_API_KEY environment variable is required")
            
            await self._init_session()
            
            # Configure enterprise-grade connection parameters
            connector = aiohttp.TCPConnector(
                ssl=ssl.create_default_context(),
                limit=100,
                limit_per_host=20,
                use_dns_cache=True
            )
            
            async with aiohttp.ClientSession(
                connector=connector,
                timeout=aiohttp.ClientTimeout(total=45)
            ) as session:
                async with session.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "http://localhost:3000",
                        "X-Title": "Insider Mirror System"
                    },
                    json={
                        "model": "anthropic/claude-2",
                        "messages": messages,
                        "stream": True,
                        "temperature": 0.7
                    },
                    timeout=None
                ) as response:
                    full_response = ""
                    async for line in response.content:
                        if line:
                            try:
                                line_str = line.decode('utf-8')
                                if line_str.startswith('data: '):
                                    chunk_data = json.loads(line_str[6:])
                                    if chunk_data != '[DONE]':
                                        if 'choices' in chunk_data and len(chunk_data['choices']) > 0:
                                            delta = chunk_data['choices'][0].get('delta', {})
                                            if 'content' in delta:
                                                content = delta['content']
                                                print(content, end='', flush=True)
                                                full_response += content
                            except (json.JSONDecodeError, UnicodeDecodeError):
                                continue
                    
                    analysis = full_response
            
            # Apply LASER filters
            filtered_trades = []
            for trade in trades:
                # Check for large trades
                if trade.get("transactionShares", 0) * trade.get("transactionPrice", 0) > 100000:
                    # Check for aligned sentiment
                    if len([t for t in trades if t["transactionType"] == trade["transactionType"]]) >= 3:
                        filtered_trades.append(trade)
            
            return {
                "status": "success",
                "filtered_trades": filtered_trades,
                "total_trades": len(trades),
                "filtered_count": len(filtered_trades),
                "analysis": analysis
            }
            
        except Exception as e:
            self.log.error(f"Error analyzing trades: {str(e)}")
            raise

    async def execute(self, symbol: str) -> Dict[str, Any]:
        """Execute LASER trading strategy"""
        try:
            print(f"""
╔══════════════════════════════════════════════════════════════════╗
║  🚀 LASER TRADING SYSTEM v1.0
║     ANALYZING {symbol}...
╚══════════════════════════════════════════════════════════════════╝

{CYAN}▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
📡 FETCHING INSIDER DATA
🧮 LASER STRATEGY: ACTIVE
💹 TRADE EXECUTION: READY
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀{NC}
""")
            # Step 1: Fetch Data
            print(f"{GREEN}[LASER] Phase 1: Data Collection{NC}")
            trades_data = await self._fetch_insider_trades(symbol)
            print("✅ Insider trading data retrieved\n")
            
            # Step 2: Analysis with LASER and OpenRouter
            print(f"{GREEN}[LASER] Phase 2: Neural Analysis{NC}")
            print("🧠 Initializing LASER analysis framework...")
            analysis = await self._analyze_trades(trades_data)
            print("\n✅ Analysis complete\n")
            
            # Step 3: Generate Results
            result = {
                "status": "success",
                "data": {
                    "symbol": symbol,
                    "company": trades_data["profile"].get("name", "Unknown"),
                    "total_trades": analysis["total_trades"],
                    "filtered_trades": analysis["filtered_trades"],
                    "filtered_count": analysis["filtered_count"],
                    "profile": {
                        "industry": trades_data["profile"].get("finnhubIndustry", "Unknown"),
                        "market_cap": trades_data["profile"].get("marketCapitalization", 0),
                        "exchange": trades_data["profile"].get("exchange", "Unknown")
                    },
                    "analysis": analysis["analysis"]
                },
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            print(f"""
{CYAN}▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
✨ ANALYSIS COMPLETE
📊 SIGNALS GENERATED
🎯 READY FOR EXECUTION
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀{NC}
""")
            return result
            
        except Exception as e:
            self.log.error(f"Error executing LASER strategy: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

    def format_output(self, result: Dict[str, Any]) -> str:
        """Format LASER strategy results for display"""
        if result["status"] != "success":
            return f"""
╔══════════════════════════════════════════════════════════════════╗
║  ❌ LASER Strategy Error
╚══════════════════════════════════════════════════════════════════╝

Error: {result.get('error', 'Unknown error')}
Timestamp: {result['timestamp']}
"""
        
        data = result["data"]
        filtered_trades = data["filtered_trades"]
        
        # Calculate statistics
        buy_trades = len([t for t in filtered_trades if t["transactionType"] == "BUY"])
        sell_trades = len([t for t in filtered_trades if t["transactionType"] == "SELL"])
        
        return f"""
╔══════════════════════════════════════════════════════════════════╗
║  📊 LASER Strategy Analysis - {data['symbol']}
╚══════════════════════════════════════════════════════════════════╝

🏢 Company Profile:
  • Company: {data['company']}
  • Industry: {data['profile']['industry']}
  • Market Cap: ${data['profile']['market_cap']:,.2f}M
  • Exchange: {data['profile']['exchange']}

📈 Trading Activity:
  • Total Insider Trades: {data['total_trades']}
  • Filtered Trades: {data['filtered_count']}
  • Buy Signals: {buy_trades}
  • Sell Signals: {sell_trades}

🔍 LASER Analysis:
  • Buy/Sell Ratio: {buy_trades/sell_trades if sell_trades > 0 else "∞"}
  • Signal Strength: {"Strong" if data['filtered_count'] >= 3 else "Moderate" if data['filtered_count'] > 0 else "Weak"}

🧠 Neural Analysis:
{data['analysis']}

⏰ Last Updated: {result['timestamp']}
"""

async def main():
    """Run the LaserTradingAgent demo"""
    config = {
        "min_transaction_value": 100000,
        "min_insider_consensus": 3,
        "lookback_days": 30
    }
    
    agent = LaserTradingAgent(config)
    
    # Demo with popular tech stocks
    symbols = ["AAPL", "MSFT", "GOOGL"]
    for symbol in symbols:
        result = await agent.execute(symbol)
        print(agent.format_output(result))
        await asyncio.sleep(1)  # Pause between symbols

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
