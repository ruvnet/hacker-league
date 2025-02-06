"""Demo agent that handles stock price data with enterprise-grade technical analysis."""

import asyncio
import logging
import aiohttp
import ssl
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional, List
import statistics

# ANSI color codes for formatted output
CYAN = '\033[0;36m'
GREEN = '\033[0;32m'
YELLOW = '\033[0;33m'
RED = '\033[0;31m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color

class StockAgent:
    """Agent that demonstrates enterprise-grade real-time data handling and analysis"""
    
    def __init__(self):
        self.log = logging.getLogger("demos.stock_agent")
        self.name = "stock_agent"
        self.session = None
        
        # Cache for technical indicators (using local mock data)
        self.indicators_cache = {}

    async def _init_session(self) -> None:
        """Initialize aiohttp session with enterprise-grade security"""
        if self.session is None or self.session.closed:
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = True
            ssl_context.verify_mode = ssl.CERT_REQUIRED
            
            timeout = aiohttp.ClientTimeout(total=30)
            connector = aiohttp.TCPConnector(
                ssl=ssl_context,
                limit=100,
                limit_per_host=20,
                use_dns_cache=True
            )
            self.session = aiohttp.ClientSession(
                connector=connector,
                timeout=timeout
            )

    async def _close_session(self) -> None:
        """Close aiohttp session"""
        if self.session and not self.session.closed:
            await self.session.close()

    def _calculate_sma(self, prices: List[float], period: int) -> float:
        """Calculate Simple Moving Average with validation"""
        if len(prices) < period:
            return 0
        return statistics.mean(prices[-period:])

    def _calculate_rsi(self, prices: List[float], period: int = 14) -> float:
        """Calculate Relative Strength Index with improved accuracy"""
        if len(prices) < period + 1:
            return 50  # Default to neutral

        deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
        gains = [d if d > 0 else 0 for d in deltas]
        losses = [-d if d < 0 else 0 for d in deltas]

        avg_gain = statistics.mean(gains[-period:])
        avg_loss = statistics.mean(losses[-period:])

        if avg_loss == 0:
            return 100
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

    def _calculate_bollinger_bands(
        self,
        prices: List[float],
        period: int = 20,
        num_std: float = 2
    ) -> Dict[str, float]:
        """Calculate Bollinger Bands with robust validation"""
        if len(prices) < period:
            return {"upper": 0, "middle": 0, "lower": 0}

        sma = self._calculate_sma(prices, period)
        std = statistics.stdev(prices[-period:])

        return {
            "upper": sma + (std * num_std),
            "middle": sma,
            "lower": sma - (std * num_std)
        }

    def _analyze_trend(self, technical_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze market trends with comprehensive signals"""
        sma_20 = technical_data["sma"]["20"]
        sma_50 = technical_data["sma"]["50"]
        sma_200 = technical_data["sma"]["200"]
        rsi = technical_data["rsi"]
        bb = technical_data["bollinger_bands"]
        
        # Trend analysis
        short_trend = "BULLISH" if sma_20 > sma_50 else "BEARISH"
        long_trend = "BULLISH" if sma_50 > sma_200 else "BEARISH"
        
        # RSI conditions
        rsi_signal = "OVERSOLD" if rsi < 30 else "OVERBOUGHT" if rsi > 70 else "NEUTRAL"
        
        # Volatility
        bb_width = (bb["upper"] - bb["lower"]) / bb["middle"]
        volatility = "HIGH" if bb_width > 0.1 else "MODERATE" if bb_width > 0.05 else "LOW"
        
        return {
            "short_term": short_trend,
            "long_term": long_trend,
            "momentum": rsi_signal,
            "volatility": volatility,
            "strength": "STRONG" if abs(sma_20 - sma_50) / sma_50 > 0.02 else "WEAK"
        }

    async def get_stock_data(
        self,
        symbol: str,
        interval: str = "1d",
        limit: int = 100
    ) -> Dict[str, Any]:
        """Get historical stock data with enterprise-grade processing"""
        try:
            print(f"""
╔══════════════════════════════════════════════════════════════════╗
║  📈 MARKET ANALYSIS SYSTEM v1.0
║     ANALYZING {symbol}...
╚══════════════════════════════════════════════════════════════════╝

{CYAN}▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
📡 FETCHING MARKET DATA
🧮 TECHNICAL ANALYSIS: READY
📊 TREND ANALYSIS: READY
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀{NC}
""")
            await self._init_session()
            
            print(f"{GREEN}[MARKET] Phase 1: Data Collection{NC}")
            self.log.info(f"Fetching stock data for {symbol}")
            
            # Generate mock price data
            base_price = 100.0
            prices = []
            timestamps = []
            
            now = datetime.now(timezone.utc)
            for i in range(limit):
                time_offset = timedelta(days=limit-i-1)
                if interval == "1h":
                    time_offset = timedelta(hours=limit-i-1)
                
                timestamp = now - time_offset
                # Enhanced price simulation
                change = (hash(f"{symbol}{timestamp}") % 200 - 100) / 1000
                price = base_price * (1 + change)
                base_price = price
                
                prices.append(price)
                timestamps.append(timestamp.isoformat())
            
            print("✅ Price data retrieved\n")
            
            print(f"{GREEN}[MARKET] Phase 2: Technical Analysis{NC}")
            print("🧮 Computing technical indicators...")
            
            # Calculate technical indicators
            technical_data = {
                "sma": {
                    "20": self._calculate_sma(prices, 20),
                    "50": self._calculate_sma(prices, 50),
                    "200": self._calculate_sma(prices, 200)
                },
                "rsi": self._calculate_rsi(prices),
                "bollinger_bands": self._calculate_bollinger_bands(prices)
            }
            
            print("✅ Technical analysis complete\n")
            
            print(f"{GREEN}[MARKET] Phase 3: Trend Analysis{NC}")
            print("📊 Analyzing market patterns...")
            
            # Analyze trends
            trend_analysis = self._analyze_trend(technical_data)
            
            print("✅ Trend analysis complete\n")
            
            print(f"""
{CYAN}▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
✨ ANALYSIS COMPLETE
📊 SIGNALS GENERATED
🎯 READY FOR DISPLAY
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀{NC}
""")
            
            return {
                "status": "success",
                "data": {
                    "symbol": symbol,
                    "interval": interval,
                    "prices": list(zip(timestamps, prices)),
                    "technical_indicators": technical_data,
                    "trend_analysis": trend_analysis,
                    "current_price": prices[-1],
                    "change_24h": ((prices[-1] - prices[-2]) / prices[-2]) * 100
                },
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            self.log.error(f"Error analyzing market data: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
        finally:
            await self._close_session()

    def format_output(self, result: Dict[str, Any]) -> str:
        """Format stock data with enhanced visual presentation"""
        if result["status"] != "success":
            return f"""
╔══════════════════════════════════════════════════════════════════╗
║  ❌ Market Analysis Error
╚══════════════════════════════════════════════════════════════════╝

Error: {result.get('error', 'Unknown error')}
Timestamp: {result['timestamp']}
"""
        
        data = result["data"]
        tech = data["technical_indicators"]
        trend = data["trend_analysis"]
        
        # Color coding based on trends
        price_color = GREEN if data['change_24h'] > 0 else RED
        short_term_color = GREEN if trend['short_term'] == "BULLISH" else RED
        long_term_color = GREEN if trend['long_term'] == "BULLISH" else RED
        
        # Momentum indicator
        momentum_color = GREEN if trend['momentum'] == "OVERSOLD" else RED if trend['momentum'] == "OVERBOUGHT" else YELLOW
        momentum_emoji = "📈" if trend['momentum'] == "OVERBOUGHT" else "📉" if trend['momentum'] == "OVERSOLD" else "↔️"
        
        # Generate ASCII chart for price bands
        current_price = data['current_price']
        bb = tech['bollinger_bands']
        price_range = bb['upper'] - bb['lower']
        chart_width = 20
        
        if price_range > 0:
            position = int((current_price - bb['lower']) / price_range * chart_width)
            chart = "─" * position + "●" + "─" * (chart_width - position - 1)
        else:
            chart = "─" * (chart_width // 2) + "●" + "─" * (chart_width // 2)
        
        return f"""
╔══════════════════════════════════════════════════════════════════╗
║  📊 Market Analysis - {data['symbol']}
╚══════════════════════════════════════════════════════════════════╝

💰 Price Action:
  • Current Price: {price_color}${data['current_price']:.2f}{NC}
  • 24h Change: {price_color}{data['change_24h']:+.2f}%{NC}
  • Price Range: ${bb['lower']:.2f} ─── ${bb['upper']:.2f}
    {chart}

📈 Technical Analysis:
  • Moving Averages:
    - SMA 20: ${tech['sma']['20']:.2f}
    - SMA 50: ${tech['sma']['50']:.2f}
    - SMA 200: ${tech['sma']['200']:.2f}
  
  • RSI (14): {momentum_color}{tech['rsi']:.2f} ({trend['momentum']}) {momentum_emoji}{NC}
  
  • Bollinger Bands:
    - Upper: ${bb['upper']:.2f}
    - Middle: ${bb['middle']:.2f}
    - Lower: ${bb['lower']:.2f}

🎯 Market Analysis:
  • Short-term Trend: {short_term_color}{trend['short_term']}{NC}
  • Long-term Trend: {long_term_color}{trend['long_term']}{NC}
  • Momentum: {momentum_color}{trend['momentum']}{NC}
  • Volatility: {YELLOW}{trend['volatility']}{NC}
  • Signal Strength: {BLUE}{trend['strength']}{NC}

⏰ Last Updated: {result['timestamp']}
"""

async def main():
    """Run the StockAgent demo with enterprise-grade setup"""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    agent = StockAgent()
    
    # Demo with major tech companies
    symbols = ["AAPL", "GOOGL", "MSFT", "AMZN", "META"]
    
    for symbol in symbols:
        try:
            result = await agent.get_stock_data(symbol)
            print(agent.format_output(result))
            await asyncio.sleep(1)  # Pause between demos
        except Exception as e:
            logging.error(f"Error processing {symbol}: {str(e)}")
            continue

if __name__ == "__main__":
    asyncio.run(main())
