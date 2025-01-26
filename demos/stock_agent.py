"""Demo agent that handles stock price data and technical analysis."""

import asyncio
import logging
import aiohttp
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional, List
import statistics

class StockAgent:
    """Agent that demonstrates real-time data handling and analysis"""
    
    def __init__(self):
        self.log = logging.getLogger("demos.stock_agent")
        self.name = "stock_agent"
        self.session = None
        
        # Cache for technical indicators (using local mock data)
        self.indicators_cache = {}

    async def _init_session(self) -> None:
        """Initialize aiohttp session"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()

    async def _close_session(self) -> None:
        """Close aiohttp session"""
        if self.session and not self.session.closed:
            await self.session.close()

    def _calculate_sma(self, prices: List[float], period: int) -> float:
        """Calculate Simple Moving Average"""
        if len(prices) < period:
            return 0
        return statistics.mean(prices[-period:])

    def _calculate_rsi(self, prices: List[float], period: int = 14) -> float:
        """Calculate Relative Strength Index"""
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
        """Calculate Bollinger Bands"""
        if len(prices) < period:
            return {"upper": 0, "middle": 0, "lower": 0}

        sma = self._calculate_sma(prices, period)
        std = statistics.stdev(prices[-period:])

        return {
            "upper": sma + (std * num_std),
            "middle": sma,
            "lower": sma - (std * num_std)
        }

    async def get_stock_data(
        self,
        symbol: str,
        interval: str = "1d",
        limit: int = 100
    ) -> Dict[str, Any]:
        """Get historical stock data"""
        try:
            await self._init_session()
            
            # Demo data generation (replace with actual API call)
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
                # Simple price simulation with some randomness
                change = (hash(f"{symbol}{timestamp}") % 200 - 100) / 1000
                price = base_price * (1 + change)
                base_price = price
                
                prices.append(price)
                timestamps.append(timestamp.isoformat())
            
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
            
            return {
                "status": "success",
                "data": {
                    "symbol": symbol,
                    "interval": interval,
                    "prices": list(zip(timestamps, prices)),
                    "technical_indicators": technical_data,
                    "current_price": prices[-1],
                    "change_24h": ((prices[-1] - prices[-2]) / prices[-2]) * 100
                },
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            self.log.error(f"Error fetching stock data: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
        finally:
            await self._close_session()

    def format_output(self, result: Dict[str, Any]) -> str:
        """Format stock data for display"""
        if result["status"] != "success":
            return f"""
╔══════════════════════════════════════════════════════════════════╗
║  ❌ Stock Data Error
╚══════════════════════════════════════════════════════════════════╝

Error: {result.get('error', 'Unknown error')}
Timestamp: {result['timestamp']}
"""
        
        data = result["data"]
        tech = data["technical_indicators"]
        
        # Determine trend signals
        rsi = tech["rsi"]
        rsi_signal = "OVERSOLD 📉" if rsi < 30 else "OVERBOUGHT 📈" if rsi > 70 else "NEUTRAL ↔️"
        
        sma_20 = tech["sma"]["20"]
        sma_50 = tech["sma"]["50"]
        trend_signal = "BULLISH 🟢" if sma_20 > sma_50 else "BEARISH 🔴" if sma_20 < sma_50 else "NEUTRAL ⚪"
        
        return f"""
╔══════════════════════════════════════════════════════════════════╗
║  📊 Stock Analysis - {data['symbol']}
╚══════════════════════════════════════════════════════════════════╝

💰 Price Information:
  • Current Price: ${data['current_price']:.2f}
  • 24h Change: {data['change_24h']:+.2f}%

📈 Technical Indicators:
  • Moving Averages:
    - SMA 20: ${tech['sma']['20']:.2f}
    - SMA 50: ${tech['sma']['50']:.2f}
    - SMA 200: ${tech['sma']['200']:.2f}
  
  • RSI (14): {tech['rsi']:.2f} ({rsi_signal})
  
  • Bollinger Bands:
    - Upper: ${tech['bollinger_bands']['upper']:.2f}
    - Middle: ${tech['bollinger_bands']['middle']:.2f}
    - Lower: ${tech['bollinger_bands']['lower']:.2f}

📊 Analysis:
  • Trend: {trend_signal}
  • Volatility: {'HIGH 📊' if tech['bollinger_bands']['upper'] - tech['bollinger_bands']['lower'] > data['current_price'] * 0.1 else 'LOW 📉'}

⏰ Last Updated: {result['timestamp']}
"""

async def main():
    """Demo the stock agent"""
    agent = StockAgent()
    
    # Demo stocks
    symbols = ["AAPL", "GOOGL", "MSFT", "AMZN"]
    
    for symbol in symbols:
        result = await agent.get_stock_data(symbol)
        print(agent.format_output(result))
        await asyncio.sleep(1)  # Pause between demos

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())