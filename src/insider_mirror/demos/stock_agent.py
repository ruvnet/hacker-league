"""Demo agent that analyzes stock data using Finnhub and OpenRouter."""

import asyncio
import logging
import aiohttp
import os
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from ..agents.base_agent import BaseAgent
from ..cli.parser import ArgumentParser

class StockAgent(BaseAgent):
    """Agent that demonstrates market data analysis"""
    
    def __init__(self, agent_config: Dict[str, Any]):
        self.name = "stock_agent"  # Set name before super().__init__
        super().__init__(self.name, agent_config)
        self.session = None
        self.model = agent_config.get("model", ArgumentParser.DEFAULT_MODEL)

    async def _init_session(self) -> None:
        """Initialize aiohttp session"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()

    async def _close_session(self) -> None:
        """Close aiohttp session"""
        if self.session and not self.session.closed:
            await self.session.close()

    async def _fetch_stock_data(self, symbol: str) -> Dict[str, Any]:
        """Fetch stock data from Finnhub API"""
        try:
            await self._init_session()
            
            api_key = os.getenv("FINNHUB_API_KEY")
            if not api_key:
                raise ValueError("FINNHUB_API_KEY environment variable is required")
            
            headers = {
                "X-Finnhub-Token": api_key
            }
            
            # Fetch quote data
            self.log.info(f"Fetching quote data for {symbol}")
            async with self.session.get(
                f"https://finnhub.io/api/v1/quote?symbol={symbol}",
                headers=headers
            ) as response:
                if response.status == 200:
                    quote_data = await response.json()
                else:
                    error_text = await response.text()
                    raise RuntimeError(f"Quote API error: {error_text}")
            
            # Fetch company profile
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
            
            return {
                "quote": quote_data,
                "profile": profile_data
            }
            
        except Exception as e:
            self.log.error(f"Error fetching stock data: {str(e)}")
            raise
            
        finally:
            await self._close_session()

    async def _analyze_stock(self, stock_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze stock data using OpenRouter LLM"""
        try:
            quote = stock_data["quote"]
            profile = stock_data["profile"]
            
            # Format data for analysis
            prompt = f"""Analyze this stock data and provide insights:
Company: {profile.get('name', 'Unknown')} ({profile.get('ticker', 'Unknown')})
Industry: {profile.get('finnhubIndustry', 'Unknown')}
Market Cap: ${profile.get('marketCapitalization', 0):,.2f}M

Current Price: ${quote.get('c', 0):,.2f}
Previous Close: ${quote.get('pc', 0):,.2f}
Day Change: {((quote.get('c', 0) - quote.get('pc', 0)) / quote.get('pc', 1) * 100):,.2f}%
Day High: ${quote.get('h', 0):,.2f}
Day Low: ${quote.get('l', 0):,.2f}

Provide:
1. A brief overview of the company and its current market position
2. Analysis of today's price action and notable patterns
3. Key technical levels and price targets
4. Potential risks and opportunities
"""
            # Call OpenRouter API
            api_key = os.getenv("OPENROUTER_API_KEY")
            if not api_key:
                raise ValueError("OPENROUTER_API_KEY environment variable is required")
            
            await self._init_session()
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "X-Title": "Insider Trading Mirror System",
                "HTTP-Referer": "https://github.com/your-username/insider-mirror",
                "Content-Type": "application/json",
                "OpenAI-Organization": "org-123"  # Required by OpenRouter
            }
            
            data = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 1000
            }
            
            self.log.info(f"Analyzing stock data with LLM model: {self.model}")
            async with self.session.post(
                "https://api.openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data
            ) as response:
                if response.status == 200:
                    llm_response = await response.json()
                    analysis = llm_response["choices"][0]["message"]["content"]
                    return {
                        "status": "success",
                        "analysis": analysis,
                        "model": self.model
                    }
                else:
                    error_text = await response.text()
                    raise RuntimeError(f"OpenRouter API error: {error_text}")
                    
        except Exception as e:
            self.log.error(f"Error analyzing stock: {str(e)}")
            raise
            
        finally:
            await self._close_session()

    async def execute(
        self,
        symbol: str
    ) -> Dict[str, Any]:
        """Execute stock agent tasks"""
        try:
            self.track_progress(1, "Fetching stock data")
            stock_data = await self._fetch_stock_data(symbol)
            
            self.track_progress(2, "Analyzing market data")
            analysis = await self._analyze_stock(stock_data)
            
            self.track_progress(3, "Generating report")
            
            return {
                "status": "success",
                "data": {
                    "symbol": symbol,
                    "company": stock_data["profile"].get("name", "Unknown"),
                    "quote": {
                        "current": stock_data["quote"]["c"],
                        "previous_close": stock_data["quote"]["pc"],
                        "change_percent": ((stock_data["quote"]["c"] - stock_data["quote"]["pc"]) / stock_data["quote"]["pc"] * 100),
                        "high": stock_data["quote"]["h"],
                        "low": stock_data["quote"]["l"]
                    },
                    "profile": {
                        "industry": stock_data["profile"].get("finnhubIndustry", "Unknown"),
                        "market_cap": stock_data["profile"].get("marketCapitalization", 0),
                        "exchange": stock_data["profile"].get("exchange", "Unknown")
                    },
                    "analysis": analysis["analysis"],
                    "model": analysis["model"]
                },
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            self.log.error(f"Error executing stock agent: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

    def format_output(self, result: Dict[str, Any]) -> str:
        """Format stock data for display"""
        if result["status"] != "success":
            return f"""
╔══════════════════════════════════════════════════════════════════╗
║  ❌ Stock Analysis Error
╚══════════════════════════════════════════════════════════════════╝

Error: {result.get('error', 'Unknown error')}
Timestamp: {result['timestamp']}
"""
        
        data = result["data"]
        quote = data["quote"]
        profile = data["profile"]
        
        # Determine trend emoji
        trend = "🟢" if quote["change_percent"] > 0 else "🔴" if quote["change_percent"] < 0 else "⚪"
        
        return f"""
╔══════════════════════════════════════════════════════════════════╗
║  📊 Stock Analysis - {data['company']} ({data['symbol']})
╚══════════════════════════════════════════════════════════════════╝

📈 Market Data:
  • Current Price: ${quote['current']:,.2f}
  • Previous Close: ${quote['previous_close']:,.2f}
  • Day Change: {trend} {quote['change_percent']:+.2f}%
  • Day Range: ${quote['low']:,.2f} - ${quote['high']:,.2f}

🏢 Company Profile:
  • Industry: {profile['industry']}
  • Market Cap: ${profile['market_cap']:,.2f}M
  • Exchange: {profile['exchange']}

🔍 Analysis (using {data['model']}):
{data['analysis']}

⏰ Last Updated: {result['timestamp']}
"""

    def cleanup(self) -> None:
        """Clean up resources"""
        super().cleanup()
        if self.session:
            asyncio.create_task(self._close_session())