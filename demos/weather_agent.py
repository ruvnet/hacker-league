"""Demo agent that fetches and processes weather data with enterprise-grade features."""

import asyncio
import logging
import aiohttp
import ssl
import os
import json
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ANSI color codes for formatted output
CYAN = '\033[0;36m'
GREEN = '\033[0;32m'
NC = '\033[0m'  # No Color

class WeatherAgent:
    """Agent that demonstrates enterprise-grade API integration and data processing"""
    
    def __init__(self):
        self.log = logging.getLogger("demos.weather_agent")
        self.name = "weather_agent"
        self.session = None
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5"

    async def _init_session(self) -> None:
        """Initialize aiohttp session with SSL context"""
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

    def _kelvin_to_celsius(self, kelvin: float) -> float:
        """Convert Kelvin to Celsius"""
        return round(kelvin - 273.15, 1)

    def _kelvin_to_fahrenheit(self, kelvin: float) -> float:
        """Convert Kelvin to Fahrenheit"""
        return round((kelvin - 273.15) * 9/5 + 32, 1)

    def _format_weather_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Format raw weather data"""
        temp_k = data["main"]["temp"]
        return {
            "location": {
                "city": data["name"],
                "country": data["sys"]["country"],
                "coordinates": {
                    "lat": data["coord"]["lat"],
                    "lon": data["coord"]["lon"]
                }
            },
            "temperature": {
                "celsius": self._kelvin_to_celsius(temp_k),
                "fahrenheit": self._kelvin_to_fahrenheit(temp_k)
            },
            "conditions": {
                "main": data["weather"][0]["main"],
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "wind_speed": data["wind"]["speed"]
            },
            "timestamp": datetime.fromtimestamp(data["dt"], timezone.utc).isoformat()
        }

    async def get_weather(
        self,
        city: str,
        country_code: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get current weather for a location with enterprise-grade error handling"""
        try:
            print(f"""
╔══════════════════════════════════════════════════════════════════╗
║  🌤️ WEATHER SYSTEM v1.0
║     ANALYZING {city.upper()}, {country_code if country_code else ''}...
╚══════════════════════════════════════════════════════════════════╝

{CYAN}▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
📡 FETCHING WEATHER DATA
🧮 PROCESSING: ACTIVE
📊 ANALYSIS: READY
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀{NC}
""")
            
            if not self.api_key:
                raise ValueError("OPENWEATHER_API_KEY environment variable is required")
                
            await self._init_session()
            
            # Build query with error handling
            location = city if not country_code else f"{city},{country_code}"
            
            # Make API request
            print(f"{GREEN}[WEATHER] Phase 1: Data Collection{NC}")
            self.log.info(f"Fetching weather data for {location}")
            
            params = {
                "q": location,
                "appid": self.api_key
            }
            
            async with self.session.get(
                f"{self.base_url}/weather",
                params=params
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    print("✅ Weather data retrieved\n")
                    
                    # Process and format data
                    print(f"{GREEN}[WEATHER] Phase 2: Data Processing{NC}")
                    print("🧮 Processing weather information...")
                    formatted_data = self._format_weather_data(data)
                    print("✅ Processing complete\n")
                    
                    print(f"""
{CYAN}▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
✨ ANALYSIS COMPLETE
📊 DATA PROCESSED
🎯 READY FOR DISPLAY
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀{NC}
""")
                    
                    return {
                        "status": "success",
                        "data": formatted_data,
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }
                else:
                    error_text = await response.text()
                    raise RuntimeError(f"Weather API error: {error_text}")
                    
        except Exception as e:
            self.log.error(f"Error fetching weather: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
        finally:
            await self._close_session()

    def format_output(self, result: Dict[str, Any]) -> str:
        """Format weather data for display with improved visuals"""
        if result["status"] != "success":
            return f"""
╔══════════════════════════════════════════════════════════════════╗
║  ❌ Weather Data Error
╚══════════════════════════════════════════════════════════════════╝

Error: {result.get('error', 'Unknown error')}
Timestamp: {result['timestamp']}
"""
        
        data = result["data"]
        conditions = data['conditions']['main'].lower()
        
        # Select weather emoji based on conditions
        weather_emoji = "🌤️"  # default
        if "cloud" in conditions:
            weather_emoji = "☁️"
        elif "rain" in conditions:
            weather_emoji = "🌧️"
        elif "snow" in conditions:
            weather_emoji = "🌨️"
        elif "clear" in conditions:
            weather_emoji = "☀️"
        elif "storm" in conditions or "thunder" in conditions:
            weather_emoji = "⛈️"
        
        return f"""
╔══════════════════════════════════════════════════════════════════╗
║  {weather_emoji}  Weather Report - {data['location']['city']}, {data['location']['country']}
╚══════════════════════════════════════════════════════════════════╝

📍 Location:
  • Coordinates: {data['location']['coordinates']['lat']}°N, {data['location']['coordinates']['lon']}°E

🌡️ Temperature:
  • Celsius: {data['temperature']['celsius']}°C
  • Fahrenheit: {data['temperature']['fahrenheit']}°F

🌥️ Conditions:
  • Weather: {data['conditions']['main']} ({data['conditions']['description']})
  • Humidity: {data['conditions']['humidity']}%
  • Pressure: {data['conditions']['pressure']} hPa
  • Wind Speed: {data['conditions']['wind_speed']} m/s

⏰ Last Updated: {data['timestamp']}
"""

async def main():
    """Run the WeatherAgent demo with enterprise-grade setup"""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    agent = WeatherAgent()
    
    # Demo cities with country codes
    locations = [
        ("London", "UK"),
        ("New York", "US"),
        ("Tokyo", "JP"),
        ("Sydney", "AU"),
        ("Paris", "FR")
    ]
    
    for city, country in locations:
        try:
            result = await agent.get_weather(city, country)
            print(agent.format_output(result))
            await asyncio.sleep(1)  # Pause between demos
        except Exception as e:
            logging.error(f"Error processing {city}: {str(e)}")
            continue

if __name__ == "__main__":
    asyncio.run(main())
