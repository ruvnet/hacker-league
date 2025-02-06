"""Mirror Trade Agent that replicates trades from a signal source with enterprise-grade features."""

import asyncio
import logging
import aiohttp
import ssl
import json
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
import random

# ANSI color codes for formatted output
CYAN = '\033[0;36m'
GREEN = '\033[0;32m'
YELLOW = '\033[0;33m'
RED = '\033[0;31m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color

class MirrorTradeAgent:
    """Agent that mirrors trades with enterprise-grade security and monitoring."""
    
    def __init__(self):
        self.log = logging.getLogger("demos.mirror_trade_agent")
        self.name = "mirror_trade_agent"
        self.session = None
        self.trades: List[Dict[str, Any]] = []
        self.stats = {
            "trades_received": 0,
            "trades_executed": 0,
            "errors": 0,
            "start_time": datetime.now(timezone.utc)
        }

    async def _init_session(self) -> None:
        """Initialize aiohttp session with enterprise-grade security"""
        if self.session is None or self.session.closed:
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = True
            ssl_context.verify_mode = ssl.CERT_REQUIRED
            
            # Enterprise-grade connection parameters
            connector = aiohttp.TCPConnector(
                ssl=ssl_context,
                limit=100,
                limit_per_host=20,
                use_dns_cache=True
            )
            
            timeout = aiohttp.ClientTimeout(total=30)
            self.session = aiohttp.ClientSession(
                connector=connector,
                timeout=timeout
            )

    async def _close_session(self) -> None:
        """Close aiohttp session gracefully"""
        if self.session and not self.session.closed:
            await self.session.close()

    def _generate_mock_signals(self) -> List[Dict[str, Any]]:
        """Generate mock trade signals for demo purposes"""
        symbols = ["AAPL", "GOOGL", "MSFT", "AMZN", "META"]
        actions = ["BUY", "SELL"]
        signals = []
        
        for _ in range(random.randint(1, 3)):
            symbol = random.choice(symbols)
            action = random.choice(actions)
            price = random.uniform(100, 1000)
            quantity = random.randint(1, 100)
            
            signals.append({
                "symbol": symbol,
                "action": action,
                "price": round(price, 2),
                "quantity": quantity,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "signal_strength": random.uniform(0.1, 1.0),
                "source": "mock_signal_generator"
            })
        
        return signals

    def _validate_trade(self, trade: Dict[str, Any]) -> bool:
        """Validate trade signal with comprehensive checks"""
        required_fields = ["symbol", "action", "price", "quantity"]
        
        # Check required fields
        if not all(field in trade for field in required_fields):
            self.log.warning(f"Invalid trade signal - missing fields: {trade}")
            return False
            
        # Validate action
        if trade["action"] not in ["BUY", "SELL"]:
            self.log.warning(f"Invalid trade action: {trade['action']}")
            return False
            
        # Validate price and quantity
        if trade["price"] <= 0 or trade["quantity"] <= 0:
            self.log.warning(f"Invalid price or quantity: {trade}")
            return False
            
        return True

    async def fetch_signals(self) -> None:
        """Fetch trade signals with enterprise-grade error handling"""
        print(f"""
╔══════════════════════════════════════════════════════════════════╗
║  🔄 MIRROR TRADE SYSTEM v1.0
║     FETCHING SIGNALS...
╚══════════════════════════════════════════════════════════════════╝

{CYAN}▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
📡 SIGNAL SOURCE: ACTIVE
🔒 SECURE CONNECTION: READY
📊 TRADE EXECUTION: STANDBY
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀{NC}
""")
        
        try:
            print(f"{GREEN}[MIRROR] Phase 1: Signal Collection{NC}")
            signals = self._generate_mock_signals()
            print(f"📡 Received {len(signals)} new signals\n")
            
            print(f"{GREEN}[MIRROR] Phase 2: Signal Validation{NC}")
            valid_signals = []
            for signal in signals:
                if self._validate_trade(signal):
                    valid_signals.append(signal)
                    print(f"✅ Validated signal for {signal['symbol']}")
                else:
                    print(f"❌ Invalid signal for {signal['symbol']}")
            
            self.trades.extend(valid_signals)
            self.stats["trades_received"] += len(valid_signals)
            print(f"\n📊 {len(valid_signals)}/{len(signals)} signals validated\n")
            
        except Exception as e:
            self.stats["errors"] += 1
            self.log.error(f"Error fetching trade signals: {str(e)}")
            print(f"{RED}❌ Error fetching signals: {str(e)}{NC}\n")

    async def execute_trades(self) -> None:
        """Execute mirrored trades with comprehensive monitoring"""
        if not self.trades:
            return
            
        print(f"{GREEN}[MIRROR] Phase 3: Trade Execution{NC}")
        successful_trades = 0
        
        for trade in self.trades:
            try:
                # Simulate trade execution
                print(f"🔄 Executing {trade['action']} order:")
                print(f"   Symbol: {trade['symbol']}")
                print(f"   Price: ${trade['price']:.2f}")
                print(f"   Quantity: {trade['quantity']}")
                print(f"   Value: ${trade['price'] * trade['quantity']:,.2f}")
                
                # In a real implementation, this would interact with a brokerage API
                await asyncio.sleep(0.5)  # Simulate API call
                
                successful_trades += 1
                print(f"✅ Trade executed successfully\n")
                
            except Exception as e:
                self.stats["errors"] += 1
                self.log.error(f"Error executing trade: {str(e)}")
                print(f"{RED}❌ Trade execution failed: {str(e)}{NC}\n")
        
        self.stats["trades_executed"] += successful_trades
        self.trades.clear()
        
        print(f"""
{CYAN}▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
✨ EXECUTION COMPLETE
📊 TRADES PROCESSED: {successful_trades}
🎯 READY FOR NEXT CYCLE
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀{NC}
""")

    def format_status(self) -> str:
        """Format system status with enterprise-grade metrics"""
        uptime = datetime.now(timezone.utc) - self.stats["start_time"]
        hours = uptime.total_seconds() / 3600
        
        # Calculate success rate
        total_trades = self.stats["trades_received"]
        executed_trades = self.stats["trades_executed"]
        success_rate = (executed_trades / total_trades * 100) if total_trades > 0 else 0
        
        return f"""
╔══════════════════════════════════════════════════════════════════╗
║  📊 Mirror Trade System Status
╚══════════════════════════════════════════════════════════════════╝

⚡ System Metrics:
  • Uptime: {uptime}
  • Trades/Hour: {executed_trades / hours:.1f}
  • Success Rate: {success_rate:.1f}%

📈 Trade Statistics:
  • Signals Received: {self.stats['trades_received']}
  • Trades Executed: {self.stats['trades_executed']}
  • Errors: {self.stats['errors']}

⏰ Last Updated: {datetime.now(timezone.utc).isoformat()}
"""

    async def run(self, demo_duration: int = 5) -> None:
        """Run the mirror trade agent with enterprise-grade monitoring"""
        try:
            await self._init_session()
            cycles = 0
            
            while cycles < demo_duration:
                await self.fetch_signals()
                await asyncio.sleep(1)  # Brief pause for demo
                await self.execute_trades()
                print(self.format_status())
                cycles += 1
                await asyncio.sleep(2)  # Pause between cycles
                
        except KeyboardInterrupt:
            print(f"\n{YELLOW}Gracefully shutting down mirror trade system...{NC}")
        finally:
            await self._close_session()

async def main():
    """Run the MirrorTradeAgent demo with enterprise-grade setup"""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    agent = MirrorTradeAgent()
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())
